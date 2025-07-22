from datetime import datetime
from sqlalchemy.orm import Session
from config import set_env_vars
from backend.database import engine
from backend import crud, models, schemas

def create_citizen_user():
    """Create a new user with the 'citizen' role"""
    
    print("\n🧑‍🤝‍🧑 Creating a new citizen user...")
    
    try:
        # Create a database session
        db = Session(engine)
        
        # Get the citizen role
        citizen_role = crud.get_role_by_name(db, "citizen")
        
        if not citizen_role:
            print("❌ Citizen role not found. Please run init_roles_db.py first.")
            return
        
        # Check if citizen user already exists
        citizen_email = "citizen@example.com"
        existing_user = crud.get_user_by_email(db, citizen_email)
        
        if existing_user:
            print(f"⚠️ Citizen user with email {citizen_email} already exists.")
            return
        
        # Create the citizen user
        citizen_user = schemas.UserCreate(
            email=citizen_email,
            password="citizen123",  # Will be hashed by the create_user function
            first_name="Israeli",
            last_name="Citizen",
            national_id="123456789",
            city="Tel Aviv",
            neighborhood="Central",
            street="Dizengoff",
            building="42",
            entrance="A",
            postal_code="6423902",
            date_of_birth=datetime(1985, 5, 15),
            gender="Male",
            phone_number="0541234567",
            role_id=citizen_role.id
        )
        
        # Add the user to the database
        new_user = crud.create_user(db, citizen_user)
        
        print(f"✅ Citizen user created successfully!")
        print(f"   ID: {new_user.id}")
        print(f"   Name: {new_user.first_name} {new_user.last_name}")
        print(f"   Email: {new_user.email}")
        print(f"   Role: citizen")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error creating citizen user: {str(e)}")

if __name__ == "__main__":
    # Set environment variables
    set_env_vars()
    
    # Create citizen user
    create_citizen_user() 