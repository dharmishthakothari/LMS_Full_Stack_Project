import time
from collections import defaultdict
from threading import Lock
from fastapi import HTTPException, Request, status

class InMemoryRateLimiter:
    """Sliding-window rate limiter for sensitive authentication endpoints."""

    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits = defaultdict(list)
        self._lock = Lock()

    def check(self, key: str) -> None:
        now = time.time()
        cutoff = now - self.window_seconds
        with self._lock:
            timestamps = [t for t in self._hits[key] if t > cutoff]
            if len(timestamps) >= self.max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please wait a minute before trying again."
                )
            timestamps.append(now)
            self._hits[key] = timestamps

auth_rate_limiter = InMemoryRateLimiter(max_requests=30, window_seconds=60)

def rate_limit_auth(request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    auth_rate_limiter.check(f"auth:{client_ip}")
