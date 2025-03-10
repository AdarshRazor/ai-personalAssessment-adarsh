# Authentication and Authorization Routes
# This module handles user registration, login, and JWT token management

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, Token
from app.config import settings

router = APIRouter()

# OAuth2 password bearer scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

# JWT Configuration
# These settings control token generation and validation
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a new JWT access token with expiration time
    
    Args:
        data (dict): Payload data to encode in the token
        expires_delta (Optional[timedelta]): Custom expiration time, defaults to 15 minutes
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email and username validation
    
    Performs duplicate check before creating new user account
    """
    # Check if user already exists
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email or username already registered"
        )
    
    # Create new user with hashed password
    new_user = User(
        email=user.email,
        username=user.username
    )
    new_user.set_password(user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and generate access token
    
    Validates username/password and returns JWT token for authenticated requests
    """
    # Authenticate user credentials
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate access token with configured expiration
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Dependency to get current authenticated user from JWT token
    
    Validates token and returns user object for protected routes
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode and validate JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

@router.get("/users/me", response_model=UserResponse)
async def get_current_user_details(current_user: User = Depends(get_current_user)):
    """Get details of currently authenticated user
    
    Protected route that requires valid JWT token
    """
    return current_user