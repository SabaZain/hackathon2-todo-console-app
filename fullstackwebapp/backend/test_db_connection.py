import os
from sqlalchemy import create_engine, text
from sqlmodel import SQLModel, create_engine

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_kLl6eaUMti8Y@ep-snowy-mode-a7iblijc-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
os.environ['BETTER_AUTH_SECRET'] = '40eadf4650eaebe5c18941aaf176e84e99666577a61f246e19e1e7dd4bc544da'

print("Testing database connection...")

try:
    DATABASE_URL = os.getenv("DATABASE_URL")
    print(f"Database URL: {DATABASE_URL[:50]}...")

    # Create engine
    engine = create_engine(DATABASE_URL)

    # Test the connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        print(f"Query result: {result.fetchone()}")

    # Test table creation
    from models import User, Task
    print("Testing table creation...")
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created successfully!")

except Exception as e:
    print(f"Database connection failed: {e}")
    import traceback
    traceback.print_exc()