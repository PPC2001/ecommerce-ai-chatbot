"""Products API router."""

import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.models.schemas import Product, ProductListResponse
from app.services.product_service import get_all_products, get_product_by_id

logger = logging.getLogger(__name__)
settings = get_settings()

limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=ProductListResponse)
async def list_products(
    category: Optional[str] = Query(default=None, max_length=64),
    search: Optional[str] = Query(default=None, max_length=200),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    in_stock_only: bool = Query(default=False),
    page: int = Query(default=1, ge=1, le=100),
    page_size: int = Query(default=12, ge=1, le=50),
) -> ProductListResponse:
    """
    List products with optional filtering and pagination.

    All query parameters are validated by FastAPI before reaching business logic.
    No raw SQL — uses in-memory filtering (safe from SQL injection).
    """
    products, total = get_all_products(
        category=category,
        search=search,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
        page=page,
        page_size=page_size,
    )

    return ProductListResponse(
        products=products,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str) -> Product:
    """
    Get a single product by ID.

    product_id is validated to be a safe string — no path traversal possible
    since we use dict lookup, not file paths.
    """
    # Validate product_id format (alphanumeric + hyphens only)
    if not product_id.replace("-", "").isalnum() or len(product_id) > 64:
        raise HTTPException(status_code=400, detail="Invalid product ID format.")

    product = get_product_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found.")

    return product
