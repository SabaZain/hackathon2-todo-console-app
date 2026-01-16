from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel
from db import get_session
from models import User
from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    get_current_user_id
)

router = APIRouter()

class UserCreate(BaseModel):
    """
    Schema for user registration request.

    Fields:
    - email: string, user's email address
    - password: string, user's plaintext password
    """
    email: str
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login request.

    Fields:
    - email: string, user's email address
    - password: string, user's plaintext password
    """
    email: str
    password: str


class TokenResponse(BaseModel):
    """
    Schema for authentication token response.

    Fields:
    - access_token: string, JWT access token
    - token_type: string, type of token (usually "bearer")
    - user_id: int, ID of the authenticated user
    """
    access_token: str
    token_type: str = "bearer"
    user_id: int


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user account.

    Args:
        user_data: User registration data (email and password)
        session: Database session dependency

    Returns:
        TokenResponse containing the access token and user ID

    HTTP Status Codes:
    - 201: Created - User successfully registered
    - 400: Bad Request - Invalid user data or email already exists
    - 401: Unauthorized - Invalid registration attempt
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate email format (basic validation)
    if "@" not in user_data.email or "." not in user_data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    # Validate password length
    if len(user_data.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters long"
        )

    # Create new user with hashed password
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )

    # Add user to database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Create JWT access token with user ID
    token_data = {"user_id": new_user.id}
    access_token = create_access_token(data=token_data)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=new_user.id
    )


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.

    Args:
        login_data: User login credentials (email and password)
        session: Database session dependency

    Returns:
        TokenResponse containing the access token and user ID

    HTTP Status Codes:
    - 200: Success - Login successful
    - 400: Bad Request - Invalid login data
    - 401: Unauthorized - Invalid credentials
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == login_data.email)).first()

    # Check if user exists and password is correct
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT access token with user ID
    token_data = {"user_id": user.id}
    access_token = create_access_token(data=token_data)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id
    )


@router.get("/me", response_model=User)
def get_current_user(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Get current authenticated user's information.

    Args:
        user_id: The current user's ID (obtained from JWT token)
        session: Database session dependency

    Returns:
        User object with user information

    HTTP Status Codes:
    - 200: Success - User information returned
    - 401: Unauthorized - Invalid authentication
    - 404: Not Found - User not found
    """
    # Get user from database using the authenticated user ID
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user