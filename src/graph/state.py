"""
Graph State

Shared state passed between LangGraph nodes.
"""

from typing import TypedDict, Callable
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):
    """
    Shared state for the RAG workflow.
    """

    # --------------------------------------------------
    # User Input
    # --------------------------------------------------

    question: str

    # --------------------------------------------------
    # Query Rewriting
    # --------------------------------------------------

    rewritten_query: str

    # --------------------------------------------------
    # Retrieval
    # --------------------------------------------------

    retrieved_documents: list[Document]

    # --------------------------------------------------
    # Reranking
    # --------------------------------------------------

    reranked_documents: list[Document]

    # --------------------------------------------------
    # Prompt
    # --------------------------------------------------

    prompt: str

    # --------------------------------------------------
    # LLM Output
    # --------------------------------------------------

    answer: str

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    provider: str

    model: str

    success: bool

    error: str

    # --------------------------------------------------
    # UI Callbacks (Optional)
    # --------------------------------------------------

    status_callback: Callable[[str], None]

    stream_callback: Callable[[str], None]