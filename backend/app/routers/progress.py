from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Student, User, Course
from app.dependencies.auth import get_current_user
from app.services.progress_service import calculate_student_course_progress

router = APIRouter(prefix="/api/progress", tags=["Student Progress"])

@router.get("/me")
def get_my_progress(
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Convenience endpoint — students can call /api/progress/me instead of /api/progress/student/{id}."""
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Student profile not found.")
    student_id = current_user.student_profile.id

    if course_id:
        return calculate_student_course_progress(db, student_id, course_id)

    course_ids = [enr.batch.course_id for enr in current_user.student_profile.enrollments if enr.batch and enr.batch.course_id]
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all() if course_ids else []
    if not courses:
        first_course = db.query(Course).first()
        if first_course:
            courses = [first_course]

    results = []
    for c in courses:
        prog = calculate_student_course_progress(db, student_id, c.id)
        if prog:
            results.append(prog)
    return results

@router.get("/student/{student_id}")
def get_student_progress(
    student_id: int,
    course_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role.name == "student":
        if not current_user.student_profile or current_user.student_profile.id != student_id:
            raise HTTPException(status_code=403, detail="Access denied.")

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # If course_id is provided, calculate for that course
    if course_id:
        return calculate_student_course_progress(db, student_id, course_id)

    # Otherwise, return progress for all enrolled courses
    course_ids = [enr.batch.course_id for enr in student.enrollments if enr.batch and enr.batch.course_id]
    courses = db.query(Course).filter(Course.id.in_(course_ids)).all() if course_ids else []
    
    # Fallback to course 1 if enrolled list is empty
    if not courses:
        first_course = db.query(Course).first()
        if first_course:
            courses = [first_course]

    results = []
    for c in courses:
        prog = calculate_student_course_progress(db, student_id, c.id)
        if prog:
            results.append(prog)

    return results
