import dokis 
from langchain_core.documents import Document

def build_audit_config() -> dokis.Config:
    return dokis.Config(
        allowed_domains=[
            "docs.acme.internal",
            "security.acme.internal",
            "eng.acme.internal",
        ],
        min_citation_rate = 0.80,
        claim_threshold = 0.35,
    )


def docs_to_dokis_chunks(docs: list[Document]) -> list[dokis.Chunk]:
    chunks: list[dokis.Chunk] = []

    for doc in docs:
        chunks.append(
            dokis.Chunk(
                content = doc.page_content,
                source_url = doc.metadata["source"],
                metadata = doc.metadata,
            )
        )
    
    return chunks


def audit_answer(
    query: str,
    docs: list[Document],
    response_text: str,
):
    config = build_audit_config()
    chunks = docs_to_dokis_chunks(docs)

    return dokis.audit(
        query,
        chunks,
        response_text,
        config = config,
    )

