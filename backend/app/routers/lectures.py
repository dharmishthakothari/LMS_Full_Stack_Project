import os
import uuid
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.config import settings
from app.models import Lecture, CourseModule, StudyMaterial, LectureProgress, User
from app.schemas.lecture import LectureResponse, LectureCreate, LectureUpdate, StudyMaterialResponse
from app.dependencies.auth import get_current_user, require_role
from app.utils.file_validator import validate_and_read_upload, ALLOWED_MATERIAL_EXTENSIONS
from app.services.storage_service import save_bytes

router = APIRouter(prefix="/api/lectures", tags=["Lectures"])

@router.get("", response_model=List[LectureResponse])
def get_lectures(
    module_id: Optional[int] = None,
    batch_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Lecture)
    if module_id:
        query = query.filter(Lecture.module_id == module_id)
    if batch_id:
        query = query.filter((Lecture.batch_id == batch_id) | (Lecture.batch_id == None))
    
    lectures = query.order_by(Lecture.sequence_order.asc()).all()
    results = []
    
    # Check completion if student
    completed_ids = set()
    if current_user.role.name == "student" and current_user.student_profile:
        prog = db.query(LectureProgress.lecture_id).filter(
            LectureProgress.student_id == current_user.student_profile.id,
            LectureProgress.is_completed == True
        ).all()
        completed_ids = {p[0] for p in prog}

    for lec in lectures:
        results.append({
            "id": lec.id,
            "module_id": lec.module_id,
            "batch_id": lec.batch_id,
            "title": lec.title,
            "description": lec.description,
            "sequence_order": lec.sequence_order,
            "video_url": lec.video_url,
            "duration_minutes": lec.duration_minutes,
            "created_at": lec.created_at,
            "is_completed": (lec.id in completed_ids),
            "materials": lec.materials
        })
    return results

@router.post("", response_model=LectureResponse)
def create_lecture(
    data: LectureCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    mod = db.query(CourseModule).filter(CourseModule.id == data.module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found.")

    lec = Lecture(**data.dict())
    db.add(lec)
    db.commit()
    db.refresh(lec)
    return {**lec.__dict__, "is_completed": False, "materials": []}

@router.get("/{lecture_id}")
def get_lecture_details(
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    lec = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lec:
        raise HTTPException(status_code=404, detail="Lecture not found.")

    is_completed = False
    if current_user.role.name == "student" and current_user.student_profile:
        is_completed = db.query(LectureProgress).filter(
            LectureProgress.student_id == current_user.student_profile.id,
            LectureProgress.lecture_id == lecture_id,
            LectureProgress.is_completed == True
        ).first() is not None

    return {
        "id": lec.id,
        "module_id": lec.module_id,
        "title": lec.title,
        "description": lec.description,
        "sequence_order": lec.sequence_order,
        "video_url": lec.video_url,
        "duration_minutes": lec.duration_minutes,
        "created_at": lec.created_at,
        "is_completed": is_completed,
        "materials": [
            {
                "id": m.id,
                "title": m.title,
                "file_path": m.file_path,
                "file_type": m.file_type,
                "file_size_bytes": m.file_size_bytes
            }
            for m in lec.materials
        ]
    }

@router.post("/{lecture_id}/complete")
def mark_lecture_completed(
    lecture_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["student"]))
):
    if not current_user.student_profile:
        raise HTTPException(status_code=400, detail="Student profile missing.")

    student_id = current_user.student_profile.id
    existing = db.query(LectureProgress).filter(
        LectureProgress.student_id == student_id,
        LectureProgress.lecture_id == lecture_id
    ).first()

    if existing:
        existing.is_completed = True
        existing.completed_at = datetime.utcnow()
    else:
        prog = LectureProgress(student_id=student_id, lecture_id=lecture_id, is_completed=True)
        db.add(prog)

    db.commit()
    return {"message": "Lecture marked as completed."}

@router.post("/{lecture_id}/materials")
async def upload_study_material(
    lecture_id: int,
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    lec = db.query(Lecture).filter(Lecture.id == lecture_id).first()
    if not lec:
        raise HTTPException(status_code=404, detail="Lecture not found.")

    clean_name, contents = await validate_and_read_upload(file, ALLOWED_MATERIAL_EXTENSIONS)
    stored_path = save_bytes(f"materials/{clean_name}", contents, content_type=file.content_type)

    material = StudyMaterial(
        lecture_id=lecture_id,
        title=title,
        file_path=stored_path,
        file_type=file.content_type or "application/octet-stream",
        file_size_bytes=len(contents)
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material
