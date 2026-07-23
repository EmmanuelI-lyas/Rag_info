"""
Abstract base class for all LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Callable, Optional


class BaseLLM(ABC):

    @abstractmethod
    def generate(
        self,
        prompt: str,
        stream_callback: Optional[Callable[[str], None]] = None,
    ) -> dict:
        """
        Generate a response.

        Parameters
        ----------
        prompt : str
            Prompt sent to the model.

        stream_callback : Callable | None
            Optional callback used to stream generated text
            back to the UI.

        Returns
        -------
        dict
            Standardized response dictionary.
        """
        pass