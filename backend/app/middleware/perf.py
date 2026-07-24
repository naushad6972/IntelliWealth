import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)


async def performance_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = (time.perf_counter() - start) * 1000.0
    response.headers['X-Response-Time-ms'] = str(int(elapsed))
    if elapsed > 500:
        logger.warning(f"Slow request: {request.method} {request.url.path} took {elapsed:.1f}ms")
    return response
