"""LLM Adapter for OpenAI-compatible API (sumopod).

This module handles all LLM API calls, providing async completion
and structured output parsing.
"""

import os
import json
import logging
from typing import Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class LLMAdapter:
    """Adapter for OpenAI-compatible chat completions API."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or os.getenv("SUMODOP_API_KEY")
        self.base_url = base_url or os.getenv(
            "SUMODOP_BASE_URL", "https://api.sumopod.com/v1"
        )
        self.model = model or os.getenv("SUMODOP_MODEL", "gpt-4o-mini")

        if not self.api_key:
            raise ValueError(
                "API key is required. Set SUMODOP_API_KEY in .env file "
                "or pass api_key parameter."
            )

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

    async def chat_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        """Send a chat completion request to the LLM.

        Args:
            system_prompt: System-level instructions for the model.
            user_prompt: The user's question or context.
            temperature: Sampling temperature (0.0-1.0).
            max_tokens: Maximum tokens in the response.

        Returns:
            The model's response text.
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content or ""

        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise

    async def structured_completion(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        max_tokens: int = 1024,
    ) -> dict:
        """Request a structured JSON response from the LLM.

        Args:
            system_prompt: System-level instructions (should request JSON).
            user_prompt: The user's question or context.
            temperature: Lower temperature for structured output.
            max_tokens: Maximum tokens in the response.

        Returns:
            Parsed JSON dictionary from the model response.
        """
        json_prompt = (
            f"{system_prompt}\n\n"
            "You MUST respond with valid JSON only. "
            "No markdown, no code fences, no explanations."
        )

        response = await self.chat_completion(
            system_prompt=json_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Clean response and parse JSON
        cleaned = response.strip()
        cleaned = cleaned.removeprefix("```json").removesuffix("```").strip()
        cleaned = cleaned.removeprefix("```").removesuffix("```").strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse structured response as JSON: {e}")
            logger.debug(f"Raw response: {cleaned}")
            return {"raw": cleaned}