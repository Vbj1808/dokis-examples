from langchain_core.documents import Document
from src.types import SourceDocument


def to_langchain_documents(items: list[SourceDocument]) -> list[Document]:
    docs: list[Document] = []

    for item in items:
        docs.append(
            Document(
                page_content = item.content,
                metadata = {
                    "source": item.source_url,
                    "source_id": item.source_id,
                    "title": item.title,
                    "source_type": item.source_type,
                    "trust_label": item.trust_label,
                },
            )
        )
    
    return docs