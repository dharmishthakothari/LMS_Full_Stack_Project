from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Instructor, User, Batch
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/instructors", tags=["Instructors"])

@router.get("")
def list_instructors(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    query = db.query(Instructor).join(User)
    if search:
        s = f"%{search}%"
        query = query.filter((User.first_name.like(s)) | (User.last_name.like(s)) | (User.email.like(s)))

    instructors = query.all()
    results = []
    for inst in instructors:
        assigned_batches = [
            {"id": b.id, "name": b.name, "course_title": b.course.title, "status": b.status}
            for b in inst.batches
        ]
        results.append({
            "id": inst.id,
            "user_id": inst.user.id,
            "name": f"{inst.user.first_name} {inst.user.last_name}",
            "email": inst.user.email,
            "phone": inst.user.phone,
            "expertise": inst.expertise,
            "qualification": inst.qualification,
            "biography": inst.biography,
            "is_active": inst.user.is_active,
            "assigned_batches": assigned_batches
        })
    return results

@router.get("/{instructor_id}")
def get_instructor_details(
    instructor_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    inst = db.query(Instructor).filter(Instructor.id == instructor_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instructor not found.")
    
    assigned_batches = [
        {"id": b.id, "name": b.name, "course_title": b.course.title, "status": b.status, "capacity": b.capacity}
        for b in inst.batches
    ]
    return {
        "id": inst.id,
        "user_id": inst.user.id,
        "name": f"{inst.user.first_name} {inst.user.last_name}",
        "first_name": inst.user.first_name,
        "last_name": inst.user.last_name,
        "email": inst.user.email,
        "phone": inst.user.phone,
        "expertise": inst.expertise,
        "qualification": inst.qualification,
        "biography": inst.biography,
        "assigned_batches": assigned_batches
    }
