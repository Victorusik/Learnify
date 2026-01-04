from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Lesson, Block
from app.schemas.lesson import LessonResponse
from app.schemas.block import BlockResponse, TheoryBlockResponse, PracticeBlockResponse

router = APIRouter()


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    """Получить детали урока с блоками"""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    blocks = db.query(Block).filter(Block.lesson_id == lesson_id).order_by(Block.order).all()

    # Преобразуем блоки в правильный формат
    block_responses = []
    for block in blocks:
        if block.type == "theory":
            block_responses.append(TheoryBlockResponse(
                id=block.id,
                type=block.type,
                order=block.order,
                title=block.title,
                content=block.content or "",
                visualization_hint=block.visualization_hint or ""
            ))
        else:
            block_responses.append(PracticeBlockResponse(
                id=block.id,
                type=block.type,
                subtype=block.subtype or "",
                order=block.order,
                title=block.title,
                question=block.question,
                content=block.content,
                options=block.options,
                hints=block.hints or [],
                correct_answer=block.correct_answer,
                explanation=block.explanation,
                answer=block.answer,
                sample_answer=block.sample_answer
            ))

    lesson_response = LessonResponse(
        id=lesson.id,
        course_id=lesson.course_id,
        order=lesson.order,
        title=lesson.title,
        description=lesson.description,
        blocks=block_responses
    )

    return lesson_response

