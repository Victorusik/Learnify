from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct
from app.models import UserAchievement, Achievement, UserProgress, RepetitionData, User
from typing import List


async def check_and_unlock_achievements(db: AsyncSession, user_id: int) -> List[UserAchievement]:
    """
    Проверяет условия достижений и разблокирует их при необходимости
    """
    unlocked = []
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return unlocked
    

    result = await db.execute(select(Achievement))
    achievements = result.scalars().all()
    
    for achievement in achievements:

        result = await db.execute(
            select(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement.id
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing and existing.unlocked_at:
            continue
        

        progress = 0
        should_unlock = False
        
        if achievement.id == "first_step":

            result = await db.execute(
                select(func.count()).select_from(UserProgress).filter(
                    UserProgress.user_id == user_id
                )
            )
            progress_count = result.scalar_one()
            if progress_count > 0:
                should_unlock = True
                progress = 1
        
        elif achievement.id == "seven_days":

            if user.streak >= 7:
                should_unlock = True
                progress = user.streak
        
        elif achievement.id == "hundred_cards":

            result = await db.execute(
                select(func.count()).select_from(RepetitionData).filter(
                    RepetitionData.user_id == user_id
                )
            )
            cards_reviewed = result.scalar_one()
            progress = cards_reviewed
            if cards_reviewed >= 100:
                should_unlock = True
        
        elif achievement.id == "excellent":

            result = await db.execute(
                select(func.count()).select_from(RepetitionData).filter(
                    RepetitionData.user_id == user_id
                )
            )
            total_reviews = result.scalar_one()
            if total_reviews > 0:
                result = await db.execute(
                    select(func.count()).select_from(RepetitionData).filter(
                        RepetitionData.user_id == user_id,
                        RepetitionData.mistakes == 0
                    )
                )
                correct_reviews = result.scalar_one()
                accuracy = (correct_reviews / total_reviews) * 100
                progress = int(accuracy)
                if accuracy >= 90:
                    should_unlock = True
        
        elif achievement.id == "fast_start":

            result = await db.execute(
                select(func.count(distinct(UserProgress.lesson_id))).filter(
                    UserProgress.user_id == user_id
                )
            )
            lessons_completed = result.scalar_one()
            progress = lessons_completed
            if lessons_completed >= 5:
                should_unlock = True
        
        elif achievement.id == "persistence":

            progress = user.streak
            if user.streak >= 30:
                should_unlock = True
        
        elif achievement.id == "all_courses":

            result = await db.execute(
                select(func.count(distinct(UserProgress.course_id))).filter(
                    UserProgress.user_id == user_id
                )
            )
            courses_count = result.scalar_one()
            progress = courses_count

            result = await db.execute(
                select(func.count(distinct(UserProgress.course_id)))
            )
            total_courses = result.scalar_one()
            if courses_count >= total_courses and total_courses > 0:
                should_unlock = True
        
        elif achievement.id == "perfect":

            result = await db.execute(
                select(func.count()).select_from(RepetitionData).filter(
                    RepetitionData.user_id == user_id
                )
            )
            total_reviews = result.scalar_one()
            if total_reviews > 0:
                result = await db.execute(
                    select(func.count()).select_from(RepetitionData).filter(
                        RepetitionData.user_id == user_id,
                        RepetitionData.mistakes == 0
                    )
                )
                correct_reviews = result.scalar_one()
                accuracy = (correct_reviews / total_reviews) * 100
                progress = int(accuracy)
                if accuracy >= 100:
                    should_unlock = True
        

        if not existing:
            existing = UserAchievement(
                user_id=user_id,
                achievement_id=achievement.id,
                progress=progress
            )
            db.add(existing)
        
        if should_unlock and not existing.unlocked_at:
            existing.unlocked_at = datetime.utcnow()
            existing.progress = progress
            unlocked.append(existing)
        else:
            existing.progress = progress
    
    await db.commit()
    return unlocked

