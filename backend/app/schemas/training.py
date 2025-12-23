from pydantic import BaseModel
from typing import List
from app.schemas.block import BlockResponse


class TrainingCardResponse(BaseModel):
    cards: List[BlockResponse]

    class Config:
        from_attributes = True


class TrainingSubmitRequest(BaseModel):
    block_id: str
    lesson_id: str
    course_id: str
    is_correct: bool


class TrainingSubmitResponse(BaseModel):
    message: str
    next_review: str
    interval: int
    needs_review: bool

