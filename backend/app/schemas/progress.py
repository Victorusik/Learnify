from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class BlockProgressCreate(BaseModel):
    block_id: str
    lesson_id: str
    course_id: str


class LessonProgressCreate(BaseModel):
    lesson_id: str
    course_id: str


class ProgressResponse(BaseModel):
    message: str
    block_id: Optional[str] = None
    lesson_id: Optional[str] = None

