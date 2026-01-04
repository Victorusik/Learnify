from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.training import TrainingCardResponse, TrainingSubmitRequest, TrainingSubmitResponse
from app.schemas.block import BlockResponse, TheoryBlockResponse, PracticeBlockResponse
from app.services.training_service import get_cards_for_training, submit_answer
from app.services.achievement_service import check_and_unlock_achievements

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/training/cards", response_model=TrainingCardResponse)
def get_training_cards(db: Session = Depends(get_db)):
    """Получить карточки для тренировки"""
    cards = get_cards_for_training(db, DEFAULT_USER_ID, limit=10)
    
    block_responses = []
    for block in cards:
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
    
    return TrainingCardResponse(cards=block_responses)


@router.post("/training/submit", response_model=TrainingSubmitResponse)
def submit_training_answer(
    request: TrainingSubmitRequest,
    db: Session = Depends(get_db)
):
    """Отправить ответ на карточку"""
    repetition_data = submit_answer(
        db,
        DEFAULT_USER_ID,
        request.block_id,
        request.lesson_id,
        request.course_id,
        request.is_correct
    )
    
    # Проверяем достижения
    check_and_unlock_achievements(db, DEFAULT_USER_ID)
    
    return TrainingSubmitResponse(
        message="Answer submitted",
        next_review=repetition_data.next_review.isoformat() if repetition_data.next_review else "",
        interval=repetition_data.interval,
        needs_review=repetition_data.needs_review
    )

