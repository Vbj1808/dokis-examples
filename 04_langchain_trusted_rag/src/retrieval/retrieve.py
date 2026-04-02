from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever

from src.policy.provenance_retriever import build_provenance_retriever
from src.retrieval.documents import to_langchain_documents
from src.retrieval.vectorstore import build_vectorstore
from src.types import SourceDocument


def build_retriever(
    corpus: list[SourceDocument],
    k: int = 4,
) -> VectorStoreRetriever:
    docs = to_langchain_documents(corpus)
    vectorstore = build_vectorstore(docs)
    return vectorstore.as_retriever(search_kwargs = {"k": k})


def retrieve_documents(
    corpus: list[SourceDocument],
    question: str,
    k: int = 4,
) -> list[Document]:
    retriever = build_retriever(corpus = corpus, k = k)
    return retriever.invoke(question)

def retrieve_documents_with_dokis(
    corpus: list[SourceDocument],
    question: str,
    k: int = 4,
) -> tuple[list[Document], list[Document], list[Document]]:
    base_retriever = build_retriever(corpus = corpus, k = k)
    raw_docs = base_retriever.invoke(question)

    dokis_retriever = build_provenance_retriever(base_retriever)
    clean_docs = dokis_retriever.invoke(question)

    clean_source_ids = {doc.metadata["source_id"] for doc in clean_docs}
    blocked_docs = [
        doc for doc in raw_docs if doc.metadata["source_id"] not in clean_source_ids     
    ]

    return raw_docs, clean_docs, blocked_docs