from pydantic import BaseModel, EmailStr
from typing import Optional

# Base schema for user authentication and authorization
class UserBase(BaseModel):
    """Base user model containing common attributes shared across user-related schemas.
    
    Attributes:
        username (str): Unique username for the user
        email (EmailStr): Valid email address of the user, validated by Pydantic
    """
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a new user account.
    
    Extends UserBase with password field for account creation.
    
    Attributes:
        password (str): User's password for authentication
    """
    password: str

class UserResponse(UserBase):
    """Schema for returning user data in API responses.
    
    Extends UserBase with additional fields that represent user state and permissions.
    
    Attributes:
        id (int): Unique identifier for the user
        is_active (bool): Flag indicating if the user account is active
        role (str): User's role for authorization purposes
    """
    id: int
    is_active: bool
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT authentication tokens.
    
    Attributes:
        access_token (str): The JWT access token string
        token_type (str): Type of the token (e.g., 'bearer')
    """
    access_token: str
    token_type: str