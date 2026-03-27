from dokis.models import Chunk
from searcher import search
from parser import fetch_paragraphs


def retrieve(query: str, k: int = 5) -> list[Chunk]:
    """
    Search via Serper, fetch top results from allowed domains,
    extract text, and return as Dokis Chunks.
    """
    search_results = search(query, max_results=k)
    chunks: list[Chunk] = []
    for result in search_results:
        paragraphs = fetch_paragraphs(
            result["url"], fallback=result["snippet"]
        )
        for para in paragraphs[:3]:
            if len(para.split()) >= 8:
                chunks.append(Chunk(
                    content=para,
                    source_url=result["url"],
                ))
    return chunks[:k]
