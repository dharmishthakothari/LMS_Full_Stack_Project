from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel

class OptionCreate(BaseModel):
    option_text: str
    is_correct: bool = False

class OptionStudentResponse(BaseModel):
    id: int
    option_text: str

    class Config:
        from_attributes = True

class OptionInstructorResponse(BaseModel):
    id: int
    option_text: str
    is_correct: bool

    class Config:
        from_attributes = True

class QuestionCreate(BaseModel):
    question_text: str
    marks: int = 1
    sequence_order: int = 1
    options: List[OptionCreate]

class QuestionStudentResponse(BaseModel):
    id: int
    question_text: str
    marks: int
    sequence_order: int
    options: List[OptionStudentResponse]

    class Config:
        from_attributes = True

class QuestionInstructorResponse(BaseModel):
    id: int
    question_text: str
    marks: int
    sequence_order: int
    options: List[OptionInstructorResponse]

    class Config:
        from_attributes = True

class QuizBase(BaseModel):
    batch_id: int
    title: str
    description: Optional[str] = None
    duration_minutes: int = 30
    total_marks: int = 100
    passing_marks: int = 40
    retake_allowed: bool = False
    max_attempts: int = 1
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    is_published: bool = False

class QuizCreate(QuizBase):
    questions: Optional[List[QuestionCreate]] = []

class QuizResponse(QuizBase):
    id: int
    created_at: datetime
    questions_count: int = 0
    my_attempts_count: int = 0
    highest_score: Optional[Decimal] = None
    is_passed: bool = False

    class Config:
        from_attributes = True

class SubmitAnswerItem(BaseModel):
    question_id: int
    selected_option_id: Optional[int] = None

class SubmitQuizRequest(BaseModel):
    attempt_id: int
    answers: List[SubmitAnswerItem]

class AttemptResultResponse(BaseModel):
    id: int
    quiz_id: int
    quiz_title: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    score: Decimal
    total_marks: int
    passing_marks: int
    is_passed: bool
    attempt_number: int

    class Config:
        from_attributes = True
