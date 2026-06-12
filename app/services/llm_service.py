"""
Vertex AI Gemini LLM service for the e-commerce AI chatbot.
Uses google-cloud-aiplatform SDK with Application Default Credentials (ADC).
No API keys are handled here — authentication is via gcloud ADC or Workload Identity.
"""

import logging
from functools import lru_cache

import vertexai
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    SafetySetting,
)

from app.config import Settings, get_settings
from app.models.schemas import Message, MessageRole
from app.services.product_service import get_catalog_summary

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Safety settings — block harmful content
# ---------------------------------------------------------------------------
SAFETY_SETTINGS = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    ),
]

GENERATION_CONFIG = GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    max_output_tokens=4096,  # 2.5 Pro supports up to 65K output tokens
    candidate_count=1,
)

SYSTEM_INSTRUCTION = """You are ShopBot, an intelligent and friendly AI shopping assistant for our e-commerce marketplace. Your goal is to help customers find the perfect products, answer questions, and make their shopping experience delightful.

Your capabilities:
- Recommend products based on customer needs, budget, and preferences
- Compare products across categories (Electronics, Clothing, Home & Garden, Sports, Books, Beauty)
- Answer questions about product features, pricing, and availability
- Help with gift ideas and outfit suggestions
- Provide shopping advice and tips
- Assist with order-related questions

Your personality:
- Friendly, enthusiastic, and helpful
- Concise but informative — don't overwhelm with too much text
- Use emojis sparingly to add warmth
- Always be honest about limitations

Guidelines:
- Only recommend products from our actual catalog (listed below)
- Always mention prices when recommending products
- Highlight discounts and deals when relevant
- If a customer asks about something not in our catalog, suggest the closest alternative
- Never make up product details — stick to the catalog data provided
- Keep responses focused and actionable

{catalog}

Remember: You're here to help customers find exactly what they need. Be their personal shopping expert!"""


class LLMService:
    """Service for interacting with Google Vertex AI Gemini models."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._initialized = False
        self._model: GenerativeModel | None = None

    def _ensure_initialized(self) -> None:
        """Lazy initialization of Vertex AI to avoid startup delays."""
        if self._initialized:
            return

        try:
            vertexai.init(
                project=self._settings.google_cloud_project,
                location=self._settings.google_cloud_location,
            )

            catalog_text = get_catalog_summary()
            system_prompt = SYSTEM_INSTRUCTION.format(catalog=catalog_text)

            self._model = GenerativeModel(
                model_name=self._settings.gemini_model,
                system_instruction=system_prompt,
            )

            self._initialized = True
            logger.info(
                "Vertex AI initialized: project=%s, location=%s, model=%s",
                self._settings.google_cloud_project,
                self._settings.google_cloud_location,
                self._settings.gemini_model,
            )
        except Exception as exc:
            logger.error("Failed to initialize Vertex AI: %s", exc)
            raise RuntimeError(
                f"Vertex AI initialization failed: {exc}. "
                "Ensure Application Default Credentials are configured "
                "(run 'gcloud auth application-default login')."
            ) from exc

    def _build_history(self, history: list[Message]) -> list[Content]:
        """Convert our message schema to Vertex AI Content objects."""
        contents = []
        for msg in history:
            if msg.role == MessageRole.SYSTEM:
                continue  # System messages handled via system_instruction
            role = "user" if msg.role == MessageRole.USER else "model"
            contents.append(
                Content(role=role, parts=[Part.from_text(msg.content)])
            )
        return contents

    async def chat(
        self,
        user_message: str,
        conversation_history: list[Message],
    ) -> str:
        """
        Send a message to Gemini and return the response.

        Args:
            user_message: The user's latest message (already validated/trimmed).
            conversation_history: Previous turns in the conversation.

        Returns:
            The assistant's response text.
        """
        self._ensure_initialized()

        if self._model is None:
            raise RuntimeError("LLM model is not initialized.")

        try:
            history = self._build_history(conversation_history)
            chat_session = self._model.start_chat(history=history)

            response = await chat_session.send_message_async(
                user_message,
                generation_config=GENERATION_CONFIG,
                safety_settings=SAFETY_SETTINGS,
            )

            if not response.candidates:
                logger.warning("Gemini returned no candidates for message.")
                return (
                    "I'm sorry, I couldn't generate a response. "
                    "Please try rephrasing your question."
                )

            response_text = response.text
            logger.info(
                "Chat response generated: input_tokens=%s, output_tokens=%s",
                response.usage_metadata.prompt_token_count if response.usage_metadata else "unknown",
                response.usage_metadata.candidates_token_count if response.usage_metadata else "unknown",
            )

            return response_text

        except Exception as exc:
            # Log detailed error for developers, return generic message to user
            logger.error("LLM chat error: %s", exc, exc_info=True)
            raise RuntimeError(
                "An error occurred while processing your request."
            ) from exc


@lru_cache(maxsize=1)
def get_llm_service() -> LLMService:
    """Return cached LLM service singleton."""
    settings = get_settings()
    return LLMService(settings)
