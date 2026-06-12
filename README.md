---
title: E-Commerce AI Chatbot Backend
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🤖 E-Commerce AI Chatbot — Backend


Python-based REST API powering the AI shopping assistant, built with **FastAPI**, **uv**, and **Google Vertex AI Gemini 2.5 Pro**.

- [Frontend README](../ecommerce-ai-chatbot-ui/README.md) — React UI setup and component docs
- [Root README](../README.md) — Full project overview and architecture

---

## 🏗️ Architecture

```
backend/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Environment configuration & validation
│   ├── models/
│   │   └── schemas.py           # Pydantic v2 request/response schemas
│   ├── routers/
│   │   ├── chat.py              # POST /api/chat — AI conversation endpoint
│   │   └── products.py          # GET /api/products — product catalog endpoints
│   ├── services/
│   │   ├── llm_service.py       # Vertex AI Gemini 2.5 Pro integration
│   │   └── product_service.py   # In-memory product catalog (16 products)
│   └── middleware/
│       └── security.py          # Security headers middleware
├── pyproject.toml               # uv project manifest & dependencies
├── .env                         # Local environment variables
└── .venv/                       # Virtual environment (managed by uv)
```

---

## ⚡ Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Python | 3.11+ | [python.org](https://python.org) |
| uv | latest | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| gcloud CLI | latest | [cloud.google.com/sdk](https://cloud.google.com/sdk) |

### 1. Authenticate with Google Cloud

```bash
gcloud auth application-default login
```

> This sets up Application Default Credentials (ADC). No API keys are needed in code.

### 2. Install Dependencies

```bash
cd backend
uv sync
```

### 3. Configure Environment

Edit `backend/.env`:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GEMINI_MODEL=gemini-2.5-pro
APP_ENV=development
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
RATE_LIMIT_PER_MINUTE=60
```

> ⚠️ **Important:** `us-central1` is required for Gemini 2.5 Pro. Other regions may return a 404.

### 4. Start the Server

```bash
uv run uvicorn app.main:app --host localhost --port 8000 --reload
```

The API is available at **http://localhost:8000**

---

## 📡 API Reference

### Health Check

```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "development"
}
```

---

### Chat

```http
POST /api/chat
Content-Type: application/json
```

**Request body:**
```json
{
  "message": "Show me laptops under $1200",
  "conversation_history": [
    { "role": "user", "content": "Hello" },
    { "role": "assistant", "content": "Hi! How can I help?" }
  ],
  "session_id": "optional-uuid"
}
```

**Response:**
```json
{
  "message": "Here are some great laptops under $1200...",
  "session_id": "uuid-string"
}
```

**Rate limit:** 60 requests/minute per IP

---

### Products

```http
GET /api/products
```

**Query parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `category` | string | Filter by category name |
| `search` | string | Full-text search (name, description, tags, brand) |
| `min_price` | float | Minimum price |
| `max_price` | float | Maximum price |
| `in_stock_only` | bool | Show only in-stock items |
| `page` | int | Page number (default: 1) |
| `page_size` | int | Items per page (default: 12, max: 50) |

**Example:**
```http
GET /api/products?category=Electronics&max_price=500&page=1
```

---

```http
GET /api/products/{product_id}
```

Returns a single product by ID (e.g., `prod-001`).

---

## 🔧 Configuration Reference

All settings are loaded from `.env` via `pydantic-settings`. The app **fails loudly** at startup if required values are missing — no silent fallbacks.

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_CLOUD_PROJECT` | ✅ | — | GCP project ID |
| `GOOGLE_CLOUD_LOCATION` | No | `us-central1` | Vertex AI region |
| `GEMINI_MODEL` | No | `gemini-2.5-pro` | Model name |
| `APP_ENV` | No | `development` | `development` or `production` |
| `ALLOWED_ORIGINS` | No | `http://localhost:5173,...` | Comma-separated CORS origins |
| `RATE_LIMIT_PER_MINUTE` | No | `60` | Max requests per IP per minute |
| `MAX_MESSAGE_LENGTH` | No | `2000` | Max chat message length (chars) |
| `MAX_HISTORY_LENGTH` | No | `20` | Max conversation turns kept |

---

## 🔐 Security

