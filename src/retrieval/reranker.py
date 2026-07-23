"""
Cross-Encoder Reranker

Re-ranks retrieved documents using a CrossEncoder model.
"""

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        print("Loading CrossEncoder Reranker...")

        self.model = CrossEncoder(model_name)

        print("✓ CrossEncoder Loaded")

    def rerank(
        self,
        query: str,
        documents: list,
        top_k: int = 5
    ):

        if not documents:
            return []

        # ----------------------------------
        # Create query-document pairs
        # ----------------------------------

        pairs = [

            (query, doc.page_content)

            for doc in documents

        ]

        # ----------------------------------
        # Predict relevance scores
        # ----------------------------------

        scores = self.model.predict(pairs)

        # ----------------------------------
        # Combine documents with scores
        # ----------------------------------

        ranked = list(

            zip(documents, scores)

        )

        # ----------------------------------
        # Sort by score (highest first)
        # ----------------------------------

        ranked.sort(

            key=lambda x: x[1],

            reverse=True

        )

        print("\n" + "=" * 70)
        print("CrossEncoder Reranking")
        print("-" * 70)

        for i, (_, score) in enumerate(ranked[:top_k], start=1):

            print(f"{i}. Score = {score:.4f}")

        print("=" * 70 + "\n")

        # ----------------------------------
        # Return top documents only
        # ----------------------------------

        return [

            doc

            for doc, _ in ranked[:top_k]

        ]