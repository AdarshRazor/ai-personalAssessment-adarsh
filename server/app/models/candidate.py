from sqlalchemy import Column, String, JSON
from .base import BaseModel

class Candidate(BaseModel):
    __tablename__ = "candidates"
    
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    personality_profile = Column(JSON, nullable=True)  # Stores the final personality profile