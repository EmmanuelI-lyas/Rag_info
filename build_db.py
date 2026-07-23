from langchain_chroma import Chroma

from src.ingest import load_documents
from src.embeddings import load_embedding_model
from src.config import (
    VECTOR_DB_DIR,
    COLLECTION_NAME
)


def main():

    print("Loading documents...")
    documents = load_documents()

    print(f"Total documents: {len(documents)}")

    print("Loading embedding model...")
    embedding_model = load_embedding_model()

    print("Building Chroma database...")

    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=str(VECTOR_DB_DIR),
        collection_name=COLLECTION_NAME
    )

    print("Vector database created successfully.")
    print(f"Stored at: {VECTOR_DB_DIR}")


if __name__ == "__main__":
    main()