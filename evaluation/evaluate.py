"""
Runs evaluation on the Financial RAG System.
"""

import json
import csv
import time
import sys
from pathlib import Path

# --------------------------------------------------
# Project Root
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT))

# --------------------------------------------------

from src.graph.workflow import build_graph

from evaluation.metrics import (
    semantic_similarity,
    retrieval_hit,
    context_precision,
    exact_match,
)

# --------------------------------------------------
# Paths
# --------------------------------------------------

DATASET_PATH = r"D:\Rag\evaluation\dataset.json"
OUTPUT_PATH =  r"D:\Rag\evaluation\results.csv"

# --------------------------------------------------
# Load LangGraph
# --------------------------------------------------

graph = build_graph()

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------

semantic_scores = []
retrieval_scores = []
precision_scores = []
exact_scores = []
latency_scores = []

with open(OUTPUT_PATH, "w", newline="", encoding="utf-8") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow(
        [
            "ID",
            "Question",
            "SemanticSimilarity",
            "RetrievalHit",
            "ContextPrecision",
            "ExactMatch",
            "LatencySeconds",
        ]
    )

    for sample in dataset:

        question = sample["question"]
        ground_truth = sample["ground_truth"]

        print("=" * 70)
        print(question)

        start = time.time()

        result = graph.invoke(
            {
                "question": question
            }
        )

        latency = time.time() - start

        generated_answer = result["answer"]

        contexts = [
            doc.page_content
            for doc in result["reranked_documents"]
        ]

        semantic = semantic_similarity(
            generated_answer,
            ground_truth,
        )

        retrieval = retrieval_hit(
            ground_truth,
            contexts,
        )

        precision = context_precision(
            ground_truth,
            contexts,
        )

        exact = exact_match(
            generated_answer,
            ground_truth,
        )

        writer.writerow(
            [
                sample["id"],
                question,
                round(semantic, 3),
                retrieval,
                round(precision, 3),
                exact,
                round(latency, 2),
            ]
        )

        semantic_scores.append(semantic)
        retrieval_scores.append(retrieval)
        precision_scores.append(precision)
        exact_scores.append(exact)
        latency_scores.append(latency)

# --------------------------------------------------
# Summary
# --------------------------------------------------

print("\n")
print("=" * 70)
print("Evaluation Summary")
print("=" * 70)

print(f"Questions              : {len(dataset)}")
print(f"Average Semantic Score : {sum(semantic_scores)/len(dataset):.3f}")
print(f"Retrieval Hit Rate     : {sum(retrieval_scores)/len(dataset):.3f}")
print(f"Context Precision      : {sum(precision_scores)/len(dataset):.3f}")
print(f"Exact Match            : {sum(exact_scores)/len(dataset):.3f}")
print(f"Average Latency        : {sum(latency_scores)/len(dataset):.2f} sec")

print("\nResults saved to:")
print(OUTPUT_PATH)