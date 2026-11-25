from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class AssignmentBase(BaseModel):
    batch_id: int
    title: str
    description: str
    max_marks: int = 100
    due_date: datetime
    attachment_path: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    max_marks: Optional[int] = None
    due_date: Optional[datetime] = None
    attachment_path: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    marks_obtained: Decimal
    feedback_text: Optional[str] = None
    evaluated_at: datetime
    evaluator_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SubmissionResponse(BaseModel):
    id: int
    assignment_id: int
    student_id: int
    student_name: Optional[str] = None
    student_email: Optional[str] = None
    file_path: str
    submitted_at: datetime
    status: str
    feedback: Optional[FeedbackResponse] = None

    model_config = ConfigDict(from_attributes=True)

class EvaluateSubmissionRequest(BaseModel):
    marks_obtained: Decimal
    feedback_text: Optional[str] = None

class AssignmentResponse(AssignmentBase):
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    submissions_count: int = 0
    my_submission: Optional[SubmissionResponse] = None

    model_config = ConfigDict(from_attributes=True)
