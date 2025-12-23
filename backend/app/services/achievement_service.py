from datetime import datetime
from sqlalchemy.orm import Session
from app.models import UserAchievement, Achievement, UserProgress, RepetitionData, User
from typing import List


def check_and_unlock_achievements(db: Session, user_id: int) -> List[UserAchievement]:
    """
    Проверяет условия достижений и разблокирует их при необходимости
    """
    unlocked = []
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return unlocked
    
    # Получаем все достижения
    achievements = db.query(Achievement).all()
    
    for achievement in achievements:
        # Проверяем, не разблокировано ли уже
        existing = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == achievement.id
        ).first()
        
        if existing and existing.unlocked_at:
            continue
        
        # Проверяем условия
        progress = 0
        should_unlock = False
        
        if achievement.id == "first_step":
            # Завершить первый урок
            progress_count = db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).count()
            if progress_count > 0:
                should_unlock = True
                progress = 1
        
        elif achievement.id == "seven_days":
            # 7 дней подряд
            if user.streak >= 7:
                should_unlock = True
                progress = user.streak
        
        elif achievement.id == "hundred_cards":
            # 100 карточек
            cards_reviewed = db.query(RepetitionData).filter(
                RepetitionData.user_id == user_id
            ).count()
            progress = cards_reviewed
            if cards_reviewed >= 100:
                should_unlock = True
        
        elif achievement.id == "excellent":
            # 90% точности
            total_reviews = db.query(RepetitionData).filter(
                RepetitionData.user_id == user_id
            ).count()
            if total_reviews > 0:
                correct_reviews = db.query(RepetitionData).filter(
                    RepetitionData.user_id == user_id,
                    RepetitionData.mistakes == 0
                ).count()
                accuracy = (correct_reviews / total_reviews) * 100
                progress = int(accuracy)
                if accuracy >= 90:
                    should_unlock = True
        
        elif achievement.id == "fast_start":
            # 5 уроков за неделю
            lessons_completed = db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).distinct(UserProgress.lesson_id).count()
            progress = lessons_completed
            if lessons_completed >= 5:
                should_unlock = True
        
        elif achievement.id == "persistence":
            # 30 дней подряд
            progress = user.streak
            if user.streak >= 30:
                should_unlock = True
        
        elif achievement.id == "all_courses":
            # Все курсы
            courses_count = db.query(UserProgress).filter(
                UserProgress.user_id == user_id
            ).distinct(UserProgress.course_id).count()
            progress = courses_count
            # Нужно знать общее количество курсов
            total_courses = db.query(UserProgress).distinct(UserProgress.course_id).count()
            if courses_count >= total_courses and total_courses > 0:
                should_unlock = True
        
        elif achievement.id == "perfect":
            # 100% точность
            total_reviews = db.query(RepetitionData).filter(
                RepetitionData.user_id == user_id
            ).count()
            if total_reviews > 0:
                correct_reviews = db.query(RepetitionData).filter(
                    RepetitionData.user_id == user_id,
                    RepetitionData.mistakes == 0
                ).count()
                accuracy = (correct_reviews / total_reviews) * 100
                progress = int(accuracy)
                if accuracy >= 100:
                    should_unlock = True
        
        # Создаем или обновляем запись
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
    
    db.commit()
    return unlocked

