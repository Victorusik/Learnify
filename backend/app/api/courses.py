from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.database import get_db
from app.models import Course, UserCourse, User, Lesson
from app.schemas.course import CourseResponse, CourseEnrollResponse
from app.schemas.lesson import LessonListItem
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/courses", response_model=List[CourseResponse])
async def get_courses(
    category_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    query = select(Course).options(selectinload(Course.category))

    if category_id:
        query = query.filter(Course.category_id == category_id)

    result = await db.execute(query)
    courses = result.scalars().all()
    return courses


@router.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.category))
        .filter(Course.course_id == course_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/courses/{course_id}/enroll", response_model=CourseEnrollResponse)
async def enroll_course(
    course_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Course)
        .options(selectinload(Course.category))
        .filter(Course.course_id == course_id)
        )
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")


    result = await db.execute(
        select(UserCourse).filter(
            UserCourse.user_id == current_user.id,
            UserCourse.course_id == course_id
        )
    )
    existing = result.scalar_one_or_none()

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
    await db.commit()

    return CourseEnrollResponse(
        message="Successfully enrolled",
        course_id=course_id
    )


@router.get("/courses/{course_id}/lessons", response_model=List[LessonListItem])
async def get_course_lessons(course_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course).filter(Course.course_id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    result = await db.execute(
        select(Lesson).filter(Lesson.course_id == course_id).order_by(Lesson.order)
    )
    lessons = result.scalars().all()
    return lessons


@router.get("/user/courses", response_model=List[CourseResponse])
async def get_enrolled_courses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(UserCourse).filter(UserCourse.user_id == current_user.id)
    )
    user_courses = result.scalars().all()

    course_ids = [uc.course_id for uc in user_courses]
    if not course_ids:
        return []

    result = await db.execute(
        select(Course)
        .options(selectinload(Course.category))
        .filter(Course.course_id.in_(course_ids))
    )
    courses = result.scalars().all()
    return courses

