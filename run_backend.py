import uvicorn
from config import set_env_vars
import sys

if __name__ == "__main__":
    # Set environment variables from config.py
    set_env_vars()
    
    print("\n🔄 Starting FastAPI application with PostgreSQL database...")
    print("💡 To verify your PostgreSQL connection first, run: python verify_postgres.py")
    
    try:
        # Run the FastAPI application
        uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(f"\n❌ Error starting server: {str(e)}")
        print("Make sure PostgreSQL is installed and running with the correct credentials")
        sys.exit(1) 