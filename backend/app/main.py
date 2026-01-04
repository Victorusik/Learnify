from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import categories, courses, lessons, user, progress, training, achievements, auth
from app.middleware.error_handler import GlobalErrorHandler
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends, status, Response


app = FastAPI(title="Learnify API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
app.add_middleware(GlobalErrorHandler)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["authentication"])
app.include_router(categories.router, prefix=settings.API_V1_PREFIX, tags=["categories"])
app.include_router(courses.router, prefix=settings.API_V1_PREFIX, tags=["courses"])
app.include_router(lessons.router, prefix=settings.API_V1_PREFIX, tags=["lessons"])
app.include_router(user.router, prefix=settings.API_V1_PREFIX, tags=["user"])
app.include_router(progress.router, prefix=settings.API_V1_PREFIX, tags=["progress"])
app.include_router(training.router, prefix=settings.API_V1_PREFIX, tags=["training"])
app.include_router(achievements.router, prefix=settings.API_V1_PREFIX, tags=["achievements"])


@app.get("/")
def root():
    return {"message": "Learnify API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/detailed")
def health_detailed(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "ok",
            "database": "connected",
            "version": "1.0.0"
        }
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "error",
                "database": "disconnected",
                "detail": str(e)
            }
        )

