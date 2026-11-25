from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    duration_weeks = Column(Integer, nullable=False, default=12)
    fee = Column(Numeric(10, 2), nullable=False, default=0.00)
    thumbnail_url = Column(String(500), nullable=True)
    status = Column(String(50), default="draft", index=True)  # 'draft', 'published', 'unpublished', 'archived'
    created_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    modules = relationship("CourseModule", back_populates="course", cascade="all, delete-orphan", order_by="CourseModule.sequence_order")
    batches = relationship("Batch", back_populates="course")
    certificates = relationship("Certificate", back_populates="course")
    payments = relationship("Payment", back_populates="course")
