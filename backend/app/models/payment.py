from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="RESTRICT"), nullable=False)
    total_fee = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False)
    pending_amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50), nullable=False) # UPI, NetBanking, Card, Cash
    transaction_reference = Column(String(100), unique=True, nullable=False)
    status = Column(String(50), default="paid") # paid, partially_paid, pending, failed, refunded
    receipt_path = Column(String(500), nullable=True)
    remarks = Column(String(255), nullable=True)
    recorded_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    student = relationship("Student", back_populates="payments")
    course = relationship("Course", back_populates="payments")
