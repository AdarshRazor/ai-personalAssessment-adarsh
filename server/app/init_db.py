from sqlalchemy import create_engine
from app.config import settings
from app.models.base import Base
from app.models import Candidate, Question, Assessment

def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

if __name__ == "__main__":
    init_db()