from sqlalchemy.orm import Session
from typing import Optional, List
from app.models import Course, Lesson, Block, UserCourse


def get_course_progress(db: Session, user_id: int, course_id: str) -> float:
    """
    Рассчитывает прогресс пользователя по курсу в процентах
    """
    # Получаем все уроки курса
    lessons = db.query(Lesson).filter(Lesson.course_id == course_id).all()

    if not lessons:
        return 0.0

    total_blocks = 0
    completed_blocks = 0

    for lesson in lessons:
        blocks = db.query(Block).filter(Block.lesson_id == lesson.id).all()
        total_blocks += len(blocks)

        for block in blocks:
            from app.models import UserProgress
            progress = db.query(UserProgress).filter(
                UserProgress.user_id == user_id,
                UserProgress.block_id == block.id
            ).first()
            if progress:
                completed_blocks += 1

    if total_blocks == 0:
        return 0.0

    progress = (completed_blocks / total_blocks) * 100
    # Ограничиваем прогресс до 100%
    return min(progress, 100.0)

