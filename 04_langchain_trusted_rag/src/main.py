from src.audit.audit import audit_answer
from src.config import load_settings
from src.data.corpus import load_corpus
from src.generation.answer import generate_answer
from src.retrieval.retrieve import retrieve_documents_with_dokis
from src.ui.report import (
    build_answer_panel,
    build_audit_panel,
    build_header_panel,
    build_pipeline_summary_panel,
    build_provenance_table,
    build_source_table,
    build_violations_table,
)
from rich.console import Console


DEMO_QUESTION = (
    "How should a safe RAG system handle retrieved untrusted sources before answer generation?"
)


def main() -> None:
    console = Console()
    settings = load_settings()
    corpus = load_corpus()

    raw_docs, clean_docs, blocked_docs = retrieve_documents_with_dokis(
        corpus=corpus,
        question=DEMO_QUESTION,
        k=4,
    )

    answer = generate_answer(DEMO_QUESTION, clean_docs)
    audit_result = audit_answer(DEMO_QUESTION, clean_docs, answer)

    console.print(
        build_header_panel(
            model=settings.openai_model,
            embedding_model=settings.openai_embedding_model,
            corpus_size=len(corpus),
            question=DEMO_QUESTION,
        )
    )
    console.print()

    console.print(
        build_pipeline_summary_panel(
            raw_count=len(raw_docs),
            allowed_count=len(clean_docs),
            blocked_count=len(blocked_docs),
            answer_length=len(answer),
            passed=audit_result.passed,
            compliance_rate=audit_result.compliance_rate,
        )
    )
    console.print()

    console.print(build_source_table("Raw Retrieved Sources", raw_docs))
    console.print()
    console.print(build_source_table("Allowed Prompt Sources", clean_docs))
    console.print()
    console.print(build_source_table("Blocked Before Prompt", blocked_docs))
    console.print()

    console.print(build_answer_panel(answer))
    console.print()
    console.print(build_audit_panel(audit_result))
    console.print()
    console.print(build_provenance_table(audit_result))
    console.print()
    console.print(build_violations_table(audit_result))


if __name__ == "__main__":
    main()