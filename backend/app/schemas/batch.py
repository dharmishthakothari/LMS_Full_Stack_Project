from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel

class BatchBase(BaseModel):
    name: str
    code: str
    course_id: int
    instructor_id: Optional[int] = None
    start_date: date
    end_date: date
    class_days: str
    class_timing: str
    capacity: int = 30
    status: str = "upcoming"

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BaseModel):
    name: Optional[str] = None
    instructor_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    class_days: Optional[str] = None
    class_timing: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None

class BatchEnrollmentResponse(BaseModel):
    id: int
    batch_id: int
    student_id: int
    student_name: str
    student_email: str
    enrolled_at: datetime
    status: str

    class Config:
        from_attributes = True

class BatchResponse(BatchBase):
    id: int
    course_title: Optional[str] = None
    instructor_name: Optional[str] = None
    enrolled_count: int = 0
    created_at: datetime

    class Config:
        from_attributes = True

class EnrollStudentRequest(BaseModel):
    student_id: int
