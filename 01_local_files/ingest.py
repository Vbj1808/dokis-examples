from pathlib import Path
from dokis.models import Chunk


DOCS_DIR = Path(__file__).parent / "docs"


def ingest(docs_dir: Path = DOCS_DIR) -> list[Chunk]:
    """Load all .txt files in docs_dir and return as Dokis Chunks."""
    chunks: list[Chunk] = []
    for path in sorted(docs_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8").strip()
        source_url = "file://" + str(path.resolve())
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        for para in paragraphs:
            sentences = [s.strip() + "." for s in para.split(". ") if len(s.strip()) > 20]
            for sentence in sentences:
                chunks.append(Chunk(content=sentence, source_url=source_url))
    return chunks
