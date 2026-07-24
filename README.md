# 💰 IntelliWealth – AI Financial Intelligence Agent

IntelliWealth is an AI-powered Personal Finance Management platform that helps users manage their finances intelligently. It provides expense tracking, budget planning, financial analytics, AI-powered insights, spending forecasts, investment education, and an intelligent chatbot for personalized financial assistance.

---

## 🚀 Features

### 🔐 Authentication
- JWT-based Secure Authentication
- User Registration & Login
- Password Hashing using Bcrypt
- User Profile Management

### 📊 Executive Dashboard
- Financial Summary
- Income vs Expense Analysis
- Savings Overview
- Monthly Cash Flow Charts
- Recent Transactions
- AI Financial Insights

### 💳 Transaction Management
- Add, Edit & Delete Transactions
- AI-Based Transaction Categorization
- Search & Filter Transactions
- Expense Categorization
- Merchant Tracking

### 🏦 Bank Integration
- Multi-Bank Account Support
- Open Banking Architecture
- OAuth-based Secure Connection
- Automatic Transaction Sync
- Mock Bank Provider for Testing

### 📂 CSV Import
- Upload Bank Statements
- Automatic Transaction Parsing
- AI Category Detection
- Duplicate Detection

### 💵 Budget Planner
- Monthly Budget Planning
- Category-wise Budget
- Budget Utilization
- Overspending Alerts

### 📈 Deep Analytics
- Spending Trends
- Weekly & Monthly Reports
- Top Merchants
- Subscription Detection
- Category Analysis

### 🎯 Financial Goals
- Emergency Fund Goal
- Retirement Planning
- Vacation Goal
- Vehicle Goal
- Goal Progress Tracking

### 🤖 AI Financial Assistant
- Google Gemini Integration
- Personalized Financial Suggestions
- Expense Queries
- Budget Recommendations
- Investment Education
- Financial Q&A

### 📉 ML Spending Forecast
- Future Expense Prediction
- Savings Forecast
- Cash Flow Prediction
- Category-wise Forecasting

### ❤️ Financial Health Score
- Savings Rate Analysis
- Budget Discipline
- Emergency Fund Evaluation
- Personalized Improvement Suggestions

### 🧮 EMI Calculator
- EMI Calculation
- Interest Breakdown
- Loan Comparison
- Amortization Schedule

### 📚 Investment Education
- SIP Guide
- Mutual Funds
- ETFs
- Stocks
- Emergency Funds
- Risk Management
- Financial Literacy

### 📄 Reports
- PDF Reports
- CSV Export
- Financial Summary Reports

---

# 🛠 Tech Stack

## Frontend
- React.js
- Vite
- Tailwind CSS
- Chart.js
- Recharts
- Framer Motion
- Lucide Icons

## Backend
- FastAPI
- SQLAlchemy
- Pydantic
- JWT Authentication
- Bcrypt

## Database
- PostgreSQL

## Machine Learning
- Pandas
- NumPy
- Scikit-learn
- Linear Regression
- Random Forest

## AI
- Google Gemini API
- OpenAI API (Optional)

---

# 📁 Project Structure

```
IntelliWealth
│
├── backend
│   ├── app
│   ├── models
│   ├── routers
│   ├── services
│   ├── schemas
│   ├── database
│   └── main.py
│
├── frontend
│   ├── src
│   ├── pages
│   ├── components
│   ├── services
│   └── assets
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/IntelliWealth.git

cd IntelliWealth
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Backend

```bash
uvicorn app.main:app --reload
```

Backend URL

```
http://localhost:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend folder.

```env
SECRET_KEY=your_secret_key

DATABASE_URL=postgresql://username:password@localhost/intelliwealth

GEMINI_API_KEY=your_gemini_api_key

OPENAI_API_KEY=your_openai_api_key
```

---

# 🤖 AI Features

- Personalized Financial Assistant
- Expense Analysis
- Budget Suggestions
- Investment Education
- Financial Health Recommendations
- Smart Spending Insights

---

# 📊 Machine Learning Features

- Expense Prediction
- Savings Forecast
- Spending Trend Analysis
- Intelligent Transaction Categorization

---

# 🔒 Security Features

- JWT Authentication
- Password Encryption (Bcrypt)
- Protected APIs
- Role-Based Access
- Secure Bank Connection Architecture

---

# 🌟 Future Enhancements

- Real Bank API Integration
- UPI Integration
- OCR Receipt Scanner
- Fraud Detection using AI
- Voice-Based Financial Assistant
- Mobile Application
- Investment Portfolio Tracker
- Real-Time Notifications

---

# 📷 Screenshots

- Login
- Dashboard
- Transactions
- Budget Planner
- Analytics
- Goals
- Forecast
- Health Score
- EMI Calculator
- AI Chatbot
- Investment Hub


---

# 👨‍💻 Author

**Naushad Pathan**

B.Tech Data Science 

AI & Full Stack Developer

GitHub: [https://github.com/yourusername](https://github.com/naushad6972/IntelliWealth)

LinkedIn: [https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/naushad-pathan-155825327/)

---

# 📄 License

This project is developed for educational purposes and personal portfolio use.

---

## ⭐ If you like this project, don't forget to Star ⭐ the repository. 
