import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, set_env_vars

def drop_all_tables():
    """Drop all tables in the database to start fresh"""
    
    print("\n🔄 Dropping all existing tables...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        
        # Enable autocommit mode
        conn.autocommit = True
        
        # Create a cursor
        cursor = conn.cursor()
        
        # First disable foreign key checks temporarily
        cursor.execute("SET session_replication_role = 'replica';")
        
        # Get a list of all tables
        cursor.execute("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public';
        """)
        
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found to drop.")
        else:
            # Drop each table
            for table in tables:
                table_name = table[0]
                print(f"Dropping table: {table_name}")
                cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE;')
            
            print(f"✅ Successfully dropped {len(tables)} tables")
        
        # Re-enable foreign key checks
        cursor.execute("SET session_replication_role = 'origin';")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database reset completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error dropping tables: {str(e)}")

if __name__ == "__main__":
    # Set environment variables
    set_env_vars()
    
    # Drop all tables
    drop_all_tables() 