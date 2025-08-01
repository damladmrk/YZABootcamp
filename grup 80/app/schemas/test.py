from pydantic import BaseModel
from typing import List

class TestAnswer(BaseModel):
    question_id: int
    category: str
    question: str
    answer: str
    value: int

class TestSubmission(BaseModel):
    answers: List[TestAnswer]
    totalScore: int
    maxScore: int
    scorePercentage: float
    duration: float
    completed_at: str