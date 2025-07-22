import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, set_env_vars
from tabulate import tabulate

def verify_database():
    """Verify the database tables and data"""
    
    print("\n📊 Verifying Database Structure and Content")
    print("=" * 50)
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        
        # Create a cursor
        cursor = conn.cursor()
        
        # 1. List all tables
        print("\n📋 Tables in the database:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        print(tabulate(tables, headers=["Table Name"], tablefmt="pretty"))
        
        # 2. Show roles table structure
        print("\n📋 Roles Table Structure:")
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'roles'
            ORDER BY ordinal_position;
        """)
        roles_structure = cursor.fetchall()
        print(tabulate(roles_structure, headers=["Column Name", "Data Type", "Length", "Nullable"], tablefmt="pretty"))
        
        # 3. Show permissions table structure
        print("\n📋 Permissions Table Structure:")
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'permissions'
            ORDER BY ordinal_position;
        """)
        permissions_structure = cursor.fetchall()
        print(tabulate(permissions_structure, headers=["Column Name", "Data Type", "Length", "Nullable"], tablefmt="pretty"))
        
        # 4. Show users table structure
        print("\n📋 Users Table Structure:")
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        users_structure = cursor.fetchall()
        print(tabulate(users_structure, headers=["Column Name", "Data Type", "Length", "Nullable"], tablefmt="pretty"))
        
        # 5. Show role_permission table structure
        print("\n📋 Role-Permission Association Table Structure:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'role_permission'
            ORDER BY ordinal_position;
        """)
        role_perm_structure = cursor.fetchall()
        print(tabulate(role_perm_structure, headers=["Column Name", "Data Type", "Nullable"], tablefmt="pretty"))
        
        # 6. Show roles data
        print("\n📋 Roles Data:")
        cursor.execute("SELECT id, name, description FROM roles;")
        roles_data = cursor.fetchall()
        print(tabulate(roles_data, headers=["ID", "Name", "Description"], tablefmt="pretty"))
        
        # 7. Show permissions data
        print("\n📋 Permissions Data:")
        cursor.execute("SELECT id, name, description FROM permissions;")
        permissions_data = cursor.fetchall()
        print(tabulate(permissions_data, headers=["ID", "Name", "Description"], tablefmt="pretty"))
        
        # 8. Show role-permission associations
        print("\n📋 Role-Permission Associations:")
        cursor.execute("""
            SELECT r.name AS role_name, p.name AS permission_name
            FROM roles r
            JOIN role_permission rp ON r.id = rp.role_id
            JOIN permissions p ON p.id = rp.permission_id
            ORDER BY r.name, p.name;
        """)
        role_perm_data = cursor.fetchall()
        print(tabulate(role_perm_data, headers=["Role", "Permission"], tablefmt="pretty"))
        
        # 9. Show users data (limited columns for privacy)
        print("\n📋 Users Data (Limited Fields):")
        cursor.execute("""
            SELECT u.id, u.national_id, u.first_name, u.last_name, u.email,
                   r.name AS role_name, u.is_active
            FROM users u
            LEFT JOIN roles r ON u.role_id = r.id;
        """)
        users_data = cursor.fetchall()
        print(tabulate(users_data, headers=["ID", "National ID", "First Name", "Last Name", 
                                         "Email", "Role", "Active"], tablefmt="pretty"))
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database verification completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error verifying database: {str(e)}")
        
if __name__ == "__main__":
    # Set environment variables
    set_env_vars()
    
    # Verify database
    verify_database() 