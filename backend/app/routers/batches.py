from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Batch, Course, Instructor, Student, Enrollment, User
from app.schemas.batch import BatchResponse, BatchCreate, BatchUpdate, EnrollStudentRequest
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/batches", tags=["Batches"])

@router.get("")
def list_batches(
    course_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Batch)

    # Role scoping
    if current_user.role.name == "instructor":
        if current_user.instructor_profile:
            query = query.filter(Batch.instructor_id == current_user.instructor_profile.id)
        else:
            return []
    elif current_user.role.name == "student":
        if current_user.student_profile:
            query = query.join(Enrollment).filter(
                Enrollment.student_id == current_user.student_profile.id,
                Enrollment.status == "active"
            )
        else:
            return []

    if course_id:
        query = query.filter(Batch.course_id == course_id)
    if status:
        query = query.filter(Batch.status == status)

    batches = query.order_by(Batch.id.desc()).all()
    results = []
    for b in batches:
        enrolled_count = db.query(Enrollment).filter(Enrollment.batch_id == b.id, Enrollment.status == "active").count()
        results.append({
            "id": b.id,
            "name": b.name,
            "code": b.code,
            "course_id": b.course_id,
            "course_title": b.course.title if b.course else "",
            "instructor_id": b.instructor_id,
            "instructor_name": f"{b.instructor.user.first_name} {b.instructor.user.last_name}" if b.instructor else "Unassigned",
            "start_date": b.start_date.isoformat(),
            "end_date": b.end_date.isoformat(),
            "class_days": b.class_days,
            "class_timing": b.class_timing,
            "capacity": b.capacity,
            "enrolled_count": enrolled_count,
            "status": b.status,
            "created_at": b.created_at
        })
    return results

@router.post("", response_model=BatchResponse)
def create_batch(
    data: BatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    if data.end_date < data.start_date:
        raise HTTPException(status_code=400, detail="End date cannot precede start date.")

    existing = db.query(Batch).filter(Batch.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Batch code already exists.")

    batch = Batch(**data.dict())
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return {
        **batch.__dict__,
        "course_title": batch.course.title if batch.course else "",
        "instructor_name": f"{batch.instructor.user.first_name} {batch.instructor.user.last_name}" if batch.instructor else "Unassigned",
        "enrolled_count": 0
    }

@router.get("/{batch_id}")
def get_batch_details(
    batch_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    # Authorization
    if current_user.role.name == "instructor":
        if not current_user.instructor_profile or batch.instructor_id != current_user.instructor_profile.id:
            raise HTTPException(status_code=403, detail="Access denied. Not assigned to this batch.")
    elif current_user.role.name == "student":
        is_enrolled = db.query(Enrollment).filter(
            Enrollment.batch_id == batch_id,
            Enrollment.student_id == current_user.student_profile.id,
            Enrollment.status == "active"
        ).first()
        if not is_enrolled:
            raise HTTPException(status_code=403, detail="Access denied. Not enrolled in this batch.")

    enrolled = db.query(Enrollment).filter(Enrollment.batch_id == batch_id).all()
    roster = [
        {
            "enrollment_id": enr.id,
            "student_id": enr.student_id,
            "name": f"{enr.student.user.first_name} {enr.student.user.last_name}",
            "email": enr.student.user.email,
            "phone": enr.student.user.phone,
            "enrolled_at": enr.enrolled_at,
            "status": enr.status
        }
        for enr in enrolled
    ]

    return {
        "id": batch.id,
        "name": batch.name,
        "code": batch.code,
        "course_id": batch.course_id,
        "course_title": batch.course.title,
        "instructor_id": batch.instructor_id,
        "instructor_name": f"{batch.instructor.user.first_name} {batch.instructor.user.last_name}" if batch.instructor else "Unassigned",
        "start_date": batch.start_date.isoformat(),
        "end_date": batch.end_date.isoformat(),
        "class_days": batch.class_days,
        "class_timing": batch.class_timing,
        "capacity": batch.capacity,
        "status": batch.status,
        "roster": roster,
        "enrolled_count": len(roster)
    }

@router.put("/{batch_id}")
def update_batch(
    batch_id: int,
    data: BatchUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    for key, val in data.dict(exclude_unset=True).items():
        setattr(batch, key, val)

    db.commit()
    db.refresh(batch)
    return {"message": "Batch updated successfully."}

@router.post("/{batch_id}/students")
def enroll_student(
    batch_id: int,
    data: EnrollStudentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found.")

    current_count = db.query(Enrollment).filter(Enrollment.batch_id == batch_id, Enrollment.status == "active").count()
    if current_count >= batch.capacity:
        raise HTTPException(status_code=400, detail="Batch capacity has been reached.")

    existing = db.query(Enrollment).filter(
        Enrollment.batch_id == batch_id,
        Enrollment.student_id == data.student_id
    ).first()
    if existing:
        if existing.status == "active":
            raise HTTPException(status_code=400, detail="Student is already actively enrolled in this batch.")
        else:
            existing.status = "active"
            db.commit()
            return {"message": "Student re-enrolled successfully."}

    enr = Enrollment(batch_id=batch_id, student_id=data.student_id, status="active")
    db.add(enr)
    db.commit()
    return {"message": "Student enrolled successfully."}

@router.delete("/{batch_id}/students/{student_id}")
def remove_student_from_batch(
    batch_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    enr = db.query(Enrollment).filter(
        Enrollment.batch_id == batch_id,
        Enrollment.student_id == student_id
    ).first()
    if not enr:
        raise HTTPException(status_code=404, detail="Enrollment record not found.")

    enr.status = "dropped"
    db.commit()
    return {"message": "Student dropped from batch."}
