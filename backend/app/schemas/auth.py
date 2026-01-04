from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    daily_goal: Optional[int] = Field(None, ge=1, le=50)
    selected_categories: Optional[list[str]] = None


class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    level: int
    xp: int
    streak: int
    daily_goal: int
    completed_today: int
    selected_categories: list
    notifications: list

    class Config:
        from_attributes = True








