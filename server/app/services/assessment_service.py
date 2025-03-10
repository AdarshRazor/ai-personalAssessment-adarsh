from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.question import Question
from app.models.candidate import Candidate
from app.schemas.assessment import AssessmentCreate, ResponseSubmit, AssessmentResult
from app.services.openrouter_service import OpenRouterService
from typing import Dict, Any, List, Optional
import json

class AssessmentService:
    @staticmethod
    def create_assessment(db: Session, assessment: AssessmentCreate) -> Assessment:
        """Create a new assessment instance for a candidate
        
        Args:
            db: Database session
            assessment: Assessment creation data
            
        Returns:
            Assessment: Created assessment instance
            
        Raises:
            ValueError: If candidate not found
        """
        # Verify candidate exists
        candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
        if not candidate:
            raise ValueError(f"Candidate with ID {assessment.candidate_id} not found")
        
        # Initialize new assessment with default values
        db_assessment = Assessment(
            candidate_id=assessment.candidate_id,
            status="in_progress",
            responses={},
            result=None
        )
        db.add(db_assessment)
        db.commit()
        db.refresh(db_assessment)
        return db_assessment
    
    @staticmethod
    def get_assessment(db: Session, assessment_id: int) -> Optional[Assessment]:
        """Retrieve a specific assessment by ID
        
        Args:
            db: Database session
            assessment_id: ID of assessment to retrieve
            
        Returns:
            Optional[Assessment]: Assessment if found, None otherwise
        """
        return db.query(Assessment).filter(Assessment.id == assessment_id).first()

    @staticmethod
    def get_latest_assessment_by_user(db: Session, user_id: int) -> Optional[Assessment]:
        """Get the most recent assessment for a user
        
        Args:
            db: Database session
            user_id: User ID to find assessment for
            
        Returns:
            Optional[Assessment]: Most recent assessment if found, None otherwise
        """
        # Get the candidate associated with the user
        candidate = db.query(Candidate).filter(Candidate.user_id == user_id).first()
        if not candidate:
            return None
        
        # Get the latest assessment for the candidate
        latest_assessment = (
            db.query(Assessment)
            .filter(Assessment.candidate_id == candidate.id)
            .order_by(Assessment.id.desc())
            .first()
        )
        return latest_assessment

    @staticmethod
    def get_assessments_by_candidate(db: Session, candidate_id: int) -> List[Assessment]:
        """Get all assessments for a specific candidate
        
        Args:
            db: Database session
            candidate_id: Candidate ID to find assessments for
            
        Returns:
            List[Assessment]: List of all assessments for the candidate
        """
        return db.query(Assessment).filter(Assessment.candidate_id == candidate_id).all()
    
    @staticmethod
    async def submit_response(
        db: Session, 
        assessment_id: int, 
        response_data: ResponseSubmit,
        openrouter_service: OpenRouterService
    ) -> Assessment:
        """Submit and process a response for an assessment question
        
        Handles response submission, analysis, and personality profile generation
        when sufficient responses are collected.
        
        Args:
            db: Database session
            assessment_id: Assessment ID to submit response for
            response_data: Response submission data
            openrouter_service: Service for AI analysis
            
        Returns:
            Assessment: Updated assessment instance
            
        Raises:
            ValueError: If assessment or question not found
        """
        # Get the assessment
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if not assessment:
            raise ValueError(f"Assessment with ID {assessment_id} not found")
        
        # Get the question
        question = db.query(Question).filter(Question.id == response_data.question_id).first()
        if not question:
            raise ValueError(f"Question with ID {response_data.question_id} not found")
        
        # Update responses in the assessment
        responses = assessment.responses or {}
        responses[str(response_data.question_id)] = response_data.response_text
        assessment.responses = responses
        
        # If we have enough responses, analyze them
        if len(responses) >= 5:  # Minimum number of questions to provide a meaningful assessment
            assessment.status = "completed"
            
            # Analyze all responses
            analyses = {}
            for question_id, response_text in responses.items():
                question_obj = db.query(Question).filter(Question.id == int(question_id)).first()
                if question_obj:
                    analysis = await openrouter_service.analyze_response(
                        question_obj.text,
                        response_text,
                        question_obj.trait_category
                    )
                    analyses[question_obj.trait_category] = analysis
            
            # Generate personality profile
            profile = await openrouter_service.generate_personality_profile(analyses)
            assessment.result = profile
            
            # Update candidate's personality profile
            candidate = db.query(Candidate).filter(Candidate.id == assessment.candidate_id).first()
            if candidate:
                candidate.personality_profile = profile
        
        db.commit()
        db.refresh(assessment)
        return assessment