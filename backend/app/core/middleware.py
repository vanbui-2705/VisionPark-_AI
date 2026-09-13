import logging
import re
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("visionpark.http")
CORRELATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Attach a safe correlation ID to the request, response and request log."""

    async def dispatch(self, request: Request, call_next):
        supplied_id = request.headers.get("X-Correlation-ID", "")
        correlation_id = (
            supplied_id if CORRELATION_ID_PATTERN.fullmatch(supplied_id) else str(uuid4())
        )
        request.state.correlation_id = correlation_id
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id
        duration_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            "%s %s -> %s in %.2f ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
            extra={"correlation_id": correlation_id},
        )
        return response
