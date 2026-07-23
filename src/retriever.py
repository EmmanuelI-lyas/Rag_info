"""
Creates and uses the document retriever.
"""

from src.vectordb import load_vector_db
from src.config import RETRIEVAL_K


class DocumentRetriever:

    def __init__(self):

        self.vector_db = load_vector_db()

        self.retriever = self.vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": RETRIEVAL_K
            }
        )

    def retrieve(self, query: str):
        """
        Retrieve candidate documents from Chroma.
        """

        documents = self.retriever.invoke(query)

        print("\n" + "=" * 70)
        print("Retriever")
        print("-" * 70)
        print(f"Retrieved {len(documents)} candidate documents")
        print("=" * 70 + "\n")

        return documents