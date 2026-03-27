import bm25s
from dokis.models import Chunk
from ingest import ingest

ALL_CHUNKS = ingest()


def retrieve(query: str, k: int = 3) -> list[Chunk]:
    """Return the top-k chunks most relevant to query using BM25."""
    if not ALL_CHUNKS:
        raise RuntimeError("No chunks found. Add .txt files to docs/")
    corpus = [c.content for c in ALL_CHUNKS]
    corpus_tokens = bm25s.tokenize(corpus, stopwords="en")
    index = bm25s.BM25()
    index.index(corpus_tokens)
    query_tokens = bm25s.tokenize(query, stopwords="en")
    results, _ = index.retrieve(query_tokens, corpus=corpus,
                                k=min(k, len(corpus)))
    ranked_texts = list(results[0])
    text_to_chunk = {c.content: c for c in ALL_CHUNKS}
    return [text_to_chunk[t] for t in ranked_texts if t in text_to_chunk]
