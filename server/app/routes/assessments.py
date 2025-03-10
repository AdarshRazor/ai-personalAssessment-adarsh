# Assessment Management Routes
# This module handles assessment creation, response submission, and result retrieval

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from app.database import get_db
from app.schemas.assessment import (
    AssessmentCreate, 
    AssessmentResponse, 
    ResponseSubmit,
    AssessmentResult
)
from app.services.assessment_service import AssessmentService
from app.services.openrouter_service import OpenRouterService
from app.config import settings
from app.routes.auth import get_current_user
from app.models.user import User

router = APIRouter()

# Dependency to get OpenRouter service instance
def get_openrouter_service():
    """Create and return a new OpenRouter service instance for AI analysis"""
    return OpenRouterService()

@router.post("/upload-resume")
async def upload_resume(
    resume: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Handle resume file upload for assessment
    
    Args:
        resume: PDF file to be uploaded
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        dict: Contains uploaded filename, file path, and associated assessment ID
        
    Raises:
        HTTPException: If file is missing, not PDF, or upload fails
    """
    if not resume:
        raise HTTPException(status_code=400, detail="No file uploaded")
    
    if not resume.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = os.path.join("uploads", "resumes")
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the file with user-specific filename
        file_path = os.path.join(upload_dir, f"{current_user.id}_{resume.filename}")
        with open(file_path, "wb") as buffer:
            content = await resume.read()
            buffer.write(content)
        
        # Update assessment record with resume path
        assessment = AssessmentService.get_latest_assessment_by_user(db, current_user.id)
        if assessment:
            assessment.resume_file_path = file_path
            db.commit()
            db.refresh(assessment)
        
        return {"filename": resume.filename, "file_path": file_path, "assessment_id": assessment.id if assessment else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: AssessmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new assessment for a candidate
    
    Args:
        assessment: Assessment creation data
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        AssessmentResponse: Created assessment instance
        
    Raises:
        HTTPException: If validation fails or candidate not found
    """
    try:
        return AssessmentService.create_assessment(db, assessment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/current", response_model=AssessmentResponse)
async def get_current_assessment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the most recent assessment for the current user
    
    Args:
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        AssessmentResponse: Most recent assessment for the user
        
    Raises:
        HTTPException: If no assessment found or other errors occur
    """
    try:
        assessment = AssessmentService.get_latest_assessment_by_user(db, current_user.id)
        if assessment is None:
            raise HTTPException(
                status_code=404,
                detail="No assessment found for current user"
            )
        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def read_assessment(
    assessment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve a specific assessment by ID
    
    Args:
        assessment_id: ID of the assessment to retrieve
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        AssessmentResponse: Assessment details if found
        
    Raises:
        HTTPException: If assessment not found
    """
    assessment = AssessmentService.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment

@router.get("/candidate/{candidate_id}", response_model=List[AssessmentResponse])
async def read_candidate_assessments(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all assessments for a specific candidate
    
    Args:
        candidate_id: ID of the candidate
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        List[AssessmentResponse]: List of all assessments for the candidate
    """
    assessments = AssessmentService.get_assessments_by_candidate(db, candidate_id)
    return assessments

@router.post("/{assessment_id}/submit", response_model=AssessmentResponse)
async def submit_response(
    assessment_id: int,
    response_data: ResponseSubmit,
    db: Session = Depends(get_db),
    openrouter_service: OpenRouterService = Depends(get_openrouter_service),
    current_user: User = Depends(get_current_user)
):
    """Submit a response for an assessment question
    
    Args:
        assessment_id: ID of the assessment
        response_data: Response submission data
        db: Database session
        openrouter_service: Service for AI analysis
        current_user: Authenticated user making the request
        
    Returns:
        AssessmentResponse: Updated assessment with submitted response
        
    Raises:
        HTTPException: If OpenRouter API not configured or validation fails
    """
    if not settings.OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="OpenRouter API key not configured"
        )
    
    try:
        return await AssessmentService.submit_response(
            db, 
            assessment_id, 
            response_data,
            openrouter_service
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{assessment_id}/result", response_model=AssessmentResult)
async def get_assessment_result(
    assessment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve the final results of a completed assessment
    
    Args:
        assessment_id: ID of the assessment
        db: Database session
        current_user: Authenticated user making the request
        
    Returns:
        AssessmentResult: Final assessment results and personality profile
        
    Raises:
        HTTPException: If assessment not found or not complete
    """
    assessment = AssessmentService.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status != "completed" or not assessment.result:
        raise HTTPException(
            status_code=400, 
            detail="Assessment is not complete or results are not available"
        )
    
    return assessment.result