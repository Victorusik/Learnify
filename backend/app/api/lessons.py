from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Lesson, Block
from app.schemas.lesson import LessonResponse
from app.schemas.block import BlockResponse, TheoryBlockResponse, PracticeBlockResponse

router = APIRouter()


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lesson).filter(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    result = await db.execute(
        select(Block).filter(Block.lesson_id == lesson_id).order_by(Block.order)
    )
    blocks = result.scalars().all()



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

