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

### Reqiurements / Dependencies: `requirements.txt`

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