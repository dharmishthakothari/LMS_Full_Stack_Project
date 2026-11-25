from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    score = Column(Numeric(5, 2), default=0.00)
    is_passed = Column(Boolean, default=False)
    attempt_number = Column(Integer, default=1)

    quiz = relationship("Quiz", back_populates="attempts")
    student = relationship("Student", back_populates="quiz_attempts")
    answers = relationship("QuizAnswer", back_populates="attempt", cascade="all, delete-orphan")
