from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import categories, courses, lessons, user, progress, training, achievements, auth
from app.middleware.error_handler import GlobalErrorHandler
from app.database import get_db, Base, engine, AsyncSessionLocal
from app import models
from app.models import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from fastapi import Depends, status


app = FastAPI(title="Learnify API", version="1.0.0")

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


    async with AsyncSessionLocal() as db:
        try:

            result = await db.execute(select(Category))
            categories = result.scalars().all()
            category_count = len(categories)
            if category_count == 0:
                print("Database is empty, loading seed data...")
                from app.seed_data import main
                main()
                print("Seed data loaded successfully!")
            else:
                print(f"Database already contains data ({category_count} categories), skipping seed data.")
        except Exception as e:
            print(f"Error loading seed data: {e}")



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(GlobalErrorHandler)


app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["authentication"])
app.include_router(categories.router, prefix=settings.API_V1_PREFIX, tags=["categories"])
app.include_router(courses.router, prefix=settings.API_V1_PREFIX, tags=["courses"])
app.include_router(lessons.router, prefix=settings.API_V1_PREFIX, tags=["lessons"])
app.include_router(user.router, prefix=settings.API_V1_PREFIX, tags=["user"])
app.include_router(progress.router, prefix=settings.API_V1_PREFIX, tags=["progress"])
app.include_router(training.router, prefix=settings.API_V1_PREFIX, tags=["training"])
app.include_router(achievements.router, prefix=settings.API_V1_PREFIX, tags=["achievements"])


@app.get("/")
async def root():
    return {"message": "Learnify API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/detailed")
async def health_detailed(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
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

