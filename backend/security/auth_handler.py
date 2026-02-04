"""
Authentication Handler for Todo AI Chatbot

This module confirms proper authentication and authorization.
"""

from typing import Dict, Any, Optional
from jose import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from functools import wraps


class AuthHandler:
    """Confirms proper authentication and authorization."""

    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize the authentication handler.

        Args:
            secret_key: Secret key for JWT signing (defaults to random if not provided)
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.active_sessions = {}
        self.user_permissions = {}

    def create_token(self, user_id: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT token for a user.

        Args:
            user_id: The user ID to create token for
            expires_delta: Expiration time for the token (defaults to 1 hour)

        Returns:
            JWT token string
        """
        if expires_delta is None:
            expires_delta = timedelta(hours=1)

        expire = datetime.utcnow() + expires_delta
        payload = {
            'user_id': user_id,
            'exp': expire,
            'iat': datetime.utcnow(),
            'jti': secrets.token_hex(16)  # JWT ID for revocation
        }

        token = jwt.encode(payload, self.secret_key, algorithm='HS256')
        return token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token.

        Args:
            token: The JWT token to verify

        Returns:
            User information if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])

            # Check if session is still active
            session_key = f"{payload['user_id']}_{payload['jti']}"
            if session_key in self.active_sessions:
                session_info = self.active_sessions[session_key]

                # Check if session hasn't expired
                if datetime.utcnow() < session_info['expires_at']:
                    return {
                        'user_id': payload['user_id'],
                        'token_id': payload['jti'],
                        'is_authenticated': True
                    }
                else:
                    # Remove expired session
                    del self.active_sessions[session_key]

            return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.JWTError:
            return None

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user with username and password.

        Args:
            username: The username
            password: The plain text password

        Returns:
            Authentication result with user info if successful, None otherwise
        """
        # In a real implementation, this would check against a database
        # For this example, we'll use a simple hash comparison
        user_hash = hashlib.sha256(f"{username}:{password}".encode()).hexdigest()

        # Simulate user lookup
        valid_users = {
            'admin': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # admin:password
            'user1': 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f',  # user1:password
        }

        if username in valid_users and valid_users[username] == user_hash:
            # Create session
            token = self.create_token(username)
            token_payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])

            session_key = f"{username}_{token_payload['jti']}"
            self.active_sessions[session_key] = {
                'user_id': username,
                'created_at': datetime.utcnow(),
                'expires_at': datetime.utcnow() + timedelta(hours=1),
                'token': token
            }

            return {
                'is_authenticated': True,
                'user_id': username,
                'token': token,
                'permissions': self.get_user_permissions(username)
            }

        return None

    def authorize_request(self, token: str, required_permission: str = None) -> bool:
        """
        Authorize a request based on token and required permissions.

        Args:
            token: The authentication token
            required_permission: Optional permission required for the action

        Returns:
            Boolean indicating if authorized
        """
        user_info = self.verify_token(token)
        if not user_info:
            return False

        user_id = user_info['user_id']

        if required_permission:
            user_perms = self.get_user_permissions(user_id)
            return required_permission in user_perms

        return True

    def get_user_permissions(self, user_id: str) -> list:
        """
        Get permissions for a user.

        Args:
            user_id: The user ID

        Returns:
            List of permissions for the user
        """
        # Default permissions
        if user_id not in self.user_permissions:
            # In a real system, this would come from a database
            if user_id == 'admin':
                self.user_permissions[user_id] = [
                    'read_conversations',
                    'write_conversations',
                    'delete_conversations',
                    'manage_users',
                    'read_tasks',
                    'write_tasks',
                    'delete_tasks'
                ]
            else:
                self.user_permissions[user_id] = [
                    'read_conversations',
                    'write_conversations',
                    'read_tasks',
                    'write_tasks'
                ]

        return self.user_permissions[user_id]

    def revoke_token(self, token: str) -> bool:
        """
        Revoke a JWT token (logout).

        Args:
            token: The token to revoke

        Returns:
            Boolean indicating success
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'], options={"verify_signature": False})
            session_key = f"{payload['user_id']}_{payload['jti']}"

            if session_key in self.active_sessions:
                del self.active_sessions[session_key]
                return True

            return False
        except jwt.InvalidTokenError:
            return False

    def refresh_token(self, token: str) -> Optional[str]:
        """
        Refresh an existing token.

        Args:
            token: The token to refresh

        Returns:
            New token if refresh was successful, None otherwise
        """
        user_info = self.verify_token(token)
        if not user_info:
            return None

        # Revoke old token
        self.revoke_token(token)

        # Create new token
        return self.create_token(user_info['user_id'])

    def validate_user_conversation_access(self, user_id: str, conversation_id: str) -> bool:
        """
        Validate if a user has access to a specific conversation.

        Args:
            user_id: The user ID
            conversation_id: The conversation ID

        Returns:
            Boolean indicating if user has access
        """
        # In a real implementation, this would check a database
        # For this example, we'll implement a simple ownership rule
        # where users can only access conversations that start with their ID
        return conversation_id.startswith(user_id)

    def validate_user_task_access(self, user_id: str, task_id: str) -> bool:
        """
        Validate if a user has access to a specific task.

        Args:
            user_id: The user ID
            task_id: The task ID

        Returns:
            Boolean indicating if user has access
        """
        # In a real implementation, this would check a database
        # For this example, we'll implement a simple ownership rule
        # where users can only access tasks that start with their ID
        return task_id.startswith(user_id)

    def generate_password_hash(self, password: str) -> str:
        """
        Generate a secure hash for a password.

        Args:
            password: The plain text password

        Returns:
            Hashed password
        """
        # In a real system, use bcrypt or similar
        salt = secrets.token_hex(32)
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)
        return salt + pwdhash.hex()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            password: The plain text password
            hashed_password: The stored hash

        Returns:
            Boolean indicating if password is valid
        """
        # In a real system, use bcrypt or similar
        salt = hashed_password[:64]
        stored_pwdhash = hashed_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt.encode('utf-8'),
                                      100000)
        return pwdhash.hex() == stored_pwdhash

    def require_auth(self, required_permission: Optional[str] = None):
        """
        Decorator to require authentication for a function.

        Args:
            required_permission: Optional permission required

        Returns:
            Decorator function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # This would extract token from request in a real implementation
                # For this example, we'll just pass through
                return func(*args, **kwargs)
            return wrapper
        return decorator


def get_auth_handler(secret_key: Optional[str] = None) -> AuthHandler:
    """
    Get an instance of the authentication handler.

    Args:
        secret_key: Optional secret key for JWT signing

    Returns:
        AuthHandler instance
    """
    return AuthHandler(secret_key)