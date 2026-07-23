"""
RAG Pipeline

Coordinates:
1. Query Rewriting
2. Retrieval
3. Reranking
4. Prompt Building
5. LLM Generation
"""

from src.retriever import DocumentRetriever
from src.retrieval import CrossEncoderReranker
from src.prompts.rag_prompt import PromptBuilder
from src.llm.manager import LLMManager
from src.query import QueryRewriter

from src.config import FINAL_TOP_K


class RAGPipeline:

    def __init__(self):

        self.retriever = DocumentRetriever()

        self.llm = LLMManager()

        self.query_rewriter = QueryRewriter(self.llm)

        self.reranker = CrossEncoderReranker()

    def ask(self, question: str):

        # ----------------------------------
        # Step 1 : Rewrite Query
        # ----------------------------------

        rewritten_query = self.query_rewriter.rewrite(question)

        # ----------------------------------
        # Step 2 : Retrieve Candidate Documents
        # ----------------------------------

        documents = self.retriever.retrieve(rewritten_query)

        # ----------------------------------
        # Step 3 : Rerank Documents
        # ----------------------------------

        documents = self.reranker.rerank(

            query=rewritten_query,

            documents=documents,

            top_k=FINAL_TOP_K

        )

        # ----------------------------------
        # Step 4 : Build Prompt
        # ----------------------------------

        prompt = PromptBuilder.build_prompt(

            question,

            documents

        )

        # ----------------------------------
        # Step 5 : Generate Answer
        # ----------------------------------

        result = self.llm.generate(prompt)

        # ----------------------------------
        # Step 6 : Return Everything
        # ----------------------------------

        return {

            "question": question,

            "rewritten_query": rewritten_query,

            "answer": result["response"],

            "provider": result["provider"],

            "model": result["model"],

            "documents": documents,

            "success": result["success"],

            "error": result["error"]

        }