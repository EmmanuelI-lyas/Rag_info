"""
Extract text from PDF, load visual summaries,
chunk everything, and return LangChain Documents.
"""

import re
import fitz

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    PDF_PATH,
    VISUAL_SUMMARY_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)


# ---------------------------------------------------
# Clean text
# ---------------------------------------------------

def clean_text(text: str) -> str:
    """
    Perform minimal cleaning while preserving meaning.
    """

    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# ---------------------------------------------------
# Extract PDF pages
# ---------------------------------------------------

def extract_pdf_documents():
    """
    Returns one LangChain Document per PDF page.
    """

    pdf = fitz.open(PDF_PATH)

    pages = []

    for page_num, page in enumerate(pdf):

        text = clean_text(page.get_text("text"))

        if not text.strip():
            continue

        pages.append(

            Document(

                page_content=text,

                metadata={

                    "page": page_num + 1,

                    "source": PDF_PATH.name,

                    "content_type": "text"

                }

            )

        )

    pdf.close()

    return pages


# ---------------------------------------------------
# Chunk text
# ---------------------------------------------------

def chunk_documents(documents):

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(

        chunk_size=CHUNK_SIZE,

        chunk_overlap=CHUNK_OVERLAP,

        separators=[

            "\n\n",

            "\n",

            ". ",

            " ",

            ""

        ]

    )

    chunks = splitter.split_documents(documents)

    return chunks


# ---------------------------------------------------
# Load visual summaries
# ---------------------------------------------------

def load_visual_documents():

    if not VISUAL_SUMMARY_PATH.exists():

        return []

    text = VISUAL_SUMMARY_PATH.read_text(
        encoding="utf-8"
    )

    sections = re.split(
        r"(?=## Visual)",
        text
    )

    visual_docs = []

    for section in sections:

        section = section.strip()

        if not section:

            continue

        visual_docs.append(

            Document(

                page_content=section,

                metadata={

                    "source": VISUAL_SUMMARY_PATH.name,

                    "content_type": "visual"

                }

            )

        )

    return visual_docs


# ---------------------------------------------------
# Build all documents
# ---------------------------------------------------

def load_documents():

    pdf_pages = extract_pdf_documents()

    text_chunks = chunk_documents(pdf_pages)

    visual_docs = load_visual_documents()

    all_documents = text_chunks + visual_docs

    return all_documents