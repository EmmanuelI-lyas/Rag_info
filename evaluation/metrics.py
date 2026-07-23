"""
Custom Evaluation Metrics
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --------------------------------------------------
# Load embedding model once
# --------------------------------------------------

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# Helper
# --------------------------------------------------

def embed(texts):
    """
    Encode one string or a list of strings.
    """
    return embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )


# --------------------------------------------------
# Semantic Similarity
# --------------------------------------------------

def semantic_similarity(
    answer: str,
    ground_truth: str
):

    embeddings = embed([answer, ground_truth])

    score = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(score)


# --------------------------------------------------
# Retrieval Hit
# --------------------------------------------------

def retrieval_hit(
    ground_truth: str,
    contexts: list[str]
):
    """
    Returns 1 if at least one retrieved chunk
    is semantically similar to the ground truth.
    """

    if len(contexts) == 0:
        return 0

    embeddings = embed([ground_truth] + contexts)

    gt = embeddings[0]

    best_score = 0

    for ctx in embeddings[1:]:

        score = cosine_similarity(
            [gt],
            [ctx]
        )[0][0]

        best_score = max(best_score, score)

    return int(best_score >= 0.60)


# --------------------------------------------------
# Context Precision
# --------------------------------------------------

def context_precision(
    ground_truth: str,
    contexts: list[str]
):
    """
    Average semantic similarity between
    ground truth and retrieved chunks.
    """

    if len(contexts) == 0:
        return 0.0

    embeddings = embed([ground_truth] + contexts)

    gt = embeddings[0]

    scores = []

    for ctx in embeddings[1:]:

        sim = cosine_similarity(
            [gt],
            [ctx]
        )[0][0]

        scores.append(sim)

    return float(np.mean(scores))


# --------------------------------------------------
# Exact Match
# --------------------------------------------------

def exact_match(
    answer: str,
    ground_truth: str
):

    return int(
        answer.strip().lower()
        ==
        ground_truth.strip().lower()
    )