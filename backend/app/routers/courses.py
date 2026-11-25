from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Course, CourseModule, User, Batch, Enrollment
from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate
from app.dependencies.auth import get_current_user, require_role

router = APIRouter(prefix="/api/courses", tags=["Courses"])

@router.get("", response_model=List[CourseResponse])
def get_courses(
    category: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Course)
    if current_user.role.name == "student":
        # Students only see published courses or courses they are enrolled in
        query = query.filter(Course.status.in_(["published"]))
    elif status:
        query = query.filter(Course.status == status)

    if category:
        query = query.filter(Course.category == category)
    if search:
        s = f"%{search}%"
        query = query.filter((Course.title.like(s)) | (Course.code.like(s)) | (Course.description.like(s)))
    
    return query.order_by(Course.id.desc()).all()

@router.post("", response_model=CourseResponse)
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    existing = db.query(Course).filter(Course.code == data.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists.")
    
    course = Course(
        title=data.title,
        code=data.code,
        category=data.category,
        description=data.description,
        duration_weeks=data.duration_weeks,
        fee=data.fee,
        thumbnail_url=data.thumbnail_url,
        status=data.status,
        created_by_id=current_user.id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

@router.get("/{course_id}", response_model=CourseResponse)
def get_course_details(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    data: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    
    for key, val in data.dict(exclude_unset=True).items():
        setattr(course, key, val)

    db.commit()
    db.refresh(course)
    return course

@router.delete("/{course_id}")
def delete_or_archive_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    
    # Check if batches or enrollments exist
    has_batches = db.query(Batch).filter(Batch.course_id == course_id).count() > 0
    if has_batches:
        course.status = "archived"
        db.commit()
        return {"message": "Course has active dependent batches/records. It has been safely archived."}
    
    db.delete(course)
    db.commit()
    return {"message": "Course deleted successfully."}
