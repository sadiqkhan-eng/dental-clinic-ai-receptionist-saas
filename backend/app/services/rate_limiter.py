from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.cache import get_redis


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 60):
        super().__init__(app)
        self.rpm = requests_per_minute

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        try:
            r = await get_redis()
            current = await r.get(key)
            if current and int(current) >= self.rpm:
                raise HTTPException(status_code=429, detail="Too many requests")
            pipe = r.pipeline()
            pipe.incr(key)
            pipe.expire(key, 60)
            await pipe.execute()
        except HTTPException:
            raise
        except Exception:
            pass

        response = await call_next(request)
        return response
