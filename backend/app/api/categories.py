from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Category
from app.schemas.category import CategoryResponse

router = APIRouter()


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Получить список всех категорий"""
    categories = db.query(Category).all()
    return categories

