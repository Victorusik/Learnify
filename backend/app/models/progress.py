from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserCourse(Base):
    __tablename__ = "user_courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="enrolled_courses")
    course = relationship("Course")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    block_id = Column(String, ForeignKey("blocks.id"), nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="progress")
    block = relationship("Block")
    lesson = relationship("Lesson")
    course = relationship("Course")


class RepetitionData(Base):
    __tablename__ = "repetition_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    block_id = Column(String, ForeignKey("blocks.id"), nullable=False)
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    last_review = Column(DateTime(timezone=True), nullable=True)
    next_review = Column(DateTime(timezone=True), nullable=True)
    interval = Column(Integer, default=1)  # дни
    ease_factor = Column(Float, default=2.5)
    needs_review = Column(Boolean, default=False)
    mistakes = Column(Integer, default=0)

    user = relationship("User", backref="repetition_data")
    block = relationship("Block")


class UserAchievement(Base):
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(String, ForeignKey("achievements.id"), nullable=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=True)
    progress = Column(Integer, default=0)

    user = relationship("User", backref="achievements")
    achievement = relationship("Achievement")


class UserStatistics(Base):
    __tablename__ = "user_statistics"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    total_lessons = Column(Integer, default=0)
    average_accuracy = Column(Float, default=0.0)
    days_learning = Column(Integer, default=0)
    total_cards_reviewed = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", backref="statistics")

