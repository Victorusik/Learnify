from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.models import Course, Lesson, Block, UserCourse, UserProgress


async def get_course_progress(db: AsyncSession, user_id: int, course_id: str) -> float:
    result = await db.execute(select(Lesson).filter(Lesson.course_id == course_id))
    lessons = result.scalars().all()

    if not lessons:
        return 0.0

    total_blocks = 0
    completed_blocks = 0

    for lesson in lessons:
        result = await db.execute(select(Block).filter(Block.lesson_id == lesson.id))
        blocks = result.scalars().all()
        total_blocks += len(blocks)

        for block in blocks:

            result = await db.execute(
                select(UserProgress).filter(
                    UserProgress.user_id == user_id,
                    UserProgress.block_id == block.id
                )
            )
            progress = result.scalar_one_or_none()
            if progress:
                completed_blocks += 1

    if total_blocks == 0:
        return 0.0

    progress = (completed_blocks / total_blocks) * 100

    return min(progress, 100.0)

