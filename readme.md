# AI-Powered Personality Assessment System

## File Structure

```
personality-assessment-system/
│
├── server/                      # Flask/FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration settings
│   │   ├── models/              # Database models
│   │   ├── routes/              # API endpoints
│   │   ├── services/            # Business logic
│   │   └── utils/               # Helper functions
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables (git-ignored)
│
├── client/                      # React frontend
│   ├── public/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API services
│   │   ├── context/             # React context
│   │   ├── hooks/               # Custom React hooks
│   │   └── utils/               # Helper functions
│   ├── package.json             # Node dependencies
│   └── .env                     # Environment variables (git-ignored)
│
└── README.md                    # Project documentation
```

## Backend Development

### Python Virtual Env.

```bash
cd server
python -m venv venv ## install a basic env.

# Activate virtual environment
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
```

### Requirements / Dependencies: `requirements.txt`

```txt
fastapi==0.104.0
uvicorn==0.23.2
pydantic==2.4.2
python-dotenv==1.0.0
httpx==0.25.0
sqlalchemy==2.0.22
psycopg2-binary==2.9.9  # For PostgreSQL
openai==1.2.0           # For OpenRouter API integration
pytest==7.4.3           # For testing
```

#### Install dependencies

```bash
pip install -r requirements.txt
<path>\python.exe -m pip install --upgrade pip
# or
python.exe -m pip install --upgrade pip
```

## Project Components Documentation

### Server-side Components

#### Routes
- `auth.py` - Handles user authentication, registration, and JWT token management
- `assessments.py` - Manages assessment creation, response submission, and result retrieval
- `candidate.py` - Handles candidate profile creation and retrieval operations
- `questions.py` - Manages personality assessment question creation and retrieval

#### Services
- `assessment_service.py` - Core business logic for assessment processing and analysis
- `candidate_service.py` - Handles candidate data management and profile operations
- `question_service.py` - Manages question generation and retrieval operations
- `openrouter_service.py` - Integrates with OpenRouter API for AI-powered analysis

#### Models
- `assessment.py` - Database model for personality assessments
- `candidate.py` - Database model for candidate profiles
- `question.py` - Database model for assessment questions
- `user.py` - Database model for user authentication and profiles

#### Schemas
- `assessment.py` - Pydantic schemas for assessment request/response validation
- `auth.py` - Schemas for authentication and user data validation
- `candidate.py` - Schemas for candidate profile data validation
- `question.py` - Schemas for question data validation

### Configuration and Setup
- `config.py` - Application configuration settings and environment variables
- `database.py` - Database connection and session management
- `main.py` - FastAPI application initialization and route registration
- `init_db.py` - Database initialization and table creation

### Client-side Components

#### Core Components
- `components/` - Reusable UI components for the assessment interface
- `pages/` - Page components for different sections of the application
- `services/` - API integration services for backend communication
- `context/` - React context providers for state management
- `hooks/` - Custom React hooks for shared functionality
- `utils/` - Helper functions and utility modules

#### Configuration Files
- `package.json` - Node.js dependencies and project configuration
- `tsconfig.json` - TypeScript configuration settings
- `tailwind.config.ts` - Tailwind CSS styling configuration
- `components.json` - UI component configuration

## Progress

- Implemented a `ROBUST` bacnend.
- Configured Frontend: NextJS, TypeScript, Tailwind
    - Implemented Registration, Login, JWT Authentication and Cookie feature
    - Implemented Candidate Profile Dashboardd
    - Implemented Assessment page to start the user assessment.
    - Analysis of CV using openRouter and provide score (working ...)

## Important Notes

- Keep all `__init__.py` files intact as they are essential for Python package structure
- Ensure environment variables are properly configured in `.env` files