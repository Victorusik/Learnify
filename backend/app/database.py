from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE if hasattr(settings, 'DB_POOL_SIZE') else 5,
    max_overflow=settings.DB_MAX_OVERFLOW if hasattr(settings, 'DB_MAX_OVERFLOW') else 10,
    pool_recycle=settings.DB_POOL_RECYCLE if hasattr(settings, 'DB_POOL_RECYCLE') else 3600,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

