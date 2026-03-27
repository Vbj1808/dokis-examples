# Demo 03 — Live Web Search RAG with Dokis Domain Enforcement

This demo implements a retrieval-augmented generation (RAG) pipeline that fetches live web content at query time — no pre-ingestion step — restricted to a curated set of trusted medical domains. It mirrors the domain-restricted retrieval architecture described in the [HopeLink paper](https://arxiv.org/abs/2409.02588), where health information is sourced exclusively from authoritative sources to prevent misinformation. Dokis provides both a second layer of domain enforcement and full provenance auditing of the generated response.

## What it does

1. Accepts a natural-language medical query.
2. Searches the web via the **Serper API** and filters results to allowed medical domains.
3. Fetches and parses clean paragraph text from the top-matching pages.
4. Passes the text as context chunks to **Ollama (llama3.2)** for answer generation.
5. **Dokis** re-enforces domain restrictions on the chunks (defense-in-depth) and audits every claim in the response against the retrieved sources, reporting compliance rate and provenance.

## Prerequisites

- **Ollama** running locally: `ollama serve`
- **llama3.2** model pulled: `ollama pull llama3.2`
- Active internet connection (live search at query time)
- A free **Serper API key** — sign up at https://serper.dev
- Python 3.10–3.12

## Setup

1. Add your Serper API key to `.env`:
   ```
   SERPER_API_KEY=your_key_here
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python run.py
```

No ingest step is needed — retrieval happens live at query time for every question.

## Allowed Domains

Results are restricted to these authoritative medical sources:

| Domain | Source |
|---|---|
| `pubmed.ncbi.nlm.nih.gov` | PubMed / NCBI |
| `cancer.gov` | National Cancer Institute |
| `who.int` | World Health Organization |
| `cdc.gov` | Centers for Disease Control |
| `medlineplus.gov` | MedlinePlus (NLM) |

To add more domains, update `ALLOWED_DOMAINS` in both `searcher.py` and `pipeline.py`.

## Dokis: Two Layers of Domain Enforcement

Domain enforcement is applied twice:

1. **searcher.py** — filters Serper results client-side before fetching any page, keeping network requests minimal.
2. **Dokis `ProvenanceMiddleware`** — re-checks every chunk's `source_url` before it enters the LLM prompt. Even if a result somehow slips through the first filter (e.g., a redirect to an off-domain URL), Dokis blocks it here.

After generation, Dokis audits the response for unsupported claims, computes a citation compliance rate, and returns a full provenance map linking each verified claim back to its source URL.

