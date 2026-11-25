from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    certificate_number = Column(String(100), unique=True, nullable=False, index=True)
    verification_id = Column(String(100), unique=True, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False)
    issue_date = Column(Date, default=date.today, nullable=False)
    pdf_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="certificates")
    course = relationship("Course", back_populates="certificates")
