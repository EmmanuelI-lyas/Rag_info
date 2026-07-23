"""
Loads the existing Chroma vector database.
"""

from langchain_chroma import Chroma

from src.config import (
    VECTOR_DB_DIR,
    COLLECTION_NAME
)

from src.embeddings import load_embedding_model


def load_vector_db():
    """
    Loads the persisted Chroma database.
    """

    embedding_model = load_embedding_model()

    vector_db = Chroma(
        persist_directory=str(VECTOR_DB_DIR),
        embedding_function=embedding_model,
        collection_name=COLLECTION_NAME
    )

    return vector_db