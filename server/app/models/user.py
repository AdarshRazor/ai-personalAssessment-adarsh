from sqlalchemy import Column, String, Boolean
from passlib.hash import bcrypt
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # Can be 'admin' or 'user'
    
    def set_password(self, password: str):
        self.password_hash = bcrypt.hash(password)
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)