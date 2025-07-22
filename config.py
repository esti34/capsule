"""
Configuration file for database settings
Instead of using .env files, you can modify this file directly
"""

# PostgreSQL Database Configuration
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "hacaton_db"

# Function to set environment variables
def set_env_vars():
    import os
    os.environ["DB_USER"] = DB_USER
    os.environ["DB_PASSWORD"] = DB_PASSWORD
    os.environ["DB_HOST"] = DB_HOST
    os.environ["DB_PORT"] = DB_PORT
    os.environ["DB_NAME"] = DB_NAME 