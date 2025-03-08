from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

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

# Dependency to get OpenRouter service
def get_openrouter_service():
    return OpenRouterService()

@router.post("/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assessment(
    assessment: AssessmentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return AssessmentService.create_assessment(db, assessment)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def read_assessment(
    assessment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
    assessment = AssessmentService.get_assessment(db, assessment_id)
    if assessment is None:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if assessment.status != "completed" or not assessment.result:
        raise HTTPException(
            status_code=400, 
            detail="Assessment is not complete or results are not available"
        )
    
    return assessment.result