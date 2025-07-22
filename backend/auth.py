from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from backend import crud, models, schemas
from backend.database import get_db
import secrets
import string

# Configuration for JWT
SECRET_KEY = "YOUR_SECRET_KEY_HERE"  # Replace with a proper secret key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# Router initialization
router = APIRouter(prefix="/api/auth", tags=["auth"])

# Models for authentication
class Token(BaseModel):
    access_token: str
    token_type: str
    user: schemas.User

class TokenData(BaseModel):
    email: Optional[str] = None

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

# מודל פשוט לרישום משתמש חדש - רק עם השדות החיוניים
class SimpleRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    national_id: str

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_reset_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def authenticate_user(db: Session, email: str, password: str):
    user = crud.get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# Routes
@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="שם המשתמש או הסיסמה שגויים",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": user
    }

@router.post("/register", response_model=schemas.User)
async def register_user(user_data: SimpleRegisterRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="כתובת המייל כבר רשומה במערכת",
        )
    
    # Check if national ID already exists
    db_user_by_id = crud.get_user_by_national_id(db, national_id=user_data.national_id)
    if db_user_by_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="מספר הזהות כבר רשום במערכת",
        )
    
    # בדיקה שהסיסמה מספיק חזקה
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="הסיסמה חייבת להכיל לפחות 6 תווים",
        )
    
    # בדיקה שמספר הזהות תקין
    if not user_data.national_id.isdigit() or len(user_data.national_id) != 9:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="מספר זהות חייב להכיל 9 ספרות",
        )
    
    # המר את הנתונים למבנה UserCreate המלא עם ערכי ברירת מחדל לשדות החסרים
    user_create_data = schemas.UserCreate(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        national_id=user_data.national_id,
        # שדות אופציונליים יקבלו ערכי ברירת מחדל null
    )
    
    # Create user with citizen role
    return crud.create_user(db=db, user=user_create_data)

@router.post("/password-reset-request", status_code=status.HTTP_200_OK)
async def request_password_reset(request: PasswordResetRequest, db: Session = Depends(get_db)):
    # Get user by email
    user = crud.get_user_by_email(db, email=request.email)
    if not user:
        # Don't reveal that the user doesn't exist for security reasons
        return {"message": "אם כתובת המייל קיימת במערכת, הוראות לאיפוס סיסמה נשלחו אליה"}
    
    # Generate token
    reset_token = generate_reset_token()
    
    # TODO: Store token in DB with expiration time
    # TODO: Send email with reset link
    
    return {"message": "אם כתובת המייל קיימת במערכת, הוראות לאיפוס סיסמה נשלחו אליה"}

@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(reset_data: PasswordReset, db: Session = Depends(get_db)):
    # TODO: Verify token from DB
    # TODO: Update user password
    # For now, we'll just return a success message
    return {"message": "הסיסמה אופסה בהצלחה"} 