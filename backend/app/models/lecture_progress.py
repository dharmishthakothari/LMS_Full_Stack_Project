from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class LectureProgress(Base):
    __tablename__ = "lecture_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    lecture_id = Column(Integer, ForeignKey("lectures.id", ondelete="CASCADE"), nullable=False)
    is_completed = Column(Boolean, default=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("student_id", "lecture_id", name="uq_student_lecture_progress"),
    )

    student = relationship("Student", back_populates="lecture_progress")
    lecture = relationship("Lecture", back_populates="progress_records")
