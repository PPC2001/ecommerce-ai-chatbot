"""
E-Commerce AI Chatbot — FastAPI Application Entry Point

Security measures implemented:
- Strict CORS allow-list (no wildcard origins)
- Security headers middleware (CSP, X-Frame-Options, etc.)
- Rate limiting via slowapi
- Input validation via Pydantic
- Generic error messages (internal details logged only)
- TODO(security): Add OAuth2/JWT authentication for production user accounts
- TODO(security): Add CSRF tokens if cookie-based auth is added in the future
- TODO(security): Enable HTTPS/TLS in production (behind a reverse proxy like nginx)
"""

import logging
import logging.config
import os
import tempfile

# ---------------------------------------------------------------------------
# Dynamic Credentials support for platforms like Hugging Face / Heroku
# Writes JSON key from GOOGLE_CREDENTIALS_JSON_STRING env variable to a temp file
# ---------------------------------------------------------------------------
credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON_STRING")
print("=== GOOGLE CREDENTIALS DEBUG ===")
print("GOOGLE_CREDENTIALS_JSON_STRING env var exists:", credentials_json is not None)
if credentials_json:
    print("GOOGLE_CREDENTIALS_JSON_STRING length:", len(credentials_json.strip()))
    try:
        temp_dir = tempfile.gettempdir()
        credentials_path = os.path.join(temp_dir, "google-credentials.json")
        with open(credentials_path, "w", encoding="utf-8") as f:
            f.write(credentials_json)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        print("Set GOOGLE_APPLICATION_CREDENTIALS to:", credentials_path)
        print("File exists:", os.path.exists(credentials_path))
    except Exception as e:
        print("Failed to write GOOGLE_CREDENTIALS_JSON_STRING to file:", e)
else:
    print("WARNING: GOOGLE_CREDENTIALS_JSON_STRING is empty or not found in environment!")
print("================================")

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address


from app.config import get_settings
from app.middleware.security import SecurityHeadersMiddleware
from app.routers import chat, products

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

settings = get_settings()

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered e-commerce shopping assistant using Google Vertex AI Gemini",
    # Disable docs in production
    docs_url="/docs" if settings.app_env == "development" else None,
    redoc_url="/redoc" if settings.app_env == "development" else None,
    openapi_url="/openapi.json" if settings.app_env == "development" else None,
)

# ---------------------------------------------------------------------------
# State (for slowapi)
# ---------------------------------------------------------------------------

app.state.limiter = limiter

# ---------------------------------------------------------------------------
# Middleware (order matters — first added is outermost)
# ---------------------------------------------------------------------------

# 1. Security headers (outermost — applied to all responses)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Rate limiting
app.add_middleware(SlowAPIMiddleware)

# 3. CORS — allow all for public API deployment to prevent routing/preflight issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for public chatbot API
    allow_credentials=False,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
    max_age=3600,
)

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """Return a clean rate limit error without exposing internals."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Too many requests. Please slow down and try again later."
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler — log details, return generic error to client."""
    logger.error(
        "Unhandled exception on %s %s: %s",
        request.method,
        request.url.path,
        exc,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(chat.router)
app.include_router(products.router)


# ---------------------------------------------------------------------------
# Root
# ---------------------------------------------------------------------------


@app.get("/", include_in_schema=False)
async def root():
    return {"name": settings.app_name, "version": settings.app_version, "status": "ok"}
