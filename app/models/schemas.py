"""Pydantic schemas for the E-Commerce AI Chatbot API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Chat Schemas
# ---------------------------------------------------------------------------


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    """A single chat message."""

    role: MessageRole
    content: str = Field(..., min_length=1, max_length=2000)

    @field_validator("content")
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        """Strip leading/trailing whitespace from message content."""
        return v.strip()


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's chat message",
    )
    conversation_history: list[Message] = Field(
        default_factory=list,
        max_length=20,
        description="Previous conversation turns (max 20)",
    )
    session_id: Optional[str] = Field(
        default=None,
        max_length=128,
        description="Optional session identifier",
    )

    @field_validator("message")
    @classmethod
    def sanitize_message(cls, v: str) -> str:
        return v.strip()


class ChatResponse(BaseModel):
    """Response body from the chat endpoint."""

    message: str
    session_id: Optional[str] = None
    suggested_products: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Product Schemas
# ---------------------------------------------------------------------------


class ProductCategory(str, Enum):
    ELECTRONICS = "Electronics"
    CLOTHING = "Clothing"
    HOME_GOODS = "Home & Garden"
    SPORTS = "Sports & Outdoors"
    BOOKS = "Books"
    BEAUTY = "Beauty & Personal Care"


class ProductRating(BaseModel):
    score: float = Field(..., ge=0.0, le=5.0)
    count: int = Field(..., ge=0)


class Product(BaseModel):
    """E-commerce product."""

    id: str
    name: str
    description: str
    price: float = Field(..., ge=0.0)
    original_price: Optional[float] = Field(default=None, ge=0.0)
    category: ProductCategory
    tags: list[str] = Field(default_factory=list)
    rating: ProductRating
    in_stock: bool = True
    stock_count: int = Field(default=0, ge=0)
    image_url: str
    brand: str
    sku: str
    discount_percent: Optional[int] = Field(default=None, ge=0, le=100)


class ProductListResponse(BaseModel):
    """Paginated product list response."""

    products: list[Product]
    total: int
    page: int
    page_size: int


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    environment: str
