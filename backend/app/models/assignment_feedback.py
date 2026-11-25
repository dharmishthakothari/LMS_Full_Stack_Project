from datetime import datetime
from sqlalchemy import Column, Integer, Numeric, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class AssignmentFeedback(Base):
    __tablename__ = "assignment_feedback"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id", ondelete="CASCADE"), unique=True, nullable=False)
    evaluated_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    marks_obtained = Column(Numeric(5, 2), nullable=False)
    feedback_text = Column(Text, nullable=True)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="feedback")
