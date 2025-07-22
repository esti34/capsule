import os
from sqlalchemy import create_engine, text
from config import set_env_vars, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from backend.database import Base, engine
from backend.models import Role, Permission, User, role_permission
from backend import crud, models, schemas
from sqlalchemy.orm import Session

def init_database():
    """Initialize the database with tables, roles, and permissions"""
    
    print("\n🔄 Initializing database schema and initial data...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Create a database session
        db = Session(engine)
        
        # Create roles
        roles = [
            {"name": "citizen", "description": "Regular citizen user"},
            {"name": "government_office", "description": "Government office representative"},
            {"name": "local_authority", "description": "Local authority representative"},
            {"name": "admin", "description": "System administrator"}
        ]
        
        for role_data in roles:
            # Check if role already exists
            existing_role = crud.get_role_by_name(db, role_data["name"])
            if not existing_role:
                role = schemas.RoleCreate(**role_data)
                crud.create_role(db, role)
                print(f"✅ Created role: {role_data['name']}")
            else:
                print(f"⚠️ Role already exists: {role_data['name']}")
        
        # Create basic permissions
        permissions = [
            {"name": "read_public", "description": "Can read public information"},
            {"name": "edit_profile", "description": "Can edit own profile"},
            {"name": "submit_request", "description": "Can submit requests"},
            {"name": "manage_users", "description": "Can manage users"},
            {"name": "approve_requests", "description": "Can approve requests"},
            {"name": "admin_access", "description": "Has administrative access"}
        ]
        
        for perm_data in permissions:
            # Check if permission already exists
            existing_perm = crud.get_permission_by_name(db, perm_data["name"])
            if not existing_perm:
                perm = schemas.PermissionCreate(**perm_data)
                crud.create_permission(db, perm)
                print(f"✅ Created permission: {perm_data['name']}")
            else:
                print(f"⚠️ Permission already exists: {perm_data['name']}")
        
        # Assign permissions to roles
        # Get roles
        citizen_role = crud.get_role_by_name(db, "citizen")
        gov_role = crud.get_role_by_name(db, "government_office")
        local_role = crud.get_role_by_name(db, "local_authority")
        admin_role = crud.get_role_by_name(db, "admin")
        
        # Get permissions
        read_public = crud.get_permission_by_name(db, "read_public")
        edit_profile = crud.get_permission_by_name(db, "edit_profile")
        submit_request = crud.get_permission_by_name(db, "submit_request")
        manage_users = crud.get_permission_by_name(db, "manage_users")
        approve_requests = crud.get_permission_by_name(db, "approve_requests")
        admin_access = crud.get_permission_by_name(db, "admin_access")
        
        # Assign permissions
        if citizen_role and read_public and edit_profile and submit_request:
            assign_permissions(db, citizen_role, [read_public, edit_profile, submit_request])
            
        if gov_role and read_public and edit_profile and approve_requests:
            assign_permissions(db, gov_role, [read_public, edit_profile, approve_requests])
            
        if local_role and read_public and edit_profile and manage_users and approve_requests:
            assign_permissions(db, local_role, [read_public, edit_profile, manage_users, approve_requests])
            
        if admin_role and read_public and edit_profile and manage_users and approve_requests and admin_access:
            assign_permissions(db, admin_role, [read_public, edit_profile, manage_users, approve_requests, admin_access])
        
        print("✅ Assigned permissions to roles")
        
        # Create admin user if it doesn't exist
        admin_email = "admin@example.com"
        existing_admin = crud.get_user_by_email(db, admin_email)
        
        if not existing_admin:
            from datetime import datetime
            admin_user = schemas.UserCreate(
                email=admin_email,
                password="admin123",  # Will be hashed by the create_user function
                first_name="System",
                last_name="Administrator",
                national_id="000000000",
                city="Admin City",
                street="Admin Street",
                building="1",
                entrance="A",
                postal_code="12345",
                date_of_birth=datetime(1980, 1, 1),
                phone_number="123456789",
                role_id=admin_role.id if admin_role else None
            )
            crud.create_user(db, admin_user)
            print("✅ Created admin user")
        else:
            print("⚠️ Admin user already exists")
        
        db.close()
        print("\n✅ Database initialization completed successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        
def assign_permissions(db, role, permissions):
    """Helper function to assign permissions to a role"""
    for permission in permissions:
        role.permissions.append(permission)
    db.commit()
    db.refresh(role)

if __name__ == "__main__":
    # Set environment variables
    set_env_vars()
    
    # Initialize database
    init_database() 