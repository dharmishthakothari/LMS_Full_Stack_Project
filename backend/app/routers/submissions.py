import os
import uuid
from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import Submission, Assignment, AssignmentFeedback, User, Enrollment
from app.schemas.assignment import EvaluateSubmissionRequest
from app.dependencies.auth import get_current_user, require_role
from app.utils.file_validator import validate_and_read_upload, ALLOWED_SUBMISSION_EXTENSIONS
from app.services.storage_service import save_bytes

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])

@router.post("")
async def submit_assignment(
    assignment_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student"]))
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Student profile not found.")
    
    student_id = current_user.student_profile.id
    assign = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assign:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    # Check student is enrolled in batch
    is_enrolled = db.query(Enrollment).filter(
        Enrollment.batch_id == assign.batch_id,
        Enrollment.student_id == student_id,
        Enrollment.status == "active"
    ).first()
    if not is_enrolled:
        raise HTTPException(status_code=403, detail="Not enrolled in the assigned batch for this assignment.")

    # Check deadline
    now = datetime.utcnow()
    status_str = "late_submission" if now > assign.due_date else "submitted"

    # Save file safely via storage abstraction (local or S3)
    safe_name, contents = await validate_and_read_upload(file, ALLOWED_SUBMISSION_EXTENSIONS)
    filename = f"sub_{student_id}_{safe_name}"
    stored_path = save_bytes(f"submissions/{filename}", contents, content_type=file.content_type)

    submission = db.query(Submission).filter(
        Submission.assignment_id == assignment_id,
        Submission.student_id == student_id
    ).first()

    if submission:
        submission.file_path = stored_path
        submission.submitted_at = now
        submission.status = status_str
    else:
        submission = Submission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_path=stored_path,
            submitted_at=now,
            status=status_str
        )
        db.add(submission)

    db.commit()
    db.refresh(submission)
    return {
        "message": "Assignment submitted successfully.",
        "submission_id": submission.id,
        "status": submission.status
    }

@router.post("/{submission_id}/evaluate")
def evaluate_submission(
    submission_id: int,
    data: EvaluateSubmissionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found.")

    if data.marks_obtained > Decimal(str(sub.assignment.max_marks)):
        raise HTTPException(status_code=400, detail=f"Marks obtained cannot exceed maximum marks ({sub.assignment.max_marks}).")
    if data.marks_obtained < Decimal("0"):
        raise HTTPException(status_code=400, detail="Marks cannot be negative.")

    feedback = db.query(AssignmentFeedback).filter(AssignmentFeedback.submission_id == submission_id).first()
    if feedback:
        feedback.marks_obtained = data.marks_obtained
        feedback.feedback_text = data.feedback_text
        feedback.evaluated_by_id = current_user.id
        feedback.evaluated_at = datetime.utcnow()
    else:
        feedback = AssignmentFeedback(
            submission_id=submission_id,
            evaluated_by_id=current_user.id,
            marks_obtained=data.marks_obtained,
            feedback_text=data.feedback_text,
            evaluated_at=datetime.utcnow()
        )
        db.add(feedback)

    sub.status = "evaluated"
    db.commit()
    return {"message": "Submission evaluated successfully."}
