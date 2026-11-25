from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CourseModule, Course, User
from app.schemas.course import ModuleCreate, ModuleUpdate, ModuleResponse
from app.dependencies.auth import require_role

router = APIRouter(prefix="/api/modules", tags=["Course Modules"])

@router.post("", response_model=ModuleResponse)
def create_module(
    data: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")

    mod = CourseModule(
        course_id=data.course_id,
        title=data.title,
        description=data.description,
        sequence_order=data.sequence_order
    )
    db.add(mod)
    db.commit()
    db.refresh(mod)
    return mod

@router.put("/{module_id}", response_model=ModuleResponse)
def update_module(
    module_id: int,
    data: ModuleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin", "instructor"]))
):
    mod = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found.")

    for key, val in data.dict(exclude_unset=True).items():
        setattr(mod, key, val)

    db.commit()
    db.refresh(mod)
    return mod

@router.delete("/{module_id}")
def delete_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    mod = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not mod:
        raise HTTPException(status_code=404, detail="Module not found.")
    
    db.delete(mod)
    db.commit()
    return {"message": "Module deleted successfully."}
