from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, UserStatistics
from app.schemas.user import UserResponse, UserUpdate, UserStatisticsResponse

router = APIRouter()

# Временное решение: используем user_id = 1 по умолчанию
DEFAULT_USER_ID = 1


@router.get("/user", response_model=UserResponse)
def get_user(db: Session = Depends(get_db)):
    """Получить данные текущего пользователя"""
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if not user:
        # Создаем пользователя по умолчанию
        user = User(
            id=DEFAULT_USER_ID,
            name="Алексей",
            level=12,
            xp=1245,
            streak=14,
            daily_goal=5,
            completed_today=3,
            selected_categories=["health", "tech"],
            notifications=[{"time": "09:00"}, {"time": "19:00"}]
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


@router.put("/user", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
    """Обновить данные пользователя"""
    user = db.query(User).filter(User.id == DEFAULT_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


@router.get("/user/statistics", response_model=UserStatisticsResponse)
def get_user_statistics(db: Session = Depends(get_db)):
    """Получить статистику пользователя"""
    stats = db.query(UserStatistics).filter(UserStatistics.user_id == DEFAULT_USER_ID).first()
    
    if not stats:
        # Создаем статистику по умолчанию
        stats = UserStatistics(
            user_id=DEFAULT_USER_ID,
            total_lessons=156,
            average_accuracy=87.0,
            days_learning=45,
            total_cards_reviewed=1245
        )
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats

