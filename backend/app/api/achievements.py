from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models import Achievement, UserAchievement
from app.schemas.achievement import AchievementResponse, AchievementUnlockResponse
from datetime import datetime

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/achievements", response_model=List[AchievementResponse])
async def get_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()
    
    result_list = []
    for achievement in achievements:
        result = await db.execute(
            select(UserAchievement).filter(
                UserAchievement.user_id == DEFAULT_USER_ID,
                UserAchievement.achievement_id == achievement.id
            )
        )
        user_achievement = result.scalar_one_or_none()
        
        result_list.append(AchievementResponse(
            id=achievement.id,
            title=achievement.title,
            description=achievement.description,
            icon=achievement.icon,
            unlocked=user_achievement.unlocked_at is not None if user_achievement else False,
            unlocked_at=user_achievement.unlocked_at if user_achievement else None,
            progress=user_achievement.progress if user_achievement else 0,
            max_progress=achievement.max_progress
        ))
    
    return result_list


@router.post("/achievements/{achievement_id}/unlock", response_model=AchievementUnlockResponse)
async def unlock_achievement(achievement_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement).filter(Achievement.id == achievement_id))
    achievement = result.scalar_one_or_none()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    result = await db.execute(
        select(UserAchievement).filter(
            UserAchievement.user_id == DEFAULT_USER_ID,
            UserAchievement.achievement_id == achievement_id
        )
    )
    user_achievement = result.scalar_one_or_none()
    
    if not user_achievement:
        user_achievement = UserAchievement(
            user_id=DEFAULT_USER_ID,
            achievement_id=achievement_id
        )
        db.add(user_achievement)
    
    if user_achievement.unlocked_at:
        raise HTTPException(status_code=400, detail="Achievement already unlocked")
    
    user_achievement.unlocked_at = datetime.utcnow()
    await db.commit()
    await db.refresh(user_achievement)
    
    return AchievementUnlockResponse(
        message="Achievement unlocked",
        achievement_id=achievement_id,
        unlocked_at=user_achievement.unlocked_at
    )

