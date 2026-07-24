import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.db.session import engine, Base
from app.routers import (
    auth, banks, transactions, analytics, budgets,
    goals, health, emi, forecast, education, chat, reports, notifications
)
from app.services.bank_integration.sync_scheduler import perform_background_bank_sync
from app.middleware.perf import performance_middleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize background scheduler for periodic bank transaction & token auto-sync
scheduler = BackgroundScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create DB tables
    logger.info("Initializing database tables...")
    Base.metadata.create_all(bind=engine)

    # Start background scheduled bank sync task
    scheduler.add_job(
        perform_background_bank_sync,
        'interval',
        minutes=settings.BANK_SYNC_INTERVAL_MINUTES,
        id='background_bank_sync_job',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"Background bank sync scheduler started (Interval: {settings.BANK_SYNC_INTERVAL_MINUTES} mins).")

    yield

    # Shutdown
    logger.info("Shutting down background scheduler...")
    scheduler.shutdown(wait=False)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="IntelliWealth - AI-Powered Financial Intelligence Agent API",
    lifespan=lifespan
)

# Performance middleware to log slow endpoints
app.middleware('http')(performance_middleware)

# CORS configuration for Frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(banks.router, prefix=settings.API_V1_STR)
app.include_router(transactions.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)
app.include_router(budgets.router, prefix=settings.API_V1_STR)
app.include_router(goals.router, prefix=settings.API_V1_STR)
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(emi.router, prefix=settings.API_V1_STR)
app.include_router(forecast.router, prefix=settings.API_V1_STR)
app.include_router(education.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
