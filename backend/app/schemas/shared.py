from datetime import datetime, date
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

# Attendance
class AttendanceRecordItem(BaseModel):
    student_id: int
    status: str  # present, absent, late, excused
    notes: Optional[str] = None

class BatchAttendanceSubmit(BaseModel):
    batch_id: int
    session_date: date
    records: List[AttendanceRecordItem]

class AttendanceResponse(BaseModel):
    id: int
    batch_id: int
    student_id: int
    student_name: str
    session_date: date
    status: str
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StudentAttendanceSummary(BaseModel):
    total_sessions: int
    present_sessions: int
    absent_sessions: int
    attendance_percentage: float

# Payments
class PaymentCreate(BaseModel):
    student_id: int
    course_id: int
    paid_amount: Decimal
    payment_method: str
    transaction_reference: str
    remarks: Optional[str] = None

class PaymentResponse(BaseModel):
    id: int
    student_id: int
    student_name: str
    course_id: int
    course_title: str
    total_fee: Decimal
    paid_amount: Decimal
    pending_amount: Decimal
    payment_date: datetime
    payment_method: str
    transaction_reference: str
    status: str
    receipt_path: Optional[str] = None
    remarks: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Certificates
class CertificateResponse(BaseModel):
    id: int
    certificate_number: str
    verification_id: str
    student_id: int
    student_name: str
    course_id: int
    course_title: str
    issue_date: date
    pdf_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Progress
class ProgressResponse(BaseModel):
    student_id: int
    student_name: str
    course_id: int
    course_title: str
    completed_lectures: int
    total_lectures: int
    lecture_completion_percentage: float
    evaluated_assignments: int
    total_assignments: int
    assignment_completion_percentage: float
    passed_quizzes: int
    total_quizzes: int
    quiz_completion_percentage: float
    attendance_percentage: float
    overall_progress_percentage: float
    is_eligible_for_certificate: bool

# Communication
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    link: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AnnouncementCreate(BaseModel):
    title: str
    content: str
    target_role: str = "all"
    target_batch_id: Optional[int] = None

class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    target_role: str
    target_batch_id: Optional[int] = None
    batch_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
