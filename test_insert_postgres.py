import requests
import json
import psycopg2
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def test_api_insertion():
    """Test inserting data via the FastAPI endpoint and verify it's in PostgreSQL"""
    
    print("\n🧪 TESTING DATA INSERTION TO POSTGRESQL")
    print("=" * 50)
    
    api_base_url = "http://localhost:8000"
    
    # Step 1: Create a test user via API
    print("\n📝 Step 1: Creating test user via API...")
    test_user = {
        "email": "test_postgres@example.com",
        "username": "postgres_tester",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(
            f"{api_base_url}/api/users/",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_user)
        )
        
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data["id"]
            print(f"✅ User created successfully via API with ID: {user_id}")
            print(f"✅ API response: {json.dumps(user_data, indent=2)}")
        else:
            print(f"❌ Failed to create user. Status code: {response.status_code}")
            print(f"❌ Error message: {response.text}")
            if response.status_code == 400 and "Email already registered" in response.text:
                print("⚠️ Note: This user might already exist in the database")
    except Exception as e:
        print(f"❌ Exception when calling API: {str(e)}")
        print("⚠️ Make sure the API server is running (python run_backend.py)")
    
    # Step 2: Create a test item for the user
    print("\n📝 Step 2: Creating test item via API...")
    
    # Try to get user ID if we don't have it
    if 'user_id' not in locals():
        try:
            response = requests.get(f"{api_base_url}/api/users/")
            users = response.json()
            for user in users:
                if user["email"] == test_user["email"]:
                    user_id = user["id"]
                    print(f"✅ Found existing user with ID: {user_id}")
                    break
        except Exception as e:
            print(f"❌ Exception when fetching users: {str(e)}")
    
    if 'user_id' in locals():
        test_item = {
            "name": "PostgreSQL Test Item",
            "description": "This item is used to test PostgreSQL insertion"
        }
        
        try:
            response = requests.post(
                f"{api_base_url}/api/users/{user_id}/items/",
                headers={"Content-Type": "application/json"},
                data=json.dumps(test_item)
            )
            
            if response.status_code == 200:
                item_data = response.json()
                item_id = item_data["id"]
                print(f"✅ Item created successfully via API with ID: {item_id}")
                print(f"✅ API response: {json.dumps(item_data, indent=2)}")
            else:
                print(f"❌ Failed to create item. Status code: {response.status_code}")
                print(f"❌ Error message: {response.text}")
        except Exception as e:
            print(f"❌ Exception when creating item: {str(e)}")
    
    # Step 3: Directly verify data in PostgreSQL
    print("\n📝 Step 3: Directly querying PostgreSQL to verify data...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        
        cursor = conn.cursor()
        
        # Query for the user
        cursor.execute("SELECT id, email, username FROM users WHERE email = %s", 
                       (test_user["email"],))
        user_result = cursor.fetchone()
        
        if user_result:
            print(f"✅ POSTGRESQL VERIFICATION: User found in PostgreSQL database!")
            print(f"   ID: {user_result[0]}, Email: {user_result[1]}, Username: {user_result[2]}")
            
            # Query for items belonging to this user
            cursor.execute("SELECT id, name, description FROM items WHERE owner_id = %s", 
                           (user_result[0],))
            item_results = cursor.fetchall()
            
            if item_results:
                print(f"✅ POSTGRESQL VERIFICATION: Found {len(item_results)} items for this user:")
                for item in item_results:
                    print(f"   ID: {item[0]}, Name: {item[1]}, Description: {item[2]}")
            else:
                print("❌ No items found for this user in PostgreSQL")
        else:
            print("❌ User not found in PostgreSQL database")
            
        # Check if SQLite file exists
        import os
        if os.path.exists("sql_app.db"):
            print("\n⚠️ WARNING: SQLite database file (sql_app.db) still exists!")
            print("   But your application is now using PostgreSQL.")
        else:
            print("\n✅ No SQLite database file found - you're fully on PostgreSQL!")
            
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Exception when querying PostgreSQL: {str(e)}")
    
    print("\n✅ TEST COMPLETED")
    print("=" * 50)

if __name__ == "__main__":
    # Set environment variables from config
    from config import set_env_vars
    set_env_vars()
    
    # Run the test
    test_api_insertion() 