from sqlmodel import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
import os
from typing import Generator


# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine only if DATABASE_URL is available
if DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        echo=True  # Set to True for SQL debugging
    )
else:
    # For local development or build time, use a temporary in-memory database
    # This allows the app to initialize during build/deployment
    engine = create_engine("sqlite:///./temp.db", echo=True)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function that provides a database session for FastAPI endpoints.

    Yields a new database session for each request, ensuring proper cleanup
    after the request is completed.
    """
    with Session(engine) as session:
        yield session