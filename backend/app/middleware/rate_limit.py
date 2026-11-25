from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rate_limit import RateLimitEntry


class DatabaseRateLimiter:
    """Persistent sliding-window rate limiter backed by the relational database."""

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    def check(self, key: str, db: Session) -> None:
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=self.window_seconds)

        # Clean up expired entries for this client key
        db.query(RateLimitEntry).filter(
            RateLimitEntry.client_key == key,
            RateLimitEntry.created_at < cutoff,
        ).delete(synchronize_session=False)

        recent_count = (
            db.query(RateLimitEntry)
            .filter(
                RateLimitEntry.client_key == key,
                RateLimitEntry.created_at >= cutoff,
            )
            .count()
        )
        if recent_count >= self.max_requests:
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please wait a minute before trying again.",
            )

        db.add(RateLimitEntry(client_key=key, created_at=now))
        db.commit()


auth_rate_limiter = DatabaseRateLimiter(max_requests=30, window_seconds=60)


def rate_limit_auth(request: Request, db: Session = Depends(get_db)) -> None:
    client_ip = request.client.host if request.client else "unknown"
    auth_rate_limiter.check(f"auth:{client_ip}", db)
