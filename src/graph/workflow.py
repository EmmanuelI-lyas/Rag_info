"""
Builds the LangGraph workflow.
"""

from langgraph.graph import StateGraph
from langgraph.graph import START, END

from src.graph.state import GraphState

from src.graph.nodes import (
    rewrite_node,
    retrieve_node,
    rerank_node,
    prompt_node,
    generate_node
)


def build_graph():

    builder = StateGraph(GraphState)

    # -----------------------------
    # Add Nodes
    # -----------------------------

    builder.add_node("rewrite", rewrite_node)

    builder.add_node("retrieve", retrieve_node)

    builder.add_node("rerank", rerank_node)

    builder.add_node("prompt", prompt_node)

    builder.add_node("generate", generate_node)

    # -----------------------------
    # Connect Nodes
    # -----------------------------

    builder.add_edge(START, "rewrite")

    builder.add_edge("rewrite", "retrieve")

    builder.add_edge("retrieve", "rerank")

    builder.add_edge("rerank", "prompt")

    builder.add_edge("prompt", "generate")

    builder.add_edge("generate", END)

    return builder.compile()