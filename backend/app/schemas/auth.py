from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    name: str = Field(..., min_length=1, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


class UserProfile(BaseModel):
    """Schema for user profile response"""
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




