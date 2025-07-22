import os
from sqlalchemy import create_engine, inspect
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv
import psycopg2

def init_postgres():
    """Initialize PostgreSQL database if it doesn't exist"""
    
    # Load environment variables
    load_dotenv()
    
    # Default connection parameters
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "hacaton_db")
    
    # PostgreSQL connection string
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    try:
        # Step 1: Verify PostgreSQL is running by connecting to default 'postgres' database
        test_conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/postgres"
        test_engine = create_engine(test_conn_string)
        test_conn = test_engine.connect()
        test_conn.close()
        print("✅ PostgreSQL server is running")
        
        # Step 2: Check credentials
        print(f"✅ Credentials for user '{db_user}' are valid")
        
        # Step 3: Check if database exists
        if database_exists(db_url):
            print(f"✅ Database '{db_name}' already exists")
        else:
            # Create database if needed
            create_database(db_url)
            print(f"✅ Database '{db_name}' created successfully")
        
        # Step 4: Verify connection to the database
        engine = create_engine(db_url)
        conn = engine.connect()
        conn.close()
        print(f"✅ Successfully connected to database '{db_name}'")
        
        # Step 5: Check tables using SQLAlchemy Inspector
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"✅ Database contains {len(tables)} tables: {', '.join(tables) if tables else 'No tables yet'}")
        
        print("\n🚀 PostgreSQL setup completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error setting up PostgreSQL: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Verify PostgreSQL is installed and running")
        print("2. Check your PostgreSQL credentials")
        print("3. Ensure the database exists or you have permission to create it")
        print("4. Verify network access to the PostgreSQL server")
        print("5. Check pg_hba.conf to ensure it allows connections from this host")
        print("\nConnection details being used:")
        print(f"  - User: {db_user}")
        print(f"  - Host: {db_host}")
        print(f"  - Port: {db_port}")
        print(f"  - Database: {db_name}")
        exit(1)

if __name__ == "__main__":
    init_postgres() 