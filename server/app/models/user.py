# User Model Module
# This module defines the User model for authentication and authorization

from sqlalchemy import Column, String, Boolean
from passlib.hash import bcrypt
from .base import BaseModel

class User(BaseModel):
    """User model for managing authentication and user roles
    
    This model handles user authentication, password management, and role-based access control.
    It extends the BaseModel to include common fields like id and timestamps.
    
    Attributes:
        username (str): Unique username for identification
        email (str): Unique email address for communication
        password_hash (str): Securely hashed password using bcrypt
        is_active (bool): Flag indicating if the user account is active
        role (str): User role for authorization ('admin' or 'user')
    """
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Can be 'admin' or 'user'
    
    def set_password(self, password: str):
        """Hash and set the user's password using bcrypt
        
        Args:
            password: Plain text password to be hashed
        """
        self.password_hash = bcrypt.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.verify(password, self.password_hash)