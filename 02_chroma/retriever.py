import chromadb
import ollama
from pathlib import Path
from dokis.models import Chunk

CHROMA_PATH = str(Path(__file__).parent / ".chroma_db")
COLLECTION_NAME = "dokis_demo"


def retrieve(query: str, k: int = 3) -> list[Chunk]:
    """Return top-k semantically similar chunks from Chroma."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection(COLLECTION_NAME)
    query_embedding = ollama.embeddings(
        model="nomic-embed-text", prompt=query
    )["embedding"]
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas"],
    )
    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        chunks.append(Chunk(
            content=doc,
            source_url=meta.get("source_url", ""),
        ))
    return chunks
