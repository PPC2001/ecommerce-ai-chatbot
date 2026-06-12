"""Security headers middleware for FastAPI."""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Injects security headers into all HTTP responses.

    Headers implemented:
    - Content-Security-Policy: Strict policy restricting resource origins
    - X-Content-Type-Options: Prevents MIME-type sniffing
    - X-Frame-Options: Prevents clickjacking
    - Referrer-Policy: Controls referrer information
    - Permissions-Policy: Disables unused browser features
    - Cache-Control: Prevents caching of sensitive API responses
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        response: Response = await call_next(request)

        # Strict CSP — API only serves JSON, no scripts/styles needed
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; "
            "frame-ancestors 'none';"
        )

        # Prevent MIME-type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"

        # Strict referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Disable unused browser features
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), "
            "payment=(), usb=(), interest-cohort=()"
        )

        # Prevent caching of API responses (contains potentially sensitive data)
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"

        # Remove potentially revealing server headers
        # MutableHeaders uses __delitem__, not .pop()
        for header in ("server", "x-powered-by"):
            if header in response.headers:
                del response.headers[header]

        return response
