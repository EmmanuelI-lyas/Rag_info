"""
Creates an evaluation report from results.csv
"""

import pandas as pd

RESULTS_PATH = "evaluation/results.csv"


def main():

    df = pd.read_csv(RESULTS_PATH)

    print("=" * 70)
    print("Financial RAG Evaluation Report")
    print("=" * 70)

    print()

    print(f"Questions Evaluated : {len(df)}")

    print()

    print(f"Average Semantic Similarity : {df['SemanticSimilarity'].mean():.3f}")

    print(f"Retrieval Hit Rate          : {df['RetrievalHit'].mean():.3f}")

    print(f"Context Precision           : {df['ContextPrecision'].mean():.3f}")

    print(f"Exact Match                 : {df['ExactMatch'].mean():.3f}")

    print(f"Average Latency             : {df['LatencySeconds'].mean():.2f} sec")

    print()

    print("=" * 70)

    print("Top 5 Lowest Semantic Scores")

    print("=" * 70)

    print(

        df.sort_values(

            by="SemanticSimilarity"

        )[

            [

                "ID",

                "Question",

                "SemanticSimilarity"

            ]

        ].head()

    )

    print()

    print("=" * 70)

    print("Slowest Questions")

    print("=" * 70)

    print(

        df.sort_values(

            by="LatencySeconds",

            ascending=False

        )[

            [

                "ID",

                "Question",

                "LatencySeconds"

            ]

        ].head()

    )


if __name__ == "__main__":

    main()