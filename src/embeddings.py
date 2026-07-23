"""
Loads the embedding model used across the project.
"""
import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings

from src.config import EMBEDDING_MODEL
load_dotenv()
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN", "")


def load_embedding_model():
    """
    Returns the HuggingFace embedding model.
    """

    embedding_model = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={
            "device": "cpu"      # Change to "cuda" if using GPU
        },
        encode_kwargs={
            "normalize_embeddings": True
        }
    )

    return embedding_model