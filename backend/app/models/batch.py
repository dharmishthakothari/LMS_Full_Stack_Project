from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Batch(Base):
    __tablename__ = "batches"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False)
    instructor_id = Column(Integer, ForeignKey("instructors.id", ondelete="SET NULL"), nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    class_days = Column(String(100), nullable=False)  # e.g., "Mon, Wed, Fri"
    class_timing = Column(String(100), nullable=False) # e.g., "10:00 AM - 12:00 PM"
    capacity = Column(Integer, nullable=False, default=30)
    status = Column(String(50), default="upcoming", index=True) # upcoming, active, completed, closed, archived
    created_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="batches")
    instructor = relationship("Instructor", back_populates="batches")
    enrollments = relationship("Enrollment", back_populates="batch", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="batch", cascade="all, delete-orphan")
    quizzes = relationship("Quiz", back_populates="batch", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="batch", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="batch")
