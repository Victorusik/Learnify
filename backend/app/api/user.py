from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, UserStatistics
from app.schemas.user import UserResponse, UserUpdate, UserStatisticsResponse
from app.api.auth import get_current_user

router = APIRouter()


@router.get("/user", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/user", response_model=UserResponse)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    return current_user


@router.get("/user/statistics", response_model=UserStatisticsResponse)
async def get_user_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserStatistics).filter(UserStatistics.user_id == current_user.id)
    )
    stats = result.scalar_one_or_none()
    
    if not stats:
        stats = UserStatistics(
            user_id=current_user.id,
            total_lessons=0,
            average_accuracy=0.0,
            days_learning=0,
            total_cards_reviewed=0
        )
        db.add(stats)
        await db.commit()
        await db.refresh(stats)
    
    return stats

