from __future__ import annotations

from urllib.parse import urlparse

from langchain_core.documents import Document
from rich.box import SIMPLE_HEAVY
from rich.panel import Panel
from rich.table import Table


def extract_domain(url: str) -> str:
    if "://" not in url:
        return url
    return urlparse(url).netloc


def truncate(text: str, limit: int) -> str:
    text = text.replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def build_header_panel(
    *,
    model: str,
    embedding_model: str,
    corpus_size: int,
    question: str,
) -> Panel:
    return Panel.fit(
        "\n".join(
            [
                "[bold green]04_langchain_trusted_rag[/bold green]",
                "",
                f"OpenAI model: [cyan]{model}[/cyan]",
                f"Embedding model: [cyan]{embedding_model}[/cyan]",
                f"Corpus size: [cyan]{corpus_size}[/cyan]",
                "",
                f"[bold]Question[/bold]: {question}",
            ]
        ),
        title="Trusted RAG Demo",
        border_style="green",
    )


def build_pipeline_summary_panel(
    *,
    raw_count: int,
    allowed_count: int,
    blocked_count: int,
    answer_length: int,
    passed: bool,
    compliance_rate: float,
) -> Panel:
    passed_style = "green" if passed else "red"
    compliance_style = "green" if compliance_rate >= 0.80 else "yellow"

    return Panel.fit(
        "\n".join(
            [
                f"Raw retrieved docs: [cyan]{raw_count}[/cyan]",
                f"Allowed before prompt: [green]{allowed_count}[/green]",
                f"Blocked before prompt: [red]{blocked_count}[/red]",
                f"Answer length: [cyan]{answer_length} chars[/cyan]",
                f"Audit passed: [{passed_style}]{passed}[/{passed_style}]",
                f"Compliance rate: [{compliance_style}]{compliance_rate:.2f}[/{compliance_style}]",
            ]
        ),
        title="Pipeline Summary",
        border_style="yellow",
    )


def build_source_table(title: str, docs: list[Document]) -> Table:
    table = Table(title=title, box=SIMPLE_HEAVY)
    table.add_column("#", width=3, style="bold")
    table.add_column("Source ID", min_width=22, max_width=26, overflow="ellipsis")
    table.add_column("Trust", width=8)
    table.add_column("Type", min_width=16, max_width=20, overflow="ellipsis")
    table.add_column("Domain", min_width=22, max_width=28, overflow="ellipsis")
    table.add_column("Title", min_width=24, max_width=34, overflow="ellipsis")

    for idx, doc in enumerate(docs, start=1):
        trust_label = doc.metadata["trust_label"]
        trust_style = "green" if trust_label == "trusted" else "red"

        table.add_row(
            str(idx),
            str(doc.metadata["source_id"]),
            f"[{trust_style}]{trust_label}[/{trust_style}]",
            str(doc.metadata["source_type"]),
            extract_domain(str(doc.metadata["source"])),
            truncate(str(doc.metadata["title"]), 34),
        )

    if not docs:
        table.add_row("-", "-", "-", "-", "-", "No documents")

    return table


def build_answer_panel(answer: str) -> Panel:
    return Panel(
        answer,
        title="Final Answer From Allowed Docs Only",
        border_style="green",
    )


def build_audit_panel(result) -> Panel:
    passed_style = "green" if result.passed else "red"
    compliance_style = "green" if result.compliance_rate >= 0.80 else "yellow"

    return Panel.fit(
        "\n".join(
            [
                f"Passed: [{passed_style}]{result.passed}[/{passed_style}]",
                f"Compliance rate: [{compliance_style}]{result.compliance_rate:.2f}[/{compliance_style}]",
                f"Violation count: [red]{len(result.violations)}[/red]",
                f"Blocked sources reported: [red]{len(result.blocked_sources)}[/red]",
            ]
        ),
        title="Dokis Audit Result",
        border_style="blue",
    )


def build_provenance_table(result) -> Table:
    table = Table(title="Dokis Provenance Map", box=SIMPLE_HEAVY)
    table.add_column("#", width=3, style="bold")
    table.add_column("Claim", min_width=50, max_width=70, overflow="fold")
    table.add_column("Source Domain", min_width=24, max_width=30, overflow="ellipsis")

    provenance_items = list(result.provenance_map.items())

    if not provenance_items:
        table.add_row("-", "No mapped claims", "-")
        return table

    for idx, (claim_text, source_url) in enumerate(provenance_items, start=1):
        table.add_row(
            str(idx),
            truncate(str(claim_text), 220),
            extract_domain(str(source_url)),
        )

    return table


def build_violations_table(result) -> Table:
    table = Table(title="Unsupported Claims", box=SIMPLE_HEAVY)
    table.add_column("#", width=3, style="bold")
    table.add_column("Claim", min_width=42, max_width=60, overflow="fold")
    table.add_column("Confidence", width=10)
    table.add_column("Source Domain", min_width=20, max_width=28, overflow="ellipsis")

    if not result.violations:
        table.add_row("-", "No unsupported claims", "-", "-")
        return table

    for idx, claim in enumerate(result.violations, start=1):
        table.add_row(
            str(idx),
            truncate(str(claim.text), 180),
            f"{claim.confidence:.2f}",
            extract_domain(claim.source_url or "-"),
        )

    return table