from pydantic import BaseModel
from typing import List, Optional
from app.schemas.block import BlockResponse


class LessonBase(BaseModel):
    id: str
    course_id: str
    order: int
    title: str
    description: str


class LessonResponse(LessonBase):
    blocks: List[BlockResponse] = []

    class Config:
        from_attributes = True


class LessonListItem(BaseModel):
    id: str
    order: int
    title: str
    description: str
    blocks: List[BlockResponse] = []

    class Config:
        from_attributes = True

