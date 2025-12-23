from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Achievement, UserAchievement
from app.schemas.achievement import AchievementResponse, AchievementUnlockResponse
from datetime import datetime

router = APIRouter()

DEFAULT_USER_ID = 1


@router.get("/achievements", response_model=List[AchievementResponse])
def get_achievements(db: Session = Depends(get_db)):
    """Получить список всех достижений с информацией о разблокировке"""
    achievements = db.query(Achievement).all()
    
    result = []
    for achievement in achievements:
        user_achievement = db.query(UserAchievement).filter(
            UserAchievement.user_id == DEFAULT_USER_ID,
            UserAchievement.achievement_id == achievement.id
        ).first()
        
        result.append(AchievementResponse(
            id=achievement.id,
            title=achievement.title,
            description=achievement.description,
            icon=achievement.icon,
            unlocked=user_achievement.unlocked_at is not None if user_achievement else False,
            unlocked_at=user_achievement.unlocked_at if user_achievement else None,
            progress=user_achievement.progress if user_achievement else 0,
            max_progress=achievement.max_progress
        ))
    
    return result


@router.post("/achievements/{achievement_id}/unlock", response_model=AchievementUnlockResponse)
def unlock_achievement(achievement_id: str, db: Session = Depends(get_db)):
    """Разблокировать достижение (обычно вызывается автоматически)"""
    achievement = db.query(Achievement).filter(Achievement.id == achievement_id).first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found")
    
    user_achievement = db.query(UserAchievement).filter(
        UserAchievement.user_id == DEFAULT_USER_ID,
        UserAchievement.achievement_id == achievement_id
    ).first()
    
    if not user_achievement:
        user_achievement = UserAchievement(
            user_id=DEFAULT_USER_ID,
            achievement_id=achievement_id
        )
        db.add(user_achievement)
    
    if user_achievement.unlocked_at:
        raise HTTPException(status_code=400, detail="Achievement already unlocked")
    
    user_achievement.unlocked_at = datetime.utcnow()
    db.commit()
    db.refresh(user_achievement)
    
    return AchievementUnlockResponse(
        message="Achievement unlocked",
        achievement_id=achievement_id,
        unlocked_at=user_achievement.unlocked_at
    )

