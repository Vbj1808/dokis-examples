# Demo 02 — Chroma + Ollama Embeddings + llama3.2 + Dokis

This demo builds a semantic RAG pipeline that ingests plain `.txt` files into a persistent Chroma vector store using Ollama's `nomic-embed-text` embedding model, retrieves the most relevant chunks at query time via cosine similarity search (rather than BM25 keyword matching as in Demo 01), passes the grounded context to a locally running Ollama LLM (llama3.2), and enforces provenance on every response using Dokis.

## Prerequisites

- [Ollama](https://ollama.com) installed and running locally
- llama3.2 pulled: `ollama pull llama3.2`
- nomic-embed-text pulled: `ollama pull nomic-embed-text`
- Python 3.10–3.12

## Setup

```bash
pip install -r requirements.txt
```

## Ingest

Must be run once before querying (re-run any time you add or change documents):

```bash
python ingest.py
```

This embeds all `.txt` files in `docs/` and stores them in a local `.chroma_db/` directory.

## Usage

```bash
python run.py
```

Runs three test queries and prints a report showing retrieved chunks, the LLM response, and Dokis compliance information for each query.

## Adding your own documents

Drop any `.txt` files into the `docs/` folder, then re-run `python ingest.py` to rebuild the vector store with the new content.

## How Dokis fits in

`ProvenanceMiddleware.enforcer.filter()` screens retrieved chunks against the configured domain allowlist before they reach the LLM, ensuring only trusted sources are used as context. After the LLM responds, `MIDDLEWARE.audit()` checks each claim in the response against the source chunks and reports a compliance rate, provenance map, and any unsupported statements.
