"""
Interactive RAG Chat (LangGraph)
"""

from src.graph.workflow import build_graph


def print_sources(documents):

    print("\nSources Used")
    print("-" * 60)

    for i, doc in enumerate(documents, start=1):

        page = doc.metadata.get("page", "N/A")
        source = doc.metadata.get("source", "Unknown")
        content_type = doc.metadata.get("content_type", "text")

        print(
            f"{i}. "
            f"Page: {page} | "
            f"Type: {content_type} | "
            f"Source: {source}"
        )


def main():

    graph = build_graph()

    print("=" * 70)
    print("Financial RAG Assistant")
    print("Type 'exit' to quit.")
    print("=" * 70)

    while True:

        question = input("\nYou: ")

        if question.lower() in ["exit", "quit"]:

            print("\nGoodbye!")
            break

        result = graph.invoke({

            "question": question

        })

        if not result["success"]:

            print("\nFailed to generate response.")

            print(result["error"])

            continue

        print("\nAssistant:\n")

        print(result["answer"])

        print("\n")

        print("=" * 70)

        print(
            f"Provider : {result['provider']} | "
            f"Model : {result['model']}"
        )

        print_sources(result["reranked_documents"])

        print("=" * 70)


if __name__ == "__main__":

    main()