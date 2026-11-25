from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Attendance, Batch, Student, User, Enrollment
from app.schemas.shared import BatchAttendanceSubmit, AttendanceResponse, StudentAttendanceSummary
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

@router.post("")
def record_batch_attendance(
    data: BatchAttendanceSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    batch = db.query(Batch).filter(Batch.id == data.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    for item in data.records:
        rec = db.query(Attendance).filter(
            Attendance.batch_id == data.batch_id,
            Attendance.student_id == item.student_id,
            Attendance.session_date == data.session_date
        ).first()

        if rec:
            rec.status = item.status
            rec.notes = item.notes
            rec.marked_by_id = current_user.id
        else:
            rec = Attendance(
                batch_id=data.batch_id,
                student_id=item.student_id,
                session_date=data.session_date,
                status=item.status,
                notes=item.notes,
                marked_by_id=current_user.id
            )
            db.add(rec)

    db.commit()
    return {"message": f"Attendance for session {data.session_date} saved successfully."}

@router.get("/batch/{batch_id}")
def get_batch_attendance(
    batch_id: int,
    session_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    query = db.query(Attendance).filter(Attendance.batch_id == batch_id)
    if session_date:
        query = query.filter(Attendance.session_date == session_date)

    records = query.order_by(Attendance.session_date.desc()).all()
    results = []
    for r in records:
        results.append({
            "id": r.id,
            "batch_id": r.batch_id,
            "student_id": r.student_id,
            "student_name": f"{r.student.user.first_name} {r.student.user.last_name}",
            "session_date": r.session_date.isoformat(),
            "status": r.status,
            "notes": r.notes
        })
    return results

@router.get("/student/{student_id}")
def get_student_attendance(
    student_id: int,
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name == "student":
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Access denied.")

    query = db.query(Attendance).filter(Attendance.student_id == student_id)
    if batch_id:
        query = query.filter(Attendance.batch_id == batch_id)

    records = query.order_by(Attendance.session_date.desc()).all()
    total = len(records)
    present = sum(1 for r in records if r.status == "present")
    absent = total - present
    pct = (present / total * 100.0) if total > 0 else 100.0

    return {
        "summary": {
            "total_sessions": total,
            "present_sessions": present,
            "absent_sessions": absent,
            "attendance_percentage": round(pct, 1)
        },
        "history": [
            {
                "id": r.id,
                "batch_id": r.batch_id,
                "batch_name": r.batch.name if r.batch else "",
                "session_date": r.session_date.isoformat(),
                "status": r.status,
                "notes": r.notes
            }
            for r in records
        ]
    }
