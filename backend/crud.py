from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext
from . import models, schemas

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Role operations
def get_role(db: Session, role_id: int):
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_role_by_name(db: Session, name: str):
    return db.query(models.Role).filter(models.Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: schemas.RoleCreate):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Permission operations
def get_permission(db: Session, permission_id: int):
    return db.query(models.Permission).filter(models.Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str):
    return db.query(models.Permission).filter(models.Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, permission: schemas.PermissionCreate):
    db_permission = models.Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

# Assign permissions to a role
def assign_permission_to_role(db: Session, role_id: int, permission_id: int):
    db_role = get_role(db, role_id)
    db_permission = get_permission(db, permission_id)
    
    if db_role and db_permission:
        db_role.permissions.append(db_permission)
        db.commit()
        db.refresh(db_role)
    return db_role

# User operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_national_id(db: Session, national_id: str):
    return db.query(models.User).filter(models.User.national_id == national_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    # Hash the password properly
    hashed_password = get_password_hash(user.password)
    
    # Convert pydantic model to dict and exclude password
    user_data = user.dict(exclude={"password"})
    
    # מצא את תפקיד האזרח
    citizen_role = get_role_by_name(db, "citizen")
    if not citizen_role:
        # אם תפקיד האזרח לא קיים, צור אותו
        citizen_role_data = schemas.RoleCreate(name="citizen", description="משתמש אזרח רגיל במערכת")
        citizen_role = create_role(db, citizen_role_data)
    
    # קבע תפקיד אזרח למשתמש החדש
    user_data["role_id"] = citizen_role.id
    
    # יצירת ערכי ברירת מחדל לשדות חסרים
    default_values = {
        "is_active": True,
        "capsule_status": "not_ready"
    }
    
    # הוספת ערכי ברירת מחדל לנתוני המשתמש
    for key, value in default_values.items():
        if key not in user_data:
            user_data[key] = value
    
    # Create new user with hashed password
    db_user = models.User(**user_data, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Item operations
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item 