"""Mock e-commerce product catalog service."""

from app.models.schemas import Product, ProductCategory, ProductRating

# ---------------------------------------------------------------------------
# Mock Product Catalog
# ---------------------------------------------------------------------------

PRODUCTS: list[Product] = [
    # Electronics
    Product(
        id="prod-001",
        sku="ELEC-LP-001",
        name="ProBook Ultra 15 Laptop",
        description="High-performance laptop with Intel Core i7, 16GB RAM, 512GB NVMe SSD, 15.6\" 4K OLED display. Perfect for professionals and creators.",
        price=1099.99,
        original_price=1299.99,
        category=ProductCategory.ELECTRONICS,
        tags=["laptop", "computer", "ultrabook", "professional", "intel", "4K"],
        rating=ProductRating(score=4.7, count=2341),
        in_stock=True,
        stock_count=45,
        image_url="https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400",
        brand="ProBook",
        discount_percent=15,
    ),
    Product(
        id="prod-002",
        sku="ELEC-PH-001",
        name="Galaxy Pro X Smartphone",
        description="Flagship smartphone with 6.7\" AMOLED display, 200MP camera system, 5000mAh battery, 5G connectivity. Capture life in stunning detail.",
        price=899.99,
        original_price=999.99,
        category=ProductCategory.ELECTRONICS,
        tags=["smartphone", "phone", "android", "5G", "camera", "flagship"],
        rating=ProductRating(score=4.8, count=5678),
        in_stock=True,
        stock_count=120,
        image_url="https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400",
        brand="Galaxy",
        discount_percent=10,
    ),
    Product(
        id="prod-003",
        sku="ELEC-HP-001",
        name="SoundMax Pro Wireless Headphones",
        description="Premium noise-cancelling headphones with 40-hour battery life, Hi-Res Audio, and multi-device pairing. Immersive sound in any environment.",
        price=249.99,
        original_price=299.99,
        category=ProductCategory.ELECTRONICS,
        tags=["headphones", "audio", "wireless", "noise-cancelling", "bluetooth"],
        rating=ProductRating(score=4.6, count=3892),
        in_stock=True,
        stock_count=89,
        image_url="https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        brand="SoundMax",
        discount_percent=17,
    ),
    Product(
        id="prod-004",
        sku="ELEC-WH-001",
        name="SmartWatch Series 8 Pro",
        description="Advanced smartwatch with health monitoring, GPS, ECG, blood oxygen tracking, 18-day battery life, and 45mm always-on display.",
        price=329.99,
        original_price=399.99,
        category=ProductCategory.ELECTRONICS,
        tags=["smartwatch", "wearable", "health", "fitness", "GPS", "ECG"],
        rating=ProductRating(score=4.5, count=1892),
        in_stock=True,
        stock_count=67,
        image_url="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
        brand="SmartTime",
        discount_percent=18,
    ),
    Product(
        id="prod-005",
        sku="ELEC-TAB-001",
        name="ArtTab Pro 12.9 Tablet",
        description="Professional creative tablet with 12.9\" Liquid Retina XDR display, M2 chip, Pencil support, and 10-hour battery. Create without limits.",
        price=799.99,
        original_price=899.99,
        category=ProductCategory.ELECTRONICS,
        tags=["tablet", "iPad", "drawing", "creative", "stylus", "professional"],
        rating=ProductRating(score=4.9, count=4201),
        in_stock=True,
        stock_count=34,
        image_url="https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
        brand="ArtTab",
        discount_percent=11,
    ),
    Product(
        id="prod-006",
        sku="ELEC-CAM-001",
        name="PhotoPro Alpha Camera",
        description="Full-frame mirrorless camera with 61MP sensor, 4K/120fps video, AI autofocus, weather-sealed body. For the serious photographer.",
        price=2799.99,
        category=ProductCategory.ELECTRONICS,
        tags=["camera", "photography", "mirrorless", "full-frame", "professional"],
        rating=ProductRating(score=4.8, count=876),
        in_stock=True,
        stock_count=15,
        image_url="https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400",
        brand="PhotoPro",
    ),
    # Clothing
    Product(
        id="prod-007",
        sku="CLTH-JKT-001",
        name="UltraFlex Windbreaker Jacket",
        description="Lightweight, water-resistant windbreaker perfect for outdoor adventures. Packable design, breathable fabric, with secure zip pockets.",
        price=89.99,
        original_price=119.99,
        category=ProductCategory.CLOTHING,
        tags=["jacket", "windbreaker", "outdoor", "waterproof", "packable"],
        rating=ProductRating(score=4.4, count=1245),
        in_stock=True,
        stock_count=203,
        image_url="https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400",
        brand="UltraFlex",
        discount_percent=25,
    ),
    Product(
        id="prod-008",
        sku="CLTH-SN-001",
        name="CloudStep Running Sneakers",
        description="Ultra-lightweight running shoes with responsive foam sole, breathable mesh upper, and enhanced arch support. Run further, feel better.",
        price=124.99,
        original_price=149.99,
        category=ProductCategory.CLOTHING,
        tags=["sneakers", "running", "shoes", "athletic", "lightweight"],
        rating=ProductRating(score=4.7, count=3456),
        in_stock=True,
        stock_count=156,
        image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
        brand="CloudStep",
        discount_percent=17,
    ),
    Product(
        id="prod-009",
        sku="CLTH-TS-001",
        name="Merino Wool Premium T-Shirt",
        description="Soft, odor-resistant merino wool t-shirt. Temperature-regulating, machine washable, and incredibly comfortable for everyday wear.",
        price=59.99,
        category=ProductCategory.CLOTHING,
        tags=["t-shirt", "merino wool", "casual", "everyday", "sustainable"],
        rating=ProductRating(score=4.6, count=2109),
        in_stock=True,
        stock_count=389,
        image_url="https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
        brand="MerinoLife",
    ),
    # Home & Garden
    Product(
        id="prod-010",
        sku="HOME-CF-001",
        name="BrewMaster Pro Coffee Machine",
        description="Professional-grade espresso machine with 15-bar pressure, built-in grinder, milk frother, and touchscreen interface. Café quality at home.",
        price=399.99,
        original_price=499.99,
        category=ProductCategory.HOME_GOODS,
        tags=["coffee", "espresso", "kitchen", "appliance", "home", "barista"],
        rating=ProductRating(score=4.8, count=2876),
        in_stock=True,
        stock_count=78,
        image_url="https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=400",
        brand="BrewMaster",
        discount_percent=20,
    ),
    Product(
        id="prod-011",
        sku="HOME-AIR-001",
        name="PureAir Smart Air Purifier",
        description="HEPA H13 air purifier covering 500 sq ft, removes 99.97% of particles, PM2.5 sensor, app control, ultra-quiet 22dB sleep mode.",
        price=199.99,
        original_price=249.99,
        category=ProductCategory.HOME_GOODS,
        tags=["air purifier", "HEPA", "home", "health", "smart", "air quality"],
        rating=ProductRating(score=4.7, count=1543),
        in_stock=True,
        stock_count=92,
        image_url="https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",
        brand="PureAir",
        discount_percent=20,
    ),
    Product(
        id="prod-012",
        sku="HOME-BED-001",
        name="CoolSleep Bamboo Bedding Set",
        description="Luxuriously soft bamboo sheets, temperature-regulating, hypoallergenic, and eco-friendly. Includes fitted sheet, flat sheet, and 2 pillowcases.",
        price=89.99,
        original_price=119.99,
        category=ProductCategory.HOME_GOODS,
        tags=["bedding", "bamboo", "sheets", "eco-friendly", "hypoallergenic"],
        rating=ProductRating(score=4.5, count=987),
        in_stock=True,
        stock_count=234,
        image_url="https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=400",
        brand="CoolSleep",
        discount_percent=25,
    ),
    # Sports
    Product(
        id="prod-013",
        sku="SPRT-YG-001",
        name="FlexFlow Yoga Mat Premium",
        description="6mm eco-friendly TPE yoga mat with non-slip surface, alignment lines, carry strap, and superior cushioning. 72\" x 24\" size.",
        price=49.99,
        original_price=64.99,
        category=ProductCategory.SPORTS,
        tags=["yoga", "fitness", "exercise", "mat", "eco-friendly", "non-slip"],
        rating=ProductRating(score=4.6, count=3201),
        in_stock=True,
        stock_count=312,
        image_url="https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400",
        brand="FlexFlow",
        discount_percent=23,
    ),
    Product(
        id="prod-014",
        sku="SPRT-BK-001",
        name="CarbonRide Pro Electric Bike",
        description="Electric mountain bike with 750W motor, 60-mile range, hydraulic disc brakes, 21-speed Shimano gears. Conquer any terrain effortlessly.",
        price=2199.99,
        original_price=2499.99,
        category=ProductCategory.SPORTS,
        tags=["electric bike", "e-bike", "cycling", "outdoor", "mountain bike"],
        rating=ProductRating(score=4.8, count=445),
        in_stock=True,
        stock_count=12,
        image_url="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
        brand="CarbonRide",
        discount_percent=12,
    ),
    # Books
    Product(
        id="prod-015",
        sku="BOOK-AI-001",
        name="The AI Revolution: Building the Future",
        description="Comprehensive guide to artificial intelligence, machine learning, and deep learning. Includes hands-on projects and real-world applications.",
        price=34.99,
        original_price=44.99,
        category=ProductCategory.BOOKS,
        tags=["AI", "machine learning", "tech", "programming", "data science"],
        rating=ProductRating(score=4.7, count=789),
        in_stock=True,
        stock_count=500,
        image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400",
        brand="TechPress",
        discount_percent=22,
    ),
    # Beauty
    Product(
        id="prod-016",
        sku="BEAU-SK-001",
        name="GlowLab Vitamin C Serum",
        description="Advanced brightening serum with 20% Vitamin C, hyaluronic acid, and niacinamide. Reduces dark spots, boosts collagen, and hydrates deeply.",
        price=44.99,
        original_price=59.99,
        category=ProductCategory.BEAUTY,
        tags=["skincare", "serum", "vitamin C", "brightening", "anti-aging"],
        rating=ProductRating(score=4.8, count=4521),
        in_stock=True,
        stock_count=678,
        image_url="https://images.unsplash.com/photo-1556228578-0d85b1a4d571?w=400",
        brand="GlowLab",
        discount_percent=25,
    ),
]

