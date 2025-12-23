from sqlalchemy import Column, String, Integer, ARRAY, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Block(Base):
    __tablename__ = "blocks"

    id = Column(String, primary_key=True, index=True)
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    type = Column(String, nullable=False)  # 'theory' or 'practice'
    subtype = Column(String, nullable=True)  # 'multiple_choice', 'reflection', 'case', 'text_input'
    order = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    question = Column(String, nullable=True)
    options = Column(ARRAY(String), nullable=True)
    hints = Column(ARRAY(String), default=list)
    correct_answer = Column(String, nullable=True)
    explanation = Column(String, nullable=True)
    sample_answer = Column(String, nullable=True)
    answer = Column(String, nullable=True)
    visualization_hint = Column(String, nullable=True)

    lesson = relationship("Lesson", back_populates="blocks")