| Threat | Mitigation |
|--------|-----------|
| Credential exposure | Google ADC — no keys in code or env |
| CORS abuse | Strict allow-list, no wildcards |
| DoS | `slowapi` rate limiter (60 req/min/IP) |
| Clickjacking | `X-Frame-Options: DENY` |
| MIME sniffing | `X-Content-Type-Options: nosniff` |
| Info leakage | Generic error messages to clients; detailed logs server-side |
| Input abuse | Pydantic v2 validation with max-length on all fields |
| LLM misuse | Vertex AI safety filters (BLOCK_MEDIUM_AND_ABOVE) |

### Security TODOs for Production

```python
# TODO(security): Add OAuth2/JWT authentication for user accounts
# TODO(security): Move to HTTPS with TLS termination (nginx/Cloud Run)
# TODO(security): Add CSRF tokens if cookie-based auth is introduced
# TODO(security): Use Google Secret Manager for any secrets beyond ADC
# TODO(security): Consider MFA for admin accounts
```

---

## 🧠 LLM Integration

The backend uses **Vertex AI SDK** (`google-cloud-aiplatform`) with **Application Default Credentials**.

### Model: `gemini-2.5-pro`

- **Region:** `us-central1` (required — other regions may not support this model)
- **Max output tokens:** 4096
- **Temperature:** 0.7
- **Safety settings:** BLOCK_MEDIUM_AND_ABOVE for all harm categories

### System Prompt Strategy

The LLM is initialized with:
1. A **role definition** (ShopBot persona)
2. The **full product catalog** as context (injected at startup)
3. Clear **behavioral guidelines** (only recommend real products, always mention prices, etc.)

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `google-cloud-aiplatform` | Vertex AI Gemini SDK |
| `pydantic` + `pydantic-settings` | Data validation & config |
| `slowapi` | Rate limiting |
| `python-dotenv` | `.env` file loading |
| `python-multipart` | Form data support |
| `httpx` | Async HTTP client |

---

## 🛠️ Development Commands

```bash
# Install all dependencies
uv sync

# Start dev server with hot-reload
uv run uvicorn app.main:app --host localhost --port 8000 --reload

# Run tests
uv run pytest

# Check Python formatting
uv run python -m py_compile app/**/*.py && echo "Syntax OK"

# Explore interactive API docs (development only)
open http://localhost:8000/docs
```

## 🚀 Production Deployment

### Option A: Hugging Face Spaces (Free Tier)
Deploy your container to Hugging Face Spaces for 24/7 free hosting.

1. **Create Space**:
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space).
   - Select **Docker** SDK → **Blank** template.
   - Set Space Hardware to **CPU basic (Free)** and visibility to **Public**.

2. **Add Remote & Push**:
   - From this directory, add the remote and push (mapping your local `master` branch to Hugging Face's default `main` branch):
     ```bash
     git remote add hf https://huggingface.co/spaces/<your-username>/<your-space-name>
     git push -f hf master:main
     ```

3. **Variables & Secrets**:
   - Go to the **Settings** tab in your Hugging Face Space → **Variables and secrets**.
   - Create a **Secret** named `GOOGLE_CREDENTIALS_JSON_STRING` and paste the entire JSON text from your Google Cloud Service Account Key file.
   - Create **Variables** for configuration:
     * `GOOGLE_CLOUD_PROJECT` = `your-active-gcp-project-id`
     * `GOOGLE_CLOUD_LOCATION` = `us-central1`
     * `GEMINI_MODEL` = `gemini-2.5-pro`
     * `APP_ENV` = `production`
     * `ALLOWED_ORIGINS` = `https://<your-vercel-domain>.vercel.app`
     * `RATE_LIMIT_PER_MINUTE` = `60`

---

### Option B: Google Cloud Run (Recommended for GCP)
Deploy a scalable serverless container directly inside your GCP Project.

```bash
# Deploy to Cloud Run (Google will automatically build the source using Dockerfile)
gcloud run deploy ecommerce-chatbot-backend \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=us-central1,GEMINI_MODEL=gemini-2.5-pro,APP_ENV=production,ALLOWED_ORIGINS=https://your-vercel-domain.vercel.app,RATE_LIMIT_PER_MINUTE=60"
```

> **Note:** In production, set `APP_ENV=production` to disable interactive docs `/docs` and the schema `/openapi.json` for security.

