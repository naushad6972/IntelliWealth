IntelliWealth - Financial Intelligence Agent

Production-Ready Full-Stack AI Personal Finance Management Platform built with React, FastAPI, SQLAlchemy, Scikit-Learn, and Google Gemini API.

🌟 Key Features
Authentication & Profile:

Register, Login, JWT Token authentication, bcrypt password hashing.
User Financial Profile (Income, occupation, risk preference, goals, currency).
Bank Integration:

Bank Connect Simulator (HDFC, ICICI, SBI, Axis, Chase).
Auto & Manual sync with last sync timestamp logs.
Bank Statement CSV Uploader (supports HDFC, ICICI, SBI, Chase & custom schemas).
Transaction Management & AI Auto-Categorization:

Multi-stage transaction categorizer (Rule engine -> Scikit-learn Random Forest ML -> LLM fallback).
Search, filter by category/type, sort by date/amount, pagination.
Executive Dashboard & Analytics:

Total Income, Expense, Net Savings, Bank Balance cards.
Monthly Cash Flow trend AreaChart & Category PieChart.
Weekend spending surge detector, top merchants, recurring subscriptions finder.
Budget & Goal Planners:

Monthly and category budgets with overspending warning alerts.
Financial goal tracking (Emergency Fund, Vacation, Car, Home) with AI monthly savings calculator.
Machine Learning Spending Forecast:

Time-series linear regression models projecting next month spending and cash flow trends.
Financial Health Score (0–100):

6-pillar algorithm evaluating savings rate, emergency fund coverage, budget discipline, debt ratio, income stability, and investment habits.
EMI & Loan Repayment Calculator:

Interactive sliders for principal, interest rate, tenure + repayment amortization schedule.
Investment Education & AI Coach:

Modules for SIP, Mutual Funds, Stocks, ETFs, Emergency Fund, Tax Saving.
Tailored non-personalized educational AI advice generator based on user financial profile.
AI Financial Assistant Chatbot:

Context-aware chatbot answering questions like "How much did I spend on food?", "How can I save ₹5,000?", "Explain SIP".
Reports Generator:

Instant PDF executive report (ReportLab) & CSV raw ledger export.
🚀 Quickstart Guide
Option 1: Running Locally (FastAPI + React Vite)
1. Backend Setup
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
python seed.py # Seed realistic mock data
uvicorn app.main:app --reload --port 8000
Backend API will be running at http://localhost:8000 (API documentation at http://localhost:8000/docs).

2. Frontend Setup
cd frontend
npm install
npm run dev
Frontend Web Application will be available at http://localhost:3000.

Demo Login Credentials:

Email: demo@intelliwealth.ai
Password: password123
Option 2: Docker Compose Setup
docker-compose up --build
Frontend: http://localhost:3000
Backend API: http://localhost:8000
PostgreSQL: localhost:5432
🛠️ Architecture & Tech Stack
IntelliWealth/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # RESTful FastAPI Endpoints
│   │   ├── core/           # Security & Configuration
│   │   ├── db/             # SQLAlchemy Database Engine
│   │   ├── models/         # Database Models (User, Transaction, Bank, Budget, Goal, etc.)
│   │   ├── schemas/        # Pydantic DTOs & Request Validation
│   │   ├── ml/             # ML Categorizer, Forecaster, Health Score, Insights Engine
│   │   ├── ai/             # AI Chatbot Handler & Gemini Integration
│   │   └── services/       # PDF/CSV Report Generation
│   ├── main.py             # FastAPI App Entrypoint
│   ├── seed.py             # Seed Data Generator
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/            # Axios API Client
│   │   ├── components/     # Navbar, Sidebar, StatCard, Modals, AIChatWidget
│   │   ├── context/        # Auth Context Provider
│   │   ├── pages/          # Dashboard, Transactions, Analytics, Budget, Health Score, etc.
│   │   ├── App.jsx         # Router & App Layout
│   │   └── index.css       # Tailwind CSS & Glassmorphism Design Tokens
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── .env.example
└── README.md
🌐 Deployment Instructions
Frontend (Vercel): Connect repository, set build command npm run build, output directory dist.
Backend (Render/Railway): Deploy as a Python web service, set start command uvicorn app.main:app --host 0.0.0.0 --port $PORT. Set environment variables DATABASE_URL (PostgreSQL) and SECRET_KEY. =======
IntelliWealth
IntelliWealth is an AI-powered personal financial intelligence platform that analyzes spending patterns, provides smart budgeting and savings recommendations, predicts future financial trends, and empowers users to make informed financial decisions.
