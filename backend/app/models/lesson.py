from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.course_id"), nullable=False)
    order = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    course = relationship("Course", back_populates="lessons")
    blocks = relationship("Block", back_populates="lesson", cascade="all, delete-orphan", order_by="Block.order")

