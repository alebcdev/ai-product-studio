
from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    description="API for generating AI-powered product advertising creatives.",
    version=settings.app_version,
    debug=settings.debug
)


@app.get("/")
def root():
    return {
        "message": "Welcome to AI Product Studio API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
