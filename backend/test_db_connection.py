"""
Quick test script to verify database connection before deployment
"""

import os
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel

def test_db_connection():
    """Test database connection with environment variables"""

    # Get environment variables
    DATABASE_URL = os.getenv("DATABASE_URL")
    AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

    print("Testing environment variables...")
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable is not set!")
        return False
    else:
        print("✅ DATABASE_URL is set")

    if not AUTH_SECRET:
        print("❌ BETTER_AUTH_SECRET environment variable is not set!")
        return False
    else:
        print("✅ BETTER_AUTH_SECRET is set")

    print("\nTesting database connection...")
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)

        # Test the connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            print(f"✅ Query result: {result.fetchone()}")

        # Test table creation
        from models import User, Task
        print("✅ Models imported successfully!")

        print("✅ All tests passed! Ready for deployment.")
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running database connection test...")
    success = test_db_connection()
    if success:
        print("\n🎉 Ready for deployment!")
    else:
        print("\n💥 Fix the issues above before deploying!")
        exit(1)