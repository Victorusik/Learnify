from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, or_, select
from typing import List
from app.models import Block, RepetitionData
from app.utils.spaced_repetition import calculate_next_review


async def get_cards_for_training(db: AsyncSession, user_id: int, limit: int = 10) -> List[Block]:
    """
    Получает карточки для тренировки с приоритетами:
    1. needs_review = true
    2. наступило время повторения
    3. новые карточки
    """
    now = datetime.utcnow()
    cards: List[Block] = []
    

    result = await db.execute(
        select(RepetitionData).filter(
            and_(
                RepetitionData.user_id == user_id,
                RepetitionData.needs_review == True
            )
        ).limit(5)
    )
    needs_review_data = result.scalars().all()
    
    needs_review_blocks = []
    for rd in needs_review_data:
        result = await db.execute(select(Block).filter(Block.id == rd.block_id))
        block = result.scalar_one_or_none()
        if block:
            needs_review_blocks.append(block)
    cards.extend(needs_review_blocks)
    

    result = await db.execute(
        select(RepetitionData).filter(
            and_(
                RepetitionData.user_id == user_id,
                RepetitionData.needs_review == False,
                RepetitionData.next_review <= now
            )
        ).limit(5)
    )
    due_review_data = result.scalars().all()
    
    due_review_blocks = []
    for rd in due_review_data:
        result = await db.execute(select(Block).filter(Block.id == rd.block_id))
        block = result.scalar_one_or_none()
        if block:
            due_review_blocks.append(block)
    cards.extend(due_review_blocks)
    

    result = await db.execute(
        select(RepetitionData).filter(RepetitionData.user_id == user_id)
    )
    existing_block_ids = {rd.block_id for rd in result.scalars().all()}
    
    if existing_block_ids:
        result = await db.execute(
            select(Block).filter(~Block.id.in_(existing_block_ids)).limit(2)
        )
    else:
        result = await db.execute(select(Block).limit(2))
    new_blocks = result.scalars().all()
    cards.extend(new_blocks)
    
    return cards[:limit]


async def submit_answer(
    db: AsyncSession,
    user_id: int,
    block_id: str,
    lesson_id: str,
    course_id: str,
    is_correct: bool
) -> RepetitionData:
    """
    Обрабатывает ответ пользователя и обновляет данные spaced repetition
    """
    result = await db.execute(
        select(RepetitionData).filter(
            and_(
                RepetitionData.user_id == user_id,
                RepetitionData.block_id == block_id
            )
        )
    )
    repetition_data = result.scalar_one_or_none()
    
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
    
    await db.commit()
    await db.refresh(repetition_data)
    
    return repetition_data

