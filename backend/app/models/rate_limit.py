from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class RateLimitEntry(Base):
    """Persistent sliding-window rate limit hit log stored in the database."""
    __tablename__ = "rate_limit_entries"

    id = Column(Integer, primary_key=True, index=True)
    client_key = Column(String(128), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
