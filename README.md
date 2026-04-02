<div align="center">

![Dokis banner](https://raw.githubusercontent.com/Vbj1808/dokis/main/assets/banner.svg)

<br/>

[![Dokis](https://img.shields.io/pypi/v/dokis?color=1D9E75&label=dokis&logo=pypi&logoColor=white)](https://pypi.org/project/dokis/)
[![Python](https://img.shields.io/pypi/pyversions/dokis?v=1&color=3b82f6&logo=python&logoColor=white)](https://pypi.org/project/dokis/)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e?logo=opensourceinitiative&logoColor=white)](LICENSE)

**Working RAG demos for [Dokis](https://github.com/Vbj1808/dokis) — runtime provenance enforcement for LLM pipelines.**

</div>

---

## Demos

| Demo | Retrieval | LLM | What it shows |
|---|---|---|---|
| [01 — Local files](01_local_files/) | BM25 over `.txt` files | Ollama llama3.2 | Simplest possible RAG + Dokis, zero infra |
| [02 — Chroma](02_chroma/) | Chroma + nomic-embed-text | Ollama llama3.2 | Semantic vector store integration |
| [03 — Live web search](03_web_search/) | Serper API + domain filtering | Ollama llama3.2 | Defense-in-depth domain enforcement, live data |
| [04 — LangChain trusted RAG](04_langchain_trusted_rag/) | LangChain + in-memory vector store | OpenAI | Pre-generation source allowlist enforcement with `ProvenanceRetriever` + post-generation provenance audit |

---

## Prerequisites

All demos require:

- Python 3.10–3.12

### Demos 01–03

These demos require:

- [Ollama](https://ollama.com) installed and running locally
- `llama3.2` model pulled:

```bash
ollama pull llama3.2
```

Demo 02 additionally requires:

```bash
ollama pull nomic-embed-text
```

Demo 03 additionally requires:

- Active internet connection
- A free Serper API key — sign up at [serper.dev](https://serper.dev)

### Demo 04

This demo requires:

- An OpenAI API key
- A `.env` file with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

---

## Quickstart

Each demo is self-contained. Pick one and run:

**Demo 01 — simplest, no setup beyond Ollama:**

```bash
cd 01_local_files
pip install -r requirements.txt
python run.py
```

**Demo 02 — semantic retrieval with Chroma:**

```bash
cd 02_chroma
pip install -r requirements.txt
python ingest.py   # run once to build the vector store
python run.py
```

**Demo 03 — live web search with domain enforcement:**

```bash
cd 03_web_search
echo "SERPER_API_KEY=your_key_here" > .env
pip install -r requirements.txt
python run.py
```

**Demo 04 — LangChain trusted RAG with Dokis audit:**

```bash
cd 04_langchain_trusted_rag
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

---

## What Dokis does in each demo

Every demo follows the same two-layer pattern:

**Layer 1 — Pre-generation enforcement.** Retrieved chunks whose `source_url` is not on the allowlist are stripped before they reach the LLM prompt.

**Layer 2 — Post-generation auditing.** Each claim in the LLM response is matched back to its source chunk via BM25. A compliance rate, provenance map, and violation list are returned.

Demo 03 adds a third layer — Serper results are filtered client-side by domain before any page is fetched, so Dokis acts as defense-in-depth rather than the only enforcement point.

Demo 04 shows the same trust model through a LangChain integration, using `dokis.adapters.langchain.ProvenanceRetriever` to filter sources before prompt construction and `dokis.audit(...)` to verify the final answer afterward.

---

## Main library

→ [github.com/Vbj1808/dokis](https://github.com/Vbj1808/dokis)

```bash
pip install dokis
```

---

## License

MIT