from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Base schema for question data validation
class QuestionBase(BaseModel):
    """Base question model containing common attributes shared across question schemas.
    
    Attributes:
        text (str): The actual question text to be presented to candidates
        trait_category (str): The personality trait category this question assesses
        difficulty (Optional[int]): Question difficulty level, defaults to 1
    """
    text: str
    trait_category: str
    difficulty: Optional[int] = 1

class QuestionCreate(QuestionBase):
    """Schema for creating a new question. Inherits all fields from QuestionBase."""
    pass

class QuestionResponse(QuestionBase):
    """Schema for returning question data in API responses.
    
    Extends QuestionBase with additional fields that represent question metadata.
    
    Attributes:
        id (int): Unique identifier for the question
        created_at (datetime): Timestamp when the question was created
    """
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True