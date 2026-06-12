"""Chat API router with rate limiting."""

import logging
import uuid

from fastapi import APIRouter, HTTPException, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.models.schemas import ChatRequest, ChatResponse, HealthResponse
from app.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api", tags=["chat"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint — returns app status."""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
    )


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(f"{settings.rate_limit_per_minute}/minute")
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    """
    Process a chat message and return an AI response.

    Security measures:
    - Rate limited to 60 requests/minute per IP
    - Input validated and length-capped by Pydantic schema
    - Generic error messages returned to client (details logged server-side)
    - No user credentials or sensitive data logged
    """
    llm_service = get_llm_service()

    # Generate session ID if not provided
    session_id = body.session_id or str(uuid.uuid4())

    # Log request (without message content to avoid PII in logs)
    logger.info(
        "Chat request: session=%s, history_length=%d",
        session_id,
        len(body.conversation_history),
    )

    try:
        response_text = await llm_service.chat(
            user_message=body.message,
            conversation_history=body.conversation_history,
        )
    except RuntimeError as exc:
        # Log detailed error for developers
        logger.error("Chat processing failed: %s", exc, exc_info=True)
        # Return generic message to user — do NOT expose internal details
        raise HTTPException(
            status_code=503,
            detail=(
                "Our AI assistant is temporarily unavailable. "
                "Please try again in a moment."
            ),
        ) from exc
    except Exception as exc:
        logger.error("Unexpected chat error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again.",
        ) from exc

    return ChatResponse(
        message=response_text,
        session_id=session_id,
    )
