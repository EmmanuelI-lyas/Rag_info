"""
Gemini Provider
"""

from typing import Callable

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
)

from src.llm.base import BaseLLM


class GeminiProvider(BaseLLM):

    def __init__(self):

        self.provider_name = "Gemini"

        self.model_name = GEMINI_MODEL

        self.llm = ChatGoogleGenerativeAI(

            model=self.model_name,

            google_api_key=GEMINI_API_KEY,

            temperature=TEMPERATURE,

            max_output_tokens=MAX_TOKENS,

        )

    def generate(

        self,

        prompt: str,

        stream_callback: Callable | None = None,

    ):
        """
        Generates a response from Gemini.

        stream_callback is reserved for future token streaming.
        """

        try:

            response = self.llm.invoke(prompt)

            content = response.content

            if isinstance(content, list):

                text = ""

                for item in content:

                    if isinstance(item, dict):

                        text += item.get("text", "")

                    else:

                        text += str(item)

            else:

                text = content

            # Reserved for future streaming
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