# Build lookup index for O(1) access
_PRODUCT_INDEX: dict[str, Product] = {p.id: p for p in PRODUCTS}


def get_all_products(
    category: str | None = None,
    search: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    in_stock_only: bool = False,
    page: int = 1,
    page_size: int = 12,
) -> tuple[list[Product], int]:
    """
    Filter and paginate products.
    Returns (products_page, total_count).
    """
    results = list(PRODUCTS)

    if category:
        results = [p for p in results if p.category.value.lower() == category.lower()]

    if search:
        # Safe string matching — no SQL, no eval
        search_lower = search.lower()
        results = [
            p
            for p in results
            if search_lower in p.name.lower()
            or search_lower in p.description.lower()
            or any(search_lower in tag.lower() for tag in p.tags)
            or search_lower in p.brand.lower()
        ]

    if min_price is not None:
        results = [p for p in results if p.price >= min_price]

    if max_price is not None:
        results = [p for p in results if p.price <= max_price]

    if in_stock_only:
        results = [p for p in results if p.in_stock]

    total = len(results)
    start = (page - 1) * page_size
    end = start + page_size
    return results[start:end], total


def get_product_by_id(product_id: str) -> Product | None:
    """Return a product by ID or None if not found."""
    return _PRODUCT_INDEX.get(product_id)


def get_catalog_summary() -> str:
    """
    Return a text summary of available products for the LLM system prompt.
    Keeps the summary compact to avoid bloating the context window.
    """
    categories: dict[str, list[str]] = {}
    for product in PRODUCTS:
        cat = product.category.value
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(f"{product.name} (${product.price:.2f})")

    lines = ["Available Product Catalog:"]
    for cat, items in categories.items():
        lines.append(f"\n{cat}:")
        for item in items:
            lines.append(f"  - {item}")
    return "\n".join(lines)
