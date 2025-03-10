from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import questions, assessments, candidates, auth

# Initialize FastAPI application with metadata
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# Configure CORS middleware to allow cross-origin requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(questions, prefix="/api/questions", tags=["questions"])
app.include_router(assessments, prefix="/api/assessments", tags=["assessments"])
app.include_router(candidates, prefix="/api/candidates", tags=["candidates"])
app.include_router(auth, prefix="/api/auth", tags=["auth"])

# Root endpoint to verify API is running
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Personality Assessment System API"}