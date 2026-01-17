from sqlmodel import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
import os
from typing import Generator


# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")


# Create the database engine
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