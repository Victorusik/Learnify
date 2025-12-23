from sqlalchemy import Column, String, Integer
from app.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    max_progress = Column(Integer, nullable=True)

