from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    name: str
    level: int = 1
    xp: int = 0
    streak: int = 0
    daily_goal: int = 5
    completed_today: int = 0
    selected_categories: List[str] = []
    notifications: List[dict] = []


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[int] = None
    xp: Optional[int] = None
    streak: Optional[int] = None
    daily_goal: Optional[int] = None
    completed_today: Optional[int] = None
    selected_categories: Optional[List[str]] = None
    notifications: Optional[List[dict]] = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserStatisticsResponse(BaseModel):
    total_lessons: int
    average_accuracy: float
    days_learning: int
    total_cards_reviewed: int

    class Config:
        from_attributes = True

