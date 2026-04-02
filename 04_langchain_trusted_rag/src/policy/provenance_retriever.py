import dokis
from dokis.adapters.langchain import ProvenanceRetriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

def build_dokis_config() -> dokis.Config:
    return dokis.Config(
        allowed_domains=[
            "docs.acme.internal",
            "security.acme.internal",
            "eng.acme.internal",
        ],
        min_citation_rate = 0.80,
        claim_threshold = 0.35,
    )

def build_provenance_retriever(
    base_retriever: BaseRetriever,
) -> ProvenanceRetriever:
    return ProvenanceRetriever (
        base_retriever = base_retriever,
        config = build_dokis_config(),
        url_metadata_key = "source",
    )

def compute_blocked_documents(
    raw_docs: list[Document],
    clean_docs: list[Document],
) -> list[Document]:
    clean_source_ids = {doc.metadata["source_id"] for doc in clean_docs}
    return [
        doc 
        for doc in raw_docs
        if doc.metadata["source_id"] not in clean_source_ids
    ]

    