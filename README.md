# Financial RAG Assistant

This repository contains a full retrieval-augmented generation (RAG) system for financial documents.

It ingests source content, builds a vector index, retrieves relevant context, and generates grounded answers using a LangGraph workflow and multiple LLM providers.

## Project overview

The project was built to answer questions about financial documents using a retrieval-first approach. Instead of relying only on the language model's memory, the system searches a local knowledge base built from source documents and uses those retrieved passages to improve factual grounding.

## Core capabilities

- Ingests PDF content and visual-summary markdown from the data folder
- Cleans and chunks documents for better retrieval quality
- Converts text into embeddings and stores them in a Chroma vector database
- Uses a LangGraph pipeline with dedicated nodes for rewriting, retrieval, reranking, prompting, and generation
- Supports multiple LLM backends such as Gemini, Groq, and OpenRouter
- Offers both a web interface via Streamlit and a terminal chat experience
- Includes an evaluation pipeline for measuring retrieval and answer quality

## Architecture summary

The application follows a classic RAG architecture:

1. Data ingestion

   - Source PDFs and markdown summaries are loaded from the data folder.
   - Text is extracted, cleaned, and split into smaller chunks.

2. Indexing and storage

   - Embedding models convert document chunks into vectors.
   - These vectors are stored in Chroma, enabling semantic similarity search.

3. Query processing

   - A user question is rewritten to improve retrieval quality.
   - Relevant chunks are retrieved from the vector database.
   - Retrieved documents are reranked and used to build a prompt.
   - A generator model produces the final answer.

4. Interfaces

   - The Streamlit app provides a polished chat UI.
   - The terminal script offers a simpler CLI workflow.
   - Evaluation scripts test the system against a question-answer dataset.

## Repository structure

- app.py: Streamlit application entry point
- build_db.py: Builds the Chroma vector database
- chat.py: Terminal-based chat interface
- src/: Main application package containing ingestion, embeddings, retrieval, prompts, workflow logic, and UI modules
- data/: Documents and supporting files used by the system
- evaluation/: Dataset, metrics, and evaluation scripts
- vector_db/: Generated local vector database files
- architecture.svg: Visual architecture diagram for presentations and documentation

## Setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the project root with your API keys:

   ```env
   GEMINI_API_KEY=your_gemini_key
   GROQ_API_KEY=your_groq_key
   OPENROUTER_API_KEY=your_openrouter_key
   ```

4. Ensure the required source files exist in the data folder, especially:
   - data/bis_report_2026.pdf
   - data/visual_summaries.md

   If your files use different names or locations, update the paths in src/config.py.

5. Build the vector database:

   ```bash
   python build_db.py
   ```

## Run the project

### Streamlit UI

```bash
streamlit run app.py
```

### Terminal chat

```bash
python chat.py
```

## Evaluation

Run the evaluation suite with:

```bash
python evaluation/evaluate.py
```

This generates evaluation metrics and saves them to evaluation/results.csv.

## Architecture diagram

A detailed SVG diagram is available at [architecture.svg](architecture.svg). It shows the flow from document ingestion to vector storage, query processing, and generation.

## Notes

- The vector database and generated artifacts are intended to be local runtime outputs and are ignored by Git.
- Provider and model settings can be adjusted in src/config.py.
- This architecture can be adapted for other document domains beyond finance.
