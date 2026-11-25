from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="active") # active, completed, dropped

    __table_args__ = (
        UniqueConstraint("batch_id", "student_id", name="uq_batch_student"),
    )

    batch = relationship("Batch", back_populates="enrollments")
    student = relationship("Student", back_populates="enrollments")
