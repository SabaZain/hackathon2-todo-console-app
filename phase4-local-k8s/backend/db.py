from sqlmodel import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
import os
from typing import Generator


# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Check if running in production (Render or other production environment)
is_production = bool(os.getenv("RENDER")) or os.getenv("ENVIRONMENT") == "production" or os.getenv("ENV") == "production"

# Configure engine with SSL for production, no SSL changes for local development
if is_production:
    # Add SSL requirement for production environments like Render
    connect_args = {"sslmode": "require"}
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Set to True for SQL debugging
        connect_args=connect_args
    )
else:
    # No SSL changes for local development - maintain existing behavior
    engine = create_engine(
        DATABASE_URL,
        echo=True  # Set to True for SQL debugging
    )


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session for FastAPI endpoints.

    Yields a new database session for each request, ensuring proper cleanup
    after the request is completed.
    """
    with Session(engine) as session:
        yield session