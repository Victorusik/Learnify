from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Course, UserCourse, User
from app.schemas.course import CourseResponse, CourseEnrollResponse
from app.schemas.lesson import LessonListItem

router = APIRouter()

# Временное решение: используем user_id = 1 по умолчанию
# В реальном приложении это должно быть из JWT токена
DEFAULT_USER_ID = 1


@router.get("/courses", response_model=List[CourseResponse])
def get_courses(
    category_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Получить список курсов (с опциональной фильтрацией по категории)"""
    query = db.query(Course)
    
    if category_id:
        query = query.filter(Course.category_id == category_id)
    
    courses = query.all()
    return courses


@router.get("/courses/{course_id}", response_model=CourseResponse)
def get_course(course_id: str, db: Session = Depends(get_db)):
    """Получить детали курса"""
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/courses/{course_id}/enroll", response_model=CourseEnrollResponse)
def enroll_course(course_id: str, db: Session = Depends(get_db)):
    """Записаться на курс"""
    # Проверяем существование курса
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Проверяем, не записан ли уже
    existing = db.query(UserCourse).filter(
        UserCourse.user_id == DEFAULT_USER_ID,
        UserCourse.course_id == course_id
    ).first()
    
    if existing:
        return CourseEnrollResponse(
            message="Already enrolled",
            course_id=course_id
        )
    
    # Создаем запись
    user_course = UserCourse(
        user_id=DEFAULT_USER_ID,
        course_id=course_id
    )
    db.add(user_course)
    db.commit()
    
    return CourseEnrollResponse(
        message="Successfully enrolled",
        course_id=course_id
    )


@router.get("/courses/{course_id}/lessons", response_model=List[LessonListItem])
def get_course_lessons(course_id: str, db: Session = Depends(get_db)):
    """Получить уроки курса"""
    from app.models import Lesson
    
    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()
    return lessons

