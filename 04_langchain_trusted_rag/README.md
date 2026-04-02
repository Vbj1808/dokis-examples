# 04_langchain_trusted_rag

A production-grade Dokis example showing how to combine **LangChain retrieval** with **Dokis provenance enforcement** and **post-generation auditing**.

This demo uses a small, fully local, reproducible corpus with both **trusted** and **blocked** sources. LangChain retrieves relevant candidates, Dokis filters blocked sources **before** prompt construction, the model answers using only the allowed context and Dokis audits the final answer **after** generation.

---

## What this example shows

This example demonstrates a full trusted RAG flow:

1. **LangChain retrieval** - Retrieve top-k candidate documents from a mixed corpus.
2. **Pre-generation provenance enforcement** - Use `dokis.adapters.langchain.ProvenanceRetriever` to remove sources whose domains are not allowlisted.
3. **Answer generation from approved context only** - Build the final prompt using only the Dokis-filtered documents.
4. **Post-generation provenance audit** - Run `dokis.audit(...)` on the final answer against the approved evidence set.

---

## Pipeline

```text
User Question
    ↓
LangChain Retriever
    ↓
Raw Retrieved Candidates
    ↓
Dokis ProvenanceRetriever
    ↓
Allowed Prompt Sources
    ↓
LLM Answer Generation
    ↓
Dokis Audit
    ↓
Compliance Result + Provenance Map
```

---

## Why this matters

A normal retriever can return documents that are relevant but **not approved** for use in the final prompt.

This example makes that distinction explicit:

- LangChain retrieves a **mixed trust set**
- Dokis **removes blocked sources** before generation
- The model answers from **approved evidence only**
- Dokis **audits the final answer** afterward

That gives you two important controls:

| Stage | Control |
|---|---|
| Before generation | Source allowlist enforcement |
| After generation | Provenance auditing |

---

## Project structure

```
04_langchain_trusted_rag/
├── README.md
├── requirements.txt
├── .env.example
├── run.py
└── src/
    ├── audit/
    │   └── audit.py
    ├── data/
    │   └── corpus.py
    ├── generation/
    │   ├── answer.py
    │   └── prompts.py
    ├── policy/
    │   └── provenance_retriever.py
    ├── retrieval/
    │   ├── documents.py
    │   ├── retrieve.py
    │   └── vectorstore.py
    ├── ui/
    │   └── report.py
    ├── config.py
    ├── main.py
    └── types.py
```

---

## Setup

From inside `04_langchain_trusted_rag`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Then set your OpenAI key in `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

---

## Run

```bash
python run.py
```

---

## What you should see

The output is organized into these sections:

| Section | Description |
|---|---|
| **Raw Retrieved Sources** | LangChain returns top candidate docs from the mixed corpus. |
| **Allowed Prompt Sources** | Dokis filters the raw results using an allowlist of approved domains. |
| **Blocked Before Prompt** | Retrieved sources that were relevant enough to surface, but not approved for prompt construction. |
| **Final Answer From Allowed Docs Only** | The model answers using only the Dokis-filtered context. |
| **Dokis Audit Result** | The final answer is audited against the approved evidence set. |
| **Dokis Provenance Map** | Supported claims are mapped back to source domains. |

---

## Why this uses synthetic data

This example uses a small synthetic corpus on purpose. That makes it:

- **Reproducible** - same results every run
- **Stable** - no external dependencies or rate limits
- **Easy to inspect** - small enough to read in full
- **Easy to debug** - failures are deterministic
- **Reliable for demos** - no internet flakiness

For a flagship example, deterministic behavior is more important than internet realism.

---

## Why this is production-grade

This is a **production-grade example**, not a full production deployment.

It earns that label because it has:

- ✅ Clear architecture boundaries
- ✅ Explicit configuration
- ✅ Current LangChain integration
- ✅ Reproducible local behavior
- ✅ Real Dokis pre-generation enforcement
- ✅ Real Dokis post-generation audit
- ✅ Readable terminal output

It does **not** include:

- ❌ Persistent storage
- ❌ Web UI
- ❌ Auth
- ❌ Telemetry
- ❌ CI/CD

---

## Summary

`04_langchain_trusted_rag` shows a compact, trustworthy RAG pipeline with:

1. **LangChain retrieval** over a mixed corpus
2. **Dokis source allowlist enforcement** before generation
3. **Answer generation** from approved evidence only
4. **Dokis provenance audit** after generation

> If you want one example in this repo that captures the core Dokis value proposition clearly, **this is it.**