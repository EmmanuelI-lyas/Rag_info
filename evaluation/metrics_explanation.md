# Evaluation Metrics Explanation

This evaluation measures how well the RAG system answers each question in `evaluation/dataset.json` and how well it retrieves supporting context.

## How the evaluation works

For every sample in the dataset, `evaluation/evaluate.py` does the same sequence:

1. Load the question and the reference answer (`ground_truth`).
2. Run the LangGraph pipeline with `graph.invoke({"question": question})`.
3. Collect the generated answer and the reranked retrieved chunks.
4. Measure answer quality, retrieval quality, and runtime.
5. Write one row to `evaluation/results.csv`.

After all questions are processed, the script prints average scores across the full dataset.

## Metrics in `results.csv`

### `SemanticSimilarity`

This compares the generated answer to the ground truth using cosine similarity between sentence embeddings.

- Model used: `sentence-transformers/all-MiniLM-L6-v2`
- Higher is better
- Range is roughly from 0 to 1 in practice

Interpretation: a high score means the answer is semantically close to the reference, even if the wording is not identical.

### `RetrievalHit`

This is a binary retrieval score.

- `1` means at least one retrieved chunk is semantically similar enough to the ground truth
- `0` means none of the retrieved chunks passed the similarity threshold
- The threshold in the code is `0.60`

Interpretation: this tells you whether the retriever found at least one useful piece of evidence.

### `ContextPrecision`

This measures the average semantic similarity between the ground truth and all retrieved chunks.

- Higher is better
- It reflects how relevant the retrieved context set is overall
- If many retrieved chunks are off-topic, the score drops

Interpretation: this is a broader retrieval quality signal than `RetrievalHit`, because it considers every retrieved chunk instead of only the best one.

### `ExactMatch`

This checks whether the generated answer exactly matches the ground truth after trimming whitespace and lowercasing.

- `1` means the strings match exactly
- `0` means they do not

Interpretation: this is a very strict metric. It is useful for checking whether the model reproduces the reference verbatim, but it will usually score `0` when the answer is a correct paraphrase.

### `LatencySeconds`

This is the wall-clock time for one full `graph.invoke(...)` call.

- Lower is better
- It includes the time needed to retrieve, rerank, and generate the answer

Interpretation: this measures response speed, not answer quality.

## What the summary means

`evaluation/report.py` reads `evaluation/results.csv` and prints dataset-level averages:

- Average `SemanticSimilarity`
- Retrieval hit rate from `RetrievalHit`
- Average `ContextPrecision`
- Average `ExactMatch`
- Average `LatencySeconds`

It also shows:

- The questions with the lowest semantic similarity
- The slowest questions by latency

## How to read the scores

The metrics answer different questions:

- `SemanticSimilarity` asks: did the model say something close to the reference?
- `RetrievalHit` asks: did retrieval surface at least one relevant chunk?
- `ContextPrecision` asks: how relevant was the retrieved context overall?
- `ExactMatch` asks: did the model reproduce the reference exactly?
- `LatencySeconds` asks: how long did the full pipeline take?

Taken together, they show whether failures come from retrieval, generation, or speed.

## Important caveats

- The semantic metrics depend on the embedding model, so the scores are approximate rather than human judgment.
- `RetrievalHit` uses a fixed similarity threshold of `0.60`, which is a practical heuristic, not a universal standard.
- `ContextPrecision` is not the same as classical information-retrieval precision; it is an embedding-based relevance average.
- `ExactMatch` is intentionally strict and will miss correct paraphrases.

## Related files

- `evaluation/evaluate.py` runs the full evaluation loop.
- `evaluation/metrics.py` defines the scoring functions.
- `evaluation/report.py` summarizes the CSV output.
- `evaluation/results.csv` stores the per-question results.