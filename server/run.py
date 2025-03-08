import uvicorn
from app.main import app
from app.init_db import init_db

if __name__ == "__main__":
    # Initialize database tables
    init_db()
    
    # Run application
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)