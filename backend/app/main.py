from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import categories, courses, lessons, user, progress, training, achievements

app = FastAPI(title="Learnify API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
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

