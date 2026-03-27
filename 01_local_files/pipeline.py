import ollama
import dokis
from dokis.models import Chunk
from retriever import retrieve


CONFIG = dokis.Config(
    allowed_domains=[],        # empty = all file:// sources pass through
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
        "You are a helpful assistant. Answer using ONLY the sources below. "
        "Do not use any outside knowledge.\n\n"
        f"Sources:\n{context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )


def run_query(query: str) -> dict:
    raw_chunks = retrieve(query, k=3)
    clean_chunks, blocked = MIDDLEWARE.enforcer.filter(raw_chunks)
    prompt = build_prompt(query, clean_chunks)
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}],
    )
    response_text = response["message"]["content"]
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
