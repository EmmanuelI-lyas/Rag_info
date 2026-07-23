"""
Prompt builder for Retrieval-Augmented Generation (RAG).
"""

from langchain_core.documents import Document


class PromptBuilder:
    """
    Builds the final RAG prompt.
    """

    @staticmethod
    def build_context(documents: list[Document]) -> str:
        """
        Convert retrieved documents into a readable context.
        """

        context_parts = []

        for i, doc in enumerate(documents, start=1):

            page = doc.metadata.get("page", "N/A")
            source = doc.metadata.get("source", "Unknown")
            content_type = doc.metadata.get("content_type", "text")

            context_parts.append(
                f"""
==================== DOCUMENT {i} ====================

Source: {source}
Page: {page}
Type: {content_type}

{doc.page_content}
"""
            )

        return "\n".join(context_parts)

    @staticmethod
    def build_prompt(question: str, documents: list[Document]) -> str:
        """
        Build the final prompt sent to the LLM.
        """

        context = PromptBuilder.build_context(documents)

        return f"""
You are an expert financial research assistant.

Your job is to answer questions ONLY using the provided context.

Instructions:

1. Read ALL retrieved documents before answering.

2. If the answer can be reasonably inferred from the context,
   answer it in your own words.

3. You MAY summarize or combine information from multiple
   retrieved documents.

4. Do NOT invent facts that are not supported by the context.

5. Only respond with:

"I could not find this information in the provided document."

when the retrieved context genuinely contains no information
related to the user's question.

6. Keep answers concise unless the user asks for details.

==================== CONTEXT ====================

{context}

=================================================

Question:
{question}

Answer:
"""