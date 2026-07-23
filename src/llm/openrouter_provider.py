"""
OpenRouter Provider
"""

from typing import Callable

from langchain_openai import ChatOpenAI

from src.config import (
    OPENROUTER_API_KEY,
    TEMPERATURE,
    MAX_TOKENS,
)

from src.llm.base import BaseLLM


class OpenRouterProvider(BaseLLM):

    def __init__(self):

        self.provider_name = "OpenRouter"

        self.model_name = "meta-llama/llama-3.3-70b-instruct:free"

        self.llm = ChatOpenAI(

            api_key=OPENROUTER_API_KEY,

            base_url="https://openrouter.ai/api/v1",

            model=self.model_name,

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS,

        )

    def generate(

        self,

        prompt: str,

        stream_callback: Callable | None = None,

    ):

        try:

            response = self.llm.invoke(prompt)

            text = response.content

            # Reserved for future token streaming
            if stream_callback is not None:

                stream_callback(text)

            return {

                "success": True,

                "provider": self.provider_name,

                "model": self.model_name,

                "response": text,

                "error": None,

            }

        except Exception as e:

            return {

                "success": False,

                "provider": self.provider_name,

                "model": self.model_name,

                "response": None,

                "error": str(e),

            }