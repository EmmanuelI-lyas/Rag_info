"""
Query Rewriter

Rewrites user queries to improve semantic retrieval.
"""

from src.llm.manager import LLMManager
from src.prompts.rewrite_prompt import REWRITE_PROMPT


class QueryRewriter:

    def __init__(self, llm_manager):

        self.llm = llm_manager

    def rewrite(self, query: str) -> str:

        prompt = REWRITE_PROMPT.format(query=query)

        result = self.llm.generate(prompt)

        if result["success"]:

            rewritten = result["response"].strip()

            print("\n" + "=" * 70)
            print("Query Rewriter")
            print("-" * 70)
            print(f"Original : {query}")
            print(f"Rewritten: {rewritten}")
            print("=" * 70 + "\n")

            return rewritten

        print("Query rewriting failed. Using original query.")

        return query