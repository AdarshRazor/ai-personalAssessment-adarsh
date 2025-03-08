from sqlalchemy import Column, String, Text, Integer
from .base import BaseModel

class Question(BaseModel):
    __tablename__ = "questions"
    
    text = Column(Text, nullable=False)
    trait_category = Column(String, nullable=False)  # e.g., "extraversion", "openness"
    difficulty = Column(Integer, default=1)  # 1-5 scale