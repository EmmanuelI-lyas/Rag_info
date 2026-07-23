"""
Groq Provider
"""

from typing import Callable

from langchain_groq import ChatGroq

from src.config import (
    GROQ_API_KEY,
    TEMPERATURE,
    MAX_TOKENS
)

from src.llm.base import BaseLLM


class GroqProvider(BaseLLM):

    def __init__(self):

        self.provider_name = "Groq"

        self.model_name = "llama-3.3-70b-versatile"

        self.llm = ChatGroq(

            api_key=GROQ_API_KEY,

            model=self.model_name,

            temperature=TEMPERATURE,

            max_tokens=MAX_TOKENS

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

                "error": None

            }

        except Exception as e:

            return {

                "success": False,

                "provider": self.provider_name,

                "model": self.model_name,

                "response": None,

                "error": str(e)

            }