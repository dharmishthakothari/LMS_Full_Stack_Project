from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, User, Batch, Enrollment, Attendance, Payment
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("")
def list_students(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    query = db.query(Student).join(User)
    if search:
        s = f"%{search}%"
        query = query.filter((User.first_name.like(s)) | (User.last_name.like(s)) | (User.email.like(s)))
    
    students = query.all()
    results = []
    for st in students:
        enrolled_batches = [
            {"batch_id": enr.batch_id, "batch_name": enr.batch.name, "course_title": enr.batch.course.title}
            for enr in st.enrollments if enr.batch
        ]
        results.append({
            "id": st.id,
            "user_id": st.user.id,
            "name": f"{st.user.first_name} {st.user.last_name}",
            "email": st.user.email,
            "phone": st.user.phone,
            "is_active": st.user.is_active,
            "address": st.address,
            "emergency_contact": st.emergency_contact,
            "joining_date": st.joining_date.isoformat() if st.joining_date else None,
            "enrolled_batches": enrolled_batches
        })
    return results

@router.get("/{student_id}")
def get_student_profile(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Authorization: Student can only view self, Admin/Instructor can view any
    if current_user.role.name == "student":
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Access denied.")
    
    st = db.query(Student).filter(Student.id == student_id).first()
    if not st:
        raise HTTPException(status_code=404, detail="Student not found.")

    enrolled_batches = [
        {
            "batch_id": enr.batch_id,
            "batch_name": enr.batch.name,
            "course_id": enr.batch.course_id,
            "course_title": enr.batch.course.title,
            "instructor_name": f"{enr.batch.instructor.user.first_name} {enr.batch.instructor.user.last_name}" if enr.batch.instructor else "Unassigned",
            "status": enr.status
        }
        for enr in st.enrollments if enr.batch
    ]

    return {
        "id": st.id,
        "user_id": st.user.id,
        "name": f"{st.user.first_name} {st.user.last_name}",
        "first_name": st.user.first_name,
        "last_name": st.user.last_name,
        "email": st.user.email,
        "phone": st.user.phone,
        "is_active": st.user.is_active,
        "address": st.address,
        "emergency_contact": st.emergency_contact,
        "joining_date": st.joining_date.isoformat() if st.joining_date else None,
        "enrolled_batches": enrolled_batches
    }
