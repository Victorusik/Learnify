from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List
from app.models import Block, RepetitionData
from app.utils.spaced_repetition import calculate_next_review


def get_cards_for_training(db: Session, user_id: int, limit: int = 10) -> List[Block]:
    """
    Получает карточки для тренировки с приоритетами:
    1. needs_review = true
    2. наступило время повторения
    3. новые карточки
    """
    now = datetime.utcnow()
    cards: List[Block] = []
    
    # Приоритет 1: needs_review = true
    needs_review_data = db.query(RepetitionData).filter(
        and_(
            RepetitionData.user_id == user_id,
            RepetitionData.needs_review == True
        )
    ).limit(5).all()
    
    needs_review_blocks = [
        db.query(Block).filter(Block.id == rd.block_id).first()
        for rd in needs_review_data
        if db.query(Block).filter(Block.id == rd.block_id).first()
    ]
    cards.extend(needs_review_blocks)
    
    # Приоритет 2: наступило время повторения
    due_review_data = db.query(RepetitionData).filter(
        and_(
            RepetitionData.user_id == user_id,
            RepetitionData.needs_review == False,
            RepetitionData.next_review <= now
        )
    ).limit(5).all()
    
    due_review_blocks = [
        db.query(Block).filter(Block.id == rd.block_id).first()
        for rd in due_review_data
        if db.query(Block).filter(Block.id == rd.block_id).first()
    ]
    cards.extend(due_review_blocks)
    
    # Приоритет 3: новые карточки (нет в repetition_data)
    existing_block_ids = {
        rd.block_id for rd in db.query(RepetitionData).filter(
            RepetitionData.user_id == user_id
        ).all()
    }
    
    new_blocks = db.query(Block).filter(
        ~Block.id.in_(existing_block_ids)
    ).limit(2).all()
    cards.extend(new_blocks)
    
    return cards[:limit]


def submit_answer(
    db: Session,
    user_id: int,
    block_id: str,
    lesson_id: str,
    course_id: str,
    is_correct: bool
) -> RepetitionData:
    """
    Обрабатывает ответ пользователя и обновляет данные spaced repetition
    """
    repetition_data = db.query(RepetitionData).filter(
        and_(
            RepetitionData.user_id == user_id,
            RepetitionData.block_id == block_id
        )
    ).first()
    
    if not repetition_data:
        repetition_data = RepetitionData(
            user_id=user_id,
            block_id=block_id,
            lesson_id=lesson_id,
            course_id=course_id,
            interval=1,
            ease_factor=2.5,
            needs_review=False,
            mistakes=0
        )
        db.add(repetition_data)
    
    # Рассчитываем следующее повторение
    next_review, new_interval, new_ease_factor = calculate_next_review(
        repetition_data.last_review,
        repetition_data.next_review,
        repetition_data.interval,
        repetition_data.ease_factor,
        is_correct
    )
    
    repetition_data.last_review = datetime.utcnow()
    repetition_data.next_review = next_review
    repetition_data.interval = new_interval
    repetition_data.ease_factor = new_ease_factor
    repetition_data.needs_review = not is_correct
    
    if not is_correct:
        repetition_data.mistakes += 1
    else:
        repetition_data.needs_review = False
    
    db.commit()
    db.refresh(repetition_data)
    
    return repetition_data

