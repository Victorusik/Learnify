from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.schemas.category import CategoryResponse


class CourseBase(BaseModel):
    course_id: str
    title: str
    category_id: str
    subcategory: str
    level: str
    difficulty_score: int
    estimated_duration_weeks: int
    estimated_duration_hours: int
    total_lessons: int
    total_practice_tasks: int
    tags: List[str] = []
    author: str
    status: str = "active"
    language: str = "ru"
    target_audience: List[str] = []
    completion_certificate: bool = False
    short_description: str
    full_description: str
    learning_outcomes: List[str] = []
    prerequisites: List[str] = []
    cover_image_url: str
    promo_video_url: Optional[str] = None


class CourseResponse(CourseBase):
    creation_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


class CourseEnrollResponse(BaseModel):
    message: str
    course_id: str

