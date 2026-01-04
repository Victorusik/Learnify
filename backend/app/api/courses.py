from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Course, UserCourse, User, Lesson
from app.schemas.course import CourseResponse, CourseEnrollResponse
from app.schemas.lesson import LessonListItem
from app.api.auth import get_current_user

router = APIRouter()


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
def enroll_course(
    course_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Записаться на курс"""

    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")


    existing = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id,
        UserCourse.course_id == course_id
    ).first()

    if existing:
        return CourseEnrollResponse(
            message="Already enrolled",
            course_id=course_id
        )


    user_course = UserCourse(
        user_id=current_user.id,
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


    course = db.query(Course).filter(Course.course_id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order).all()
    return lessons


@router.get("/user/courses", response_model=List[CourseResponse])
def get_enrolled_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Получить список курсов, на которые записан текущий пользователь"""
    user_courses = db.query(UserCourse).filter(
        UserCourse.user_id == current_user.id
    ).all()

    course_ids = [uc.course_id for uc in user_courses]
    if not course_ids:
        return []

    courses = db.query(Course).filter(Course.course_id.in_(course_ids)).all()
    return courses

