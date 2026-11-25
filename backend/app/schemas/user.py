from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict

class RoleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role_name: str  # admin, instructor, student
    # Optional profile fields
    expertise: Optional[str] = None
    qualification: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    profile_image: Optional[str] = None
    is_active: Optional[bool] = None

class InstructorProfileResponse(BaseModel):
    id: int
    expertise: Optional[str] = None
    qualification: Optional[str] = None
    biography: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class StudentProfileResponse(BaseModel):
    id: int
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    emergency_contact: Optional[str] = None
    joining_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserBase):
    id: int
    profile_image: Optional[str] = None
    created_at: datetime
    role: RoleResponse
    instructor_profile: Optional[InstructorProfileResponse] = None
    student_profile: Optional[StudentProfileResponse] = None

    model_config = ConfigDict(from_attributes=True)
