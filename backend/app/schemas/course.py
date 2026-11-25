from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class LectureSimpleResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    sequence_order: int
    duration_minutes: int
    video_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ModuleBase(BaseModel):
    title: str
    description: Optional[str] = None
    sequence_order: int = 1

class ModuleCreate(ModuleBase):
    course_id: int

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sequence_order: Optional[int] = None

class ModuleResponse(ModuleBase):
    id: int
    course_id: int
    created_at: datetime
    lectures: List[LectureSimpleResponse] = []

    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    title: str
    code: str
    category: str
    description: Optional[str] = None
    duration_weeks: int = 12
    fee: Decimal = Decimal("0.00")
    thumbnail_url: Optional[str] = None
    status: str = "draft"

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    duration_weeks: Optional[int] = None
    fee: Optional[Decimal] = None
    thumbnail_url: Optional[str] = None
    status: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    created_by_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    modules: List[ModuleResponse] = []

    model_config = ConfigDict(from_attributes=True)
