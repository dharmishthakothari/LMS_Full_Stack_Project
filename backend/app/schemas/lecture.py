from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class StudyMaterialResponse(BaseModel):
    id: int
    lecture_id: int
    title: str
    file_path: str
    file_type: str
    file_size_bytes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LectureBase(BaseModel):
    module_id: int
    batch_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    sequence_order: int = 1
    video_url: Optional[str] = None
    duration_minutes: int = 60

class LectureCreate(LectureBase):
    pass

class LectureUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    sequence_order: Optional[int] = None
    video_url: Optional[str] = None
    duration_minutes: Optional[int] = None

class LectureResponse(LectureBase):
    id: int
    created_at: datetime
    is_completed: bool = False
    materials: List[StudyMaterialResponse] = []

    model_config = ConfigDict(from_attributes=True)
