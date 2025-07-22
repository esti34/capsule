import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import socket
import platform
import sys

def check_postgres_connection():
    """Check PostgreSQL connection and verify configuration"""
    
    # Load environment variables
    load_dotenv()
    
    # Get database connection parameters
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "hacaton_db")
    
    # PostgreSQL connection string
    db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print("\n📊 PostgreSQL Connection Verification")
    print("=" * 40)
    
    # Step 1: Check if PostgreSQL server is reachable
    print("\n🔍 Step 1: Checking if PostgreSQL server is reachable...")
    try:
        # Try to establish a socket connection to the PostgreSQL server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((db_host, int(db_port)))
        if result == 0:
            print(f"✅ PostgreSQL server is reachable at {db_host}:{db_port}")
        else:
            print(f"❌ Could not reach PostgreSQL server at {db_host}:{db_port}")
            print(f"   Make sure PostgreSQL is running and accessible from this machine")
        sock.close()
    except Exception as e:
        print(f"❌ Error checking server reachability: {str(e)}")
    
    # Step 2: Try to connect to the database
    print("\n🔍 Step 2: Checking database credentials and existence...")
    try:
        # Create engine and connect
        engine = create_engine(db_url)
        with engine.connect() as conn:
            print(f"✅ Successfully connected to database '{db_name}'")
            
            # Execute a simple query to check if connection is working
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ PostgreSQL version: {version}")
            
            # Get database size
            result = conn.execute(text(
                "SELECT pg_size_pretty(pg_database_size(current_database()))"
            ))
            db_size = result.scalar()
            print(f"✅ Database size: {db_size}")
            
            # Get schema info
            result = conn.execute(text(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
            ))
            tables_count = result.scalar()
            print(f"✅ Number of tables: {tables_count}")
            
            if tables_count > 0:
                # List tables
                result = conn.execute(text(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                ))
                tables = [row[0] for row in result]
                print(f"✅ Tables in database: {', '.join(tables)}")
    except Exception as e:
        print(f"❌ Could not connect to database: {str(e)}")
        print("   Please check your credentials and ensure the database exists")
    
    # Step 3: Check environment information
    print("\n🔍 Step 3: System information...")
    print(f"✅ Operating System: {platform.system()} {platform.release()}")
    print(f"✅ Python Version: {sys.version.split()[0]}")
    try:
        import sqlalchemy
        print(f"✅ SQLAlchemy Version: {sqlalchemy.__version__}")
    except ImportError:
        print("❌ SQLAlchemy is not installed")
    
    try:
        import psycopg2
        print(f"✅ Psycopg2 Version: {psycopg2.__version__}")
    except ImportError:
        print("❌ Psycopg2 is not installed")
    
    # Step 4: Provide next steps
    print("\n📝 Next steps:")
    print("1. If all checks passed, your PostgreSQL setup is working correctly!")
    print("2. If there were connection issues, check the following:")
    print("   - PostgreSQL service is running")
    print("   - Credentials are correct")
    print("   - Firewall is not blocking connections")
    print("   - pg_hba.conf is configured to accept connections from this host")
    print(f"   - The '{db_name}' database exists")
    print("3. To check pg_hba.conf configuration, connect to PostgreSQL and run:")
    print("   SHOW hba_file;")
    print("   Then open that file and ensure it allows connections from your client")
    
    print("\n📌 Connection information used:")
    print(f"  - Database URL: postgresql://{db_user}:****@{db_host}:{db_port}/{db_name}")
    print(f"  - User: {db_user}")
    print(f"  - Host: {db_host}")
    print(f"  - Port: {db_port}")
    print(f"  - Database: {db_name}")
    print("=" * 40)

if __name__ == "__main__":
    check_postgres_connection() 