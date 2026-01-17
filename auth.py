"""
Authentication & JWT Helper Functions Module

This module contains functions for implementing JWT-based authentication.
These functions handle token creation, verification, and user authentication
to secure the API endpoints and enforce user isolation.
"""

from fastapi import Request, HTTPException, Depends, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import Task  # We'll use this for type hints in ownership checks

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not JWT_SECRET:
    # For local development or build time, use a temporary secret
    # This allows the app to initialize during build/deployment
    # IMPORTANT: This is not secure for production - set BETTER_AUTH_SECRET in production
    import warnings
    warnings.warn("BETTER_AUTH_SECRET not set, using temporary secret. This is insecure for production!")
    JWT_SECRET = "temporary-secret-key-for-development-or-build"  # DO NOT USE IN PRODUCTION
JWT_ALGORITHM = "HS256"  # Algorithm used for signing tokens
JWT_EXPIRATION_MINUTES = 30  # Expiration time for tokens (in minutes)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password.

    Args:
        password: The plain text password to hash

    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
              (typically user information like user_id, email, etc.)
        expires_delta: Optional timedelta for token expiration (uses default if not provided)

    Returns:
        str: The encoded JWT token string
    """
    # Copy the data to avoid modifying the original
    to_encode = data.copy()

    # Set expiration time for the token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)

    # Add expiration time to the token data
    to_encode.update({"exp": expire})

    # Encode the data using JWT_SECRET and JWT_ALGORITHM
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """
    Verify a JWT token and return the decoded payload.

    Args:
        token: The JWT token string to verify

    Returns:
        dict: The decoded token payload containing user information,
              or None if the token is invalid
    """
    try:
        # Decode the token using the secret and algorithm
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

        # Extract user_id from the payload
        user_id: int = payload.get("user_id")

        # Check if user_id exists in the payload
        if user_id is None:
            return None

        return payload
    except JWTError:
        # Return None if there's an error decoding the token
        return None


security = HTTPBearer()


def get_current_user_id(credentials: HTTPAuthorizationCredentials = Security(security)) -> int:
    """
    Extract the current user's ID from the Authorization header.

    This function serves as a dependency that can be injected into route handlers
    to get the authenticated user's ID. It extracts the user ID from the
    JWT token in the Authorization header.

    Args:
        credentials: HTTP Authorization credentials containing the Bearer token

    Returns:
        int: The ID of the currently authenticated user

    Raises:
        HTTPException: With status code 401 if no user is authenticated
                      With status code 403 if access is forbidden
    """
    # Extract the token from the credentials
    token = credentials.credentials

    # Verify the token and decode the payload
    payload = verify_token(token)

    # Check if token is valid and contains user_id
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract user_id from the payload
    user_id: int = payload.get("user_id")

    # Check if user_id exists in the payload
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


def require_user_owns_task(task: Task, current_user_id: int = Depends(get_current_user_id)) -> int:
    """
    Dependency to ensure a user owns a specific task.

    This implements user isolation by checking that the authenticated user
    owns the task they're trying to access.

    Args:
        task: The task object to check ownership for
        current_user_id: The ID of the currently authenticated user (from JWT token)

    Returns:
        int: The current user's ID if they own the task

    Raises:
        HTTPException: With status code 403 if user doesn't own the task
    """
    # Check if the task's owner matches the authenticated user
    if task.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't own this task"
        )

    return current_user_id


# DEV NOTE: This bypass is for hackathon demo & local testing
# JWT auth will be restored later for production


# Example usage patterns for route protection:

# Example of how to protect an endpoint that requires authentication:
# @router.get("/protected-endpoint")
# def protected_endpoint(current_user_id: int = Security(get_current_user_id)):
#     """
#     Example of a protected endpoint that requires authentication.
#     The get_current_user_id dependency ensures the user is authenticated.
#     """
#     return {"message": f"Hello user {current_user_id}, you are authenticated!"}

# User Isolation & Authorization Guidance:
# - Always verify that the authenticated user can access the requested resource
# - Use the user ID from the JWT token to filter database queries
# - Return 403 Forbidden (or 404 to avoid revealing existence) if user doesn't own the resource
# - Implement role-based access control if needed for different user permissions
# - Log authentication attempts for security monitoring