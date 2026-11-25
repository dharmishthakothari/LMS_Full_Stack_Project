from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    target_role = Column(String(50), default="all") # all, admin, instructor, student
    target_batch_id = Column(Integer, ForeignKey("batches.id", ondelete="SET NULL"), nullable=True)
    published_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    batch = relationship("Batch", back_populates="announcements")
