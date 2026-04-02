from langchain_core.documents import Document

SYSTEM_PROMPT = """You are a careful assistant answering questions about trusted retrieval systems.

Rules:
- Use only the provided context.
- Do not rely on outside knowledge.
- If the context is insufficient, say so.
- Keep the answer concise but specific.
- Do not mention blocked or filtered documents unless the context supports that explanation.
"""

def build_context(docs: list[Document]) -> str:
    sections: list[str] = []

    for idx, doc in enumerate(docs, start=1):
        sections.append(
            "\n".join(
                [
                    f"[Source {idx}]",
                    f"Source ID: {doc.metadata['source_id']}",
                    f"Title: {doc.metadata['title']}",
                    f"Domain: {doc.metadata['source'].split('/')[2] if '://' in doc.metadata['source'] else doc.metadata['source']}",
                    f"Content: {doc.page_content}",
                ]
            )
        )

    return "\n\n".join(sections)


def build_answer_prompt(question: str, docs: list[Document]) -> str:
    context = build_context(docs)
    return "\n\n".join(
        [
            "Answer the question using only the context below.",
            "",
            context,
            "",
            f"Question: {question}",
            "",
            "Return a short answer of 3-5 sentences. Explain the pre-generation filtering step clearly, and mention post-generation evidence traceability only if supported by the context.",
        ]
    )