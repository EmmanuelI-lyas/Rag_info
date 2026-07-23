"""
LangGraph Nodes

Each node performs one step of the RAG pipeline.
"""

from src.query import QueryRewriter
from src.retriever import DocumentRetriever
from src.retrieval import CrossEncoderReranker
from src.prompts.rag_prompt import PromptBuilder
from src.llm.manager import LLMManager

from src.config import FINAL_TOP_K


# --------------------------------------------------
# Shared Objects
# --------------------------------------------------

llm = LLMManager()

query_rewriter = QueryRewriter(llm)

retriever = DocumentRetriever()

reranker = CrossEncoderReranker()


# --------------------------------------------------
# Status Helper
# --------------------------------------------------

def _status(state, message):

    callback = state.get("status_callback")

    if callback is not None:

        callback(message)


# --------------------------------------------------
# Rewrite Node
# --------------------------------------------------

def rewrite_node(state):

    _status(state, "Rewriting your question...")

    rewritten_query = query_rewriter.rewrite(

        state["question"]

    )

    return {

        "rewritten_query": rewritten_query

    }


# --------------------------------------------------
# Retrieval Node
# --------------------------------------------------

def retrieve_node(state):

    _status(state, "Searching the report...")

    documents = retriever.retrieve(

        state["rewritten_query"]

    )

    return {

        "retrieved_documents": documents

    }


# --------------------------------------------------
# Reranking Node
# --------------------------------------------------

def rerank_node(state):

    _status(

        state,

        "Selecting the most relevant evidence..."

    )

    documents = reranker.rerank(

        query=state["rewritten_query"],

        documents=state["retrieved_documents"],

        top_k=FINAL_TOP_K

    )

    return {

        "reranked_documents": documents

    }


# --------------------------------------------------
# Prompt Node
# --------------------------------------------------

def prompt_node(state):

    _status(state, "Preparing the final prompt...")

    prompt = PromptBuilder.build_prompt(

        question=state["question"],

        documents=state["reranked_documents"]

    )

    return {

        "prompt": prompt

    }


# --------------------------------------------------
# Generation Node
# --------------------------------------------------

def generate_node(state):

    _status(state, "Generating answer...")

    result = llm.generate(

        prompt=state["prompt"],

        stream_callback=state.get("stream_callback")

    )

    return {

        "answer": result["response"],

        "provider": result["provider"],

        "model": result["model"],

        "success": result["success"],

        "error": result["error"]

    }