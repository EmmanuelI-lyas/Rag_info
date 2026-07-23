from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# Project Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

PDF_PATH = DATA_DIR / "bis_report_2026.pdf"

VISUAL_SUMMARY_PATH = DATA_DIR / "visual_summaries.md"


# ==========================
# Embedding Model
# ==========================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"


# ==========================
# Chunking
# ==========================

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 150


# ==========================
# Retrieval
# ==========================

RETRIEVAL_K = 15
FINAL_TOP_K = 5


# ==========================
# Chroma Collection
# ==========================

COLLECTION_NAME = "bis_rag"
# ==========================
# API Keys
# ==========================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# ==========================
# LLM Settings
# ==========================

PRIMARY_PROVIDER = "gemini"

FALLBACK_PROVIDERS = [
    "groq",
    "openrouter"
]

TEMPERATURE = 0.2

MAX_TOKENS = 1024
# ==========================
# Provider Routing
# ==========================

PRIMARY_PROVIDER = "gemini"

FALLBACK_PROVIDERS = [
    "groq",
    "openrouter"
]


# ==========================
# Provider Models
# ==========================

GEMINI_MODEL = "gemini-flash-latest"

GROQ_MODEL = "llama-3.3-70b-versatile"

OPENROUTER_MODEL = "meta-llama/llama-3.3-70b-instruct:free"


# ==========================
# Smart Routing
# ==========================

SMALL_PROMPT_THRESHOLD = 3000

MEDIUM_PROMPT_THRESHOLD = 7000

ENABLE_FALLBACK = True


# ==========================
# Logging
# ==========================

SHOW_PROVIDER_LOGS = True