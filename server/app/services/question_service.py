# Question Service Module
# This module handles personality assessment question management and generation

from sqlalchemy.orm import Session
from app.models.question import Question
from app.schemas.question import QuestionCreate
from app.services.openrouter_service import OpenRouterService
from typing import List, Optional

class QuestionService:
    """Service class for managing personality assessment questions
    
    This class provides methods for creating, retrieving, and generating
    personality assessment questions. It works with the OpenRouter service
    to generate AI-powered behavioral questions for different personality traits.
    
    The service handles:
    - Question creation and storage
    - Retrieval by trait category
    - Automated question generation for personality traits
    - Question difficulty management
    
    All methods are implemented as static methods for stateless operation.
    """
    @staticmethod
    async def create_question(db: Session, question: QuestionCreate) -> Question:
        db_question = Question(
            text=question.text,
            trait_category=question.trait_category,
            difficulty=question.difficulty
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        return db_question
    
    @staticmethod
    def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
        return db.query(Question).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_questions_by_trait(db: Session, trait_category: str) -> List[Question]:
        return db.query(Question).filter(Question.trait_category == trait_category).all()
    
    @staticmethod
    async def generate_and_save_questions(db: Session, openrouter_service: OpenRouterService) -> List[Question]:
        """Generate questions for all major personality traits and save them to the database."""
        traits = [
            "openness", "conscientiousness", "extraversion", 
            "agreeableness", "neuroticism"
        ]
        
        all_questions = []
        
        for trait in traits:
            questions_text = await openrouter_service.generate_questions(trait, count=3)
            
            for text in questions_text:
                question = QuestionCreate(
                    text=text,
                    trait_category=trait,
                    difficulty=2  # Default medium difficulty
                )
                db_question = await QuestionService.create_question(db, question)
                all_questions.append(db_question)
        
        return all_questions