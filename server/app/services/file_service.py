import os
from pathlib import Path
from fastapi import UploadFile
from datetime import datetime

class FileService:
    UPLOAD_DIR = Path("uploads/resumes")

    @classmethod
    async def save_resume(cls, file: UploadFile, candidate_id: int) -> str:
        """Save a resume file and return its path"""
        # Create upload directory if it doesn't exist
        os.makedirs(cls.UPLOAD_DIR, exist_ok=True)

        # Generate unique filename using timestamp and candidate_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"resume_{candidate_id}_{timestamp}.pdf"
        file_path = cls.UPLOAD_DIR / filename

        # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Return the relative path to be stored in the database
        return str(file_path)

    @classmethod
    def delete_resume(cls, file_path: str) -> bool:
        """Delete a resume file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False