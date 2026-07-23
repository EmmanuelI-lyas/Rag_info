"""
LLM Manager

Responsible for:
1. Choosing provider order
2. Handling failover
3. Returning first successful response
"""

from typing import Callable, Optional

from src.config import (
    PRIMARY_PROVIDER,
    FALLBACK_PROVIDERS,
)

from src.llm.gemini_provider import GeminiProvider
from src.llm.groq_provider import GroqProvider
from src.llm.openrouter_provider import OpenRouterProvider


class LLMManager:

    def __init__(self):

        self.providers = {
            "gemini": GeminiProvider(),
            "groq": GroqProvider(),
            "openrouter": OpenRouterProvider(),
        }

    # --------------------------------------------------
    # Provider Order
    # --------------------------------------------------

    def get_provider_order(self):

        order = [PRIMARY_PROVIDER]

        for provider in FALLBACK_PROVIDERS:

            if provider not in order:
                order.append(provider)

        return order

    # --------------------------------------------------
    # Generate
    # --------------------------------------------------

    def generate(
        self,
        prompt: str,
        stream_callback: Optional[Callable[[str], None]] = None,
    ):

        errors = []

        for provider_name in self.get_provider_order():

            provider = self.providers[provider_name]

            print(f"\nTrying {provider_name}...")

            result = provider.generate(
                prompt=prompt,
                stream_callback=stream_callback,
            )

            if result["success"]:

                print(f"✓ Success using {provider_name}")

                return result

            print(f"✗ Failed ({provider_name})")
            print(result["error"])

            errors.append(
                {
                    "provider": provider_name,
                    "error": result["error"],
                }
            )

        return {
            "success": False,
            "provider": None,
            "model": None,
            "response": None,
            "error": errors,
        }