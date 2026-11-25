from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Role, Student, Instructor
from app.schemas.user import UserResponse, UserCreate, UserUpdate, RoleResponse
from app.dependencies.auth import get_current_user, require_role
from app.utils.security import get_password_hash

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.get("", response_model=List[UserResponse])
def get_users(
    role: Optional[str] = None,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    query = db.query(User).join(Role)
    if role:
        query = query.filter(Role.name == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.email.like(search_filter)) |
            (User.first_name.like(search_filter)) |
            (User.last_name.like(search_filter))
        )
    return query.order_by(User.id.desc()).all()

@router.post("", response_model=UserResponse)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    role = db.query(Role).filter(Role.name == data.role_name).first()
    if not role:
        raise HTTPException(status_code=400, detail=f"Role '{data.role_name}' does not exist.")

    user = User(
        email=data.email,
        password_hash=get_password_hash(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        phone=data.phone,
        role_id=role.id,
        is_active=data.is_active
    )
    db.add(user)
    db.flush()

    if data.role_name == "instructor":
        instructor = Instructor(
            user_id=user.id,
            expertise=data.expertise or "General Technical Instruction",
            qualification=data.qualification or "Professional Certification",
            biography="Institute faculty member."
        )
        db.add(instructor)
    elif data.role_name == "student":
        student = Student(
            user_id=user.id,
            address=data.address,
            date_of_birth=data.date_of_birth
        )
        db.add(student)

    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if data.first_name is not None:
        user.first_name = data.first_name
    if data.last_name is not None:
        user.last_name = data.last_name
    if data.phone is not None:
        user.phone = data.phone
    if data.profile_image is not None:
        user.profile_image = data.profile_image
    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(["admin"]))
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot deactivate your own administrator account.")
    
    user.is_active = False
    db.commit()
    return {"message": "User account deactivated successfully."}
