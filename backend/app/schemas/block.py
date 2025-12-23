from pydantic import BaseModel
from typing import Optional, List


class TheoryBlockResponse(BaseModel):
    type: str = "theory"
    order: int
    title: str
    content: str
    visualization_hint: str

    class Config:
        from_attributes = True


class PracticeBlockResponse(BaseModel):
    type: str = "practice"
    subtype: str
    order: int
    title: str
    question: Optional[str] = None
    content: Optional[str] = None
    options: Optional[List[str]] = None
    hints: List[str] = []
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    answer: Optional[str] = None
    sample_answer: Optional[str] = None

    class Config:
        from_attributes = True


BlockResponse = TheoryBlockResponse | PracticeBlockResponse

