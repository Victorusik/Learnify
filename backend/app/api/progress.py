from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.database import get_db
from app.models import UserProgress, User, Lesson, Block
from app.schemas.progress import BlockProgressCreate, LessonProgressCreate, ProgressResponse
from app.services.achievement_service import check_and_unlock_achievements

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/progress")
async def get_progress(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserProgress).filter(UserProgress.user_id == DEFAULT_USER_ID)
    )
    progress_items = result.scalars().all()

    return {
        "total_blocks_completed": len(progress_items),
        "progress": [
            {
                "block_id": p.block_id,
                "lesson_id": p.lesson_id,
                "course_id": p.course_id,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None
            }
            for p in progress_items
        ]
    }


@router.post("/progress/block", response_model=ProgressResponse)
async def mark_block_completed(
    progress_data: BlockProgressCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserProgress).filter(
            UserProgress.user_id == DEFAULT_USER_ID,
            UserProgress.block_id == progress_data.block_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        return ProgressResponse(
            message="Block already completed",
            block_id=progress_data.block_id
        )


    user_progress = UserProgress(
        user_id=DEFAULT_USER_ID,
        block_id=progress_data.block_id,
        lesson_id=progress_data.lesson_id,
        course_id=progress_data.course_id,
        completed_at=datetime.utcnow()
    )
    db.add(user_progress)
    await db.commit()


    await check_and_unlock_achievements(db, DEFAULT_USER_ID)

    return ProgressResponse(
        message="Block marked as completed",
        block_id=progress_data.block_id
    )


@router.post("/progress/lesson", response_model=ProgressResponse)
async def mark_lesson_completed(
    progress_data: LessonProgressCreate,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Block).filter(Block.lesson_id == progress_data.lesson_id)
    )
    blocks = result.scalars().all()


    for block in blocks:
        result = await db.execute(
            select(UserProgress).filter(
                UserProgress.user_id == DEFAULT_USER_ID,
                UserProgress.block_id == block.id
            )
        )
        existing = result.scalar_one_or_none()

        if not existing:
            user_progress = UserProgress(
                user_id=DEFAULT_USER_ID,
                block_id=block.id,
                lesson_id=progress_data.lesson_id,
                course_id=progress_data.course_id,
                completed_at=datetime.utcnow()
            )
            db.add(user_progress)

    await db.commit()


    await check_and_unlock_achievements(db, DEFAULT_USER_ID)

    return ProgressResponse(
        message="Lesson marked as completed",
        lesson_id=progress_data.lesson_id
    )

