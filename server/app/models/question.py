# Question Model Module
# This module defines the Question model for personality assessment questions

from sqlalchemy import Column, String, Text, Integer
from .base import BaseModel

class Question(BaseModel):
    """Question model for managing personality assessment questions
    
    This model stores questions used in candidate personality assessments. Each question
    is associated with a specific personality trait category and has a difficulty level
    to ensure balanced assessments.
    
    Attributes:
        text (str): The actual question text to be presented to candidates
        trait_category (str): Category of personality trait being assessed (e.g., 'extraversion')
        difficulty (int): Question difficulty rating on a 1-5 scale
    """
    __tablename__ = "questions"
    
    text = Column(Text, nullable=False)
    trait_category = Column(String, nullable=False)  # e.g., "extraversion", "openness"
    difficulty = Column(Integer, default=1)  # 1-5 scale