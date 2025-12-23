from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import UserProgress, User, Lesson
from app.schemas.progress import BlockProgressCreate, LessonProgressCreate, ProgressResponse
from app.services.achievement_service import check_and_unlock_achievements

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/progress")
def get_progress(db: Session = Depends(get_db)):
    """Получить прогресс пользователя по всем курсам"""
    progress_items = db.query(UserProgress).filter(
        UserProgress.user_id == DEFAULT_USER_ID
    ).all()
    
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
def mark_block_completed(
    progress_data: BlockProgressCreate,
    db: Session = Depends(get_db)
):
    """Отметить блок как выполненный"""
    # Проверяем, не отмечен ли уже
    existing = db.query(UserProgress).filter(
        UserProgress.user_id == DEFAULT_USER_ID,
        UserProgress.block_id == progress_data.block_id
    ).first()
    
    if existing:
        return ProgressResponse(
            message="Block already completed",
            block_id=progress_data.block_id
        )
    
    # Создаем запись о прогрессе
    user_progress = UserProgress(
        user_id=DEFAULT_USER_ID,
        block_id=progress_data.block_id,
        lesson_id=progress_data.lesson_id,
        course_id=progress_data.course_id,
        completed_at=datetime.utcnow()
    )
    db.add(user_progress)
    db.commit()
    
    # Проверяем достижения
    check_and_unlock_achievements(db, DEFAULT_USER_ID)
    
    return ProgressResponse(
        message="Block marked as completed",
        block_id=progress_data.block_id
    )


@router.post("/progress/lesson", response_model=ProgressResponse)
def mark_lesson_completed(
    progress_data: LessonProgressCreate,
    db: Session = Depends(get_db)
):
    """Отметить урок как завершенный"""
    # Получаем все блоки урока
    from app.models import Block
    blocks = db.query(Block).filter(Block.lesson_id == progress_data.lesson_id).all()
    
    # Отмечаем все блоки как завершенные
    for block in blocks:
        existing = db.query(UserProgress).filter(
            UserProgress.user_id == DEFAULT_USER_ID,
            UserProgress.block_id == block.id
        ).first()
        
        if not existing:
            user_progress = UserProgress(
                user_id=DEFAULT_USER_ID,
                block_id=block.id,
                lesson_id=progress_data.lesson_id,
                course_id=progress_data.course_id,
                completed_at=datetime.utcnow()
            )
            db.add(user_progress)
    
    db.commit()
    
    # Проверяем достижения
    check_and_unlock_achievements(db, DEFAULT_USER_ID)
    
    return ProgressResponse(
        message="Lesson marked as completed",
        lesson_id=progress_data.lesson_id
    )

