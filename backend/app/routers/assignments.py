from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Assignment, Submission, Batch, User, Enrollment
from app.schemas.assignment import AssignmentResponse, AssignmentCreate, AssignmentUpdate
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/assignments", tags=["Assignments"])

@router.get("")
def list_assignments(
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Assignment)

    if current_user.role.name == "student" and current_user.student_profile:
        # Filter assignments to batches student is enrolled in
        enrolled_batches = db.query(Enrollment.batch_id).filter(
            Enrollment.student_id == current_user.student_profile.id,
            Enrollment.status == "active"
        ).all()
        b_ids = [b[0] for b in enrolled_batches]
        query = query.filter(Assignment.batch_id.in_(b_ids))
    elif current_user.role.name == "instructor" and current_user.instructor_profile:
        inst_batches = db.query(Batch.id).filter(Batch.instructor_id == current_user.instructor_profile.id).all()
        b_ids = [b[0] for b in inst_batches]
        query = query.filter(Assignment.batch_id.in_(b_ids))

    if batch_id:
        query = query.filter(Assignment.batch_id == batch_id)

    assignments = query.order_by(Assignment.due_date.asc()).all()
    results = []

    for a in assignments:
        sub_count = db.query(Submission).filter(Submission.assignment_id == a.id).count()
        my_sub = None
        if current_user.role.name == "student" and current_user.student_profile:
            sub_rec = db.query(Submission).filter(
                Submission.assignment_id == a.id,
                Submission.student_id == current_user.student_profile.id
            ).first()
            if sub_rec:
                my_sub = {
                    "id": sub_rec.id,
                    "submitted_at": sub_rec.submitted_at.isoformat(),
                    "file_path": sub_rec.file_path,
                    "status": sub_rec.status,
                    "feedback": {
                        "marks_obtained": float(sub_rec.feedback.marks_obtained),
                        "feedback_text": sub_rec.feedback.feedback_text
                    } if sub_rec.feedback else None
                }

        results.append({
            "id": a.id,
            "batch_id": a.batch_id,
            "batch_name": a.batch.name if a.batch else "",
            "course_title": a.batch.course.title if (a.batch and a.batch.course) else "",
            "title": a.title,
            "description": a.description,
            "max_marks": a.max_marks,
            "due_date": a.due_date.isoformat(),
            "attachment_path": a.attachment_path,
            "submissions_count": sub_count,
            "my_submission": my_sub,
            "created_at": a.created_at
        })
    return results

@router.post("", response_model=AssignmentResponse)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    assign = Assignment(
        batch_id=data.batch_id,
        title=data.title,
        description=data.description,
        max_marks=data.max_marks,
        due_date=data.due_date,
        attachment_path=data.attachment_path,
        created_by_id=current_user.id
    )
    db.add(assign)
    db.commit()
    db.refresh(assign)
    return {**assign.__dict__, "submissions_count": 0, "my_submission": None}

@router.get("/{assignment_id}")
def get_assignment_details(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assign = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assign:
        raise HTTPException(status_code=404, detail="Assignment not found.")

    submissions_list = []
    my_sub = None

    if current_user.role.name in ["admin", "instructor"]:
        subs = db.query(Submission).filter(Submission.assignment_id == assignment_id).all()
        for s in subs:
            submissions_list.append({
                "id": s.id,
                "student_id": s.student_id,
                "student_name": f"{s.student.user.first_name} {s.student.user.last_name}",
                "student_email": s.student.user.email,
                "file_path": s.file_path,
                "submitted_at": s.submitted_at.isoformat(),
                "status": s.status,
                "feedback": {
                    "marks_obtained": float(s.feedback.marks_obtained),
                    "feedback_text": s.feedback.feedback_text,
                    "evaluated_at": s.feedback.evaluated_at.isoformat()
                } if s.feedback else None
            })
    else:
        # Student
        sub_rec = db.query(Submission).filter(
            Submission.assignment_id == assignment_id,
            Submission.student_id == current_user.student_profile.id
        ).first()
        if sub_rec:
            my_sub = {
                "id": sub_rec.id,
                "submitted_at": sub_rec.submitted_at.isoformat(),
                "file_path": sub_rec.file_path,
                "status": sub_rec.status,
                "feedback": {
                    "marks_obtained": float(sub_rec.feedback.marks_obtained),
                    "feedback_text": sub_rec.feedback.feedback_text
                } if sub_rec.feedback else None
            }

    return {
        "id": assign.id,
        "batch_id": assign.batch_id,
        "batch_name": assign.batch.name if assign.batch else "",
        "course_title": assign.batch.course.title if (assign.batch and assign.batch.course) else "",
        "title": assign.title,
        "description": assign.description,
        "max_marks": assign.max_marks,
        "due_date": assign.due_date.isoformat(),
        "attachment_path": assign.attachment_path,
        "created_at": assign.created_at.isoformat(),
        "my_submission": my_sub,
        "submissions": submissions_list
    }
