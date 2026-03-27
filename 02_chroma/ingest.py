from pathlib import Path
import chromadb
import ollama
from dokis.models import Chunk

DOCS_DIR = Path(__file__).parent / "docs"
CHROMA_PATH = str(Path(__file__).parent / ".chroma_db")
COLLECTION_NAME = "dokis_demo"


def embed(text: str) -> list[float]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]


def load_chunks(docs_dir: Path) -> list[Chunk]:
    chunks = []
    for path in sorted(docs_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        source_url = "file://" + str(path.resolve())
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            sentences = [s.strip() + "." for s in para.split(". ")
                         if len(s.strip()) > 20]
            for s in sentences:
                chunks.append(Chunk(content=s, source_url=source_url))
    return chunks


def ingest(docs_dir: Path = DOCS_DIR) -> None:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    # Delete existing collection for idempotency
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = client.create_collection(COLLECTION_NAME)
    chunks = load_chunks(docs_dir)
    for i, chunk in enumerate(chunks):
        embedding = embed(chunk.content)
        collection.add(
            ids=[f"doc_{i}"],
            embeddings=[embedding],
            documents=[chunk.content],
            metadatas=[{"source_url": chunk.source_url}],
        )
    print(f"Ingested {len(chunks)} chunks from {docs_dir}")


if __name__ == "__main__":
    ingest()
