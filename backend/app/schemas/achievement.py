from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AchievementResponse(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None
    progress: Optional[int] = None
    max_progress: Optional[int] = None

    class Config:
        from_attributes = True


class AchievementUnlockResponse(BaseModel):
    message: str
    achievement_id: str
    unlocked_at: datetime

