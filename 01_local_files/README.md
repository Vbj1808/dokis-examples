# Demo 01 — Local Files + BM25 + Ollama + Dokis

This demo builds a minimal retrieval-augmented generation (RAG) pipeline that reads plain `.txt` files from a local `docs/` folder, retrieves the most relevant sentence-level chunks using BM25 keyword search, sends them as grounded context to a locally running Ollama LLM (llama3.2), and enforces provenance on every response using Dokis.

## Prerequisites

- [Ollama](https://ollama.com) installed and running locally
- The llama3.2 model pulled: `ollama pull llama3.2`
- Python 3.10–3.12

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python run.py
```

The script runs three test queries and prints a report showing the retrieved chunks, the LLM response, and Dokis compliance information for each query.

## Adding your own documents

Drop any `.txt` files into the `docs/` folder. They will be automatically picked up and chunked at sentence level the next time you run the pipeline — no re-indexing step required.

## How Dokis fits in

`ProvenanceMiddleware.enforcer.filter()` screens retrieved chunks against the configured domain allowlist before they reach the LLM, ensuring only trusted sources are used as context. After the LLM responds, `MIDDLEWARE.audit()` checks each claim in the response against the source chunks and reports a compliance rate, provenance map, and any unsupported statements.
