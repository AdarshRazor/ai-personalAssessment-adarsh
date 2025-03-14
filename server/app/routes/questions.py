# Question Management Routes
# This module handles personality assessment question creation and retrieval

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.question import QuestionCreate, QuestionResponse
from app.services.question_service import QuestionService
from app.services.openrouter_service import OpenRouterService
from app.config import settings
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

# Dependency to get OpenRouter service instance
def get_openrouter_service():
    return OpenRouterService()

@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    question: QuestionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new personality assessment question
    
    Args:
        question: Question creation data
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        QuestionResponse: Created question
    """
    return await QuestionService.create_question(db, question)

@router.get("/", response_model=List[QuestionResponse])
async def read_questions(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a paginated list of all questions
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        List[QuestionResponse]: List of questions
    """
    questions = QuestionService.get_questions(db, skip=skip, limit=limit)
    return questions

@router.get("/trait/{trait_category}", response_model=List[QuestionResponse])
async def read_questions_by_trait(
    trait_category: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve questions filtered by personality trait category
    
    Args:
        trait_category: Category of personality trait to filter by
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        List[QuestionResponse]: List of questions for the specified trait
    """
    questions = QuestionService.get_questions_by_trait(db, trait_category)
    return questions

@router.post("/generate", response_model=List[QuestionResponse], status_code=status.HTTP_201_CREATED)
async def generate_questions(
    db: Session = Depends(get_db),
    openrouter_service: OpenRouterService = Depends(get_openrouter_service),
    current_user: User = Depends(get_current_user)
):
    """Generate standard questions for all personality traits using AI
    
    Args:
        db: Database session
        openrouter_service: Service for AI-powered question generation
        current_user: Authenticated user making the request
        
    Returns:
        List[QuestionResponse]: List of generated questions
        
    Raises:
        HTTPException: If OpenRouter API is not configured
    """
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="OpenRouter API key not configured"
        )
    
    questions = await QuestionService.generate_and_save_questions(db, openrouter_service)
    return questions