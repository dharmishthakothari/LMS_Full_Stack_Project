from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    sequence_order = Column(Integer, nullable=False, default=1)
    video_url = Column(String(500), nullable=True)
    duration_minutes = Column(Integer, default=60)
    created_at = Column(DateTime, default=datetime.utcnow)

    module = relationship("CourseModule", back_populates="lectures")
    materials = relationship("StudyMaterial", back_populates="lecture", cascade="all, delete-orphan")
    progress_records = relationship("LectureProgress", back_populates="lecture", cascade="all, delete-orphan")
