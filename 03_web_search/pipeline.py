import ollama
import dokis
from dokis.models import Chunk
from retriever import retrieve


CONFIG = dokis.Config(
    allowed_domains=[
        "pubmed.ncbi.nlm.nih.gov",
        "cancer.gov",
        "who.int",
        "cdc.gov",
        "medlineplus.gov",
    ],
    min_citation_rate=0.5,
    claim_threshold=0.3,
    matcher="bm25",
    fail_on_violation=False,
)

MIDDLEWARE = dokis.ProvenanceMiddleware(CONFIG)


def build_prompt(query: str, chunks: list[Chunk]) -> str:
    context = "\n\n".join(
        f"[Source: {c.source_url}]\n{c.content}" for c in chunks
    )
    return (
        "You are a medical information assistant. "
        "Answer using ONLY the sources below. "
        "Do not use any outside knowledge.\n\n"
        f"Sources:\n{context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )


def run_query(query: str) -> dict:
    # 1. Retrieve live web content via Serper
    raw_chunks = retrieve(query, k=5)

    # 2. Dokis domain filter — second line of defense after searcher.py
    clean_chunks, blocked = MIDDLEWARE.enforcer.filter(raw_chunks)

    if not clean_chunks:
        return {
            "query": query,
            "retrieved": len(raw_chunks),
            "clean": 0,
            "blocked": blocked,
            "response": "No content from allowed domains found.",
            "compliance_rate": 0.0,
            "passed": False,
            "violations": [],
            "provenance_map": {},
        }

    # 3. Call Ollama
    prompt = build_prompt(query, clean_chunks)
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = response["message"]["content"]

    # 4. Audit with Dokis
    result = MIDDLEWARE.audit(query, clean_chunks, response_text)

    return {
        "query": query,
        "retrieved": len(raw_chunks),
        "clean": len(clean_chunks),
        "blocked": blocked,
        "response": response_text,
        "compliance_rate": result.compliance_rate,
        "passed": result.passed,
        "violations": [c.text for c in result.violations],
        "provenance_map": result.provenance_map,
    }
