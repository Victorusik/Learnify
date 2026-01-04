from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, UserStatistics
from app.schemas.user import UserResponse, UserUpdate, UserStatisticsResponse

router = APIRouter()


DEFAULT_USER_ID = 1


@router.get("/user", response_model=UserResponse)
async def get_user(db: AsyncSession = Depends(get_db)):
    """Получить данные текущего пользователя"""
    result = await db.execute(select(User).filter(User.id == DEFAULT_USER_ID))
    user = result.scalar_one_or_none()
    if not user:

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
        await db.commit()
        await db.refresh(user)
    return user


@router.put("/user", response_model=UserResponse)
async def update_user(user_update: UserUpdate, db: AsyncSession = Depends(get_db)):
    """Обновить данные пользователя"""
    result = await db.execute(select(User).filter(User.id == DEFAULT_USER_ID))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    return user


@router.get("/user/statistics", response_model=UserStatisticsResponse)
async def get_user_statistics(db: AsyncSession = Depends(get_db)):
    """Получить статистику пользователя"""
    result = await db.execute(
        select(UserStatistics).filter(UserStatistics.user_id == DEFAULT_USER_ID)
    )
    stats = result.scalar_one_or_none()
    
    if not stats:

        stats = UserStatistics(
            user_id=DEFAULT_USER_ID,
            total_lessons=156,
            average_accuracy=87.0,
            days_learning=45,
            total_cards_reviewed=1245
        )
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
    
    return stats

