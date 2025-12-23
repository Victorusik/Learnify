from sqlalchemy import Column, String, Integer, Boolean, ARRAY, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Course(Base):
    __tablename__ = "courses"

    course_id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    subcategory = Column(String, nullable=False)
    level = Column(String, nullable=False)  # 'Легкий', 'Средний', 'Сложный'
    difficulty_score = Column(Integer, nullable=False)
    estimated_duration_weeks = Column(Integer, nullable=False)
    estimated_duration_hours = Column(Integer, nullable=False)
    total_lessons = Column(Integer, nullable=False)
    total_practice_tasks = Column(Integer, nullable=False)
    tags = Column(ARRAY(String), default=list)
    author = Column(String, nullable=False)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, default="active")
    language = Column(String, default="ru")
    target_audience = Column(ARRAY(String), default=list)
    completion_certificate = Column(Boolean, default=False)
    short_description = Column(String, nullable=False)
    full_description = Column(String, nullable=False)
    learning_outcomes = Column(ARRAY(String), default=list)
    prerequisites = Column(ARRAY(String), default=list)
    cover_image_url = Column(String, nullable=False)
    promo_video_url = Column(String, nullable=True)

    category = relationship("Category", backref="courses")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")

