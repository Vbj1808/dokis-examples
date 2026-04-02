from src.types import SourceDocument


CORPUS: list[SourceDocument] = [
    SourceDocument(
        source_id="trusted_product_spec",
        title="Official Product Spec: Trusted Retrieval Controls",
        source_url="https://docs.acme.internal/product/trusted-retrieval",
        source_type="official_docs",
        trust_label="trusted",
        content=(
            "Trusted retrieval controls ensure that only approved source collections "
            "are eligible to enter the final generation context. "
            "Applications should enforce source allowlists before constructing prompts "
            "for policy-sensitive or compliance-sensitive tasks."
        ),
    ),
    SourceDocument(
        source_id="trusted_security_policy",
        title="Security Policy Handbook: Evidence Requirements",
        source_url="https://security.acme.internal/handbook/evidence-requirements",
        source_type="security_policy",
        trust_label="trusted",
        content=(
            "Generated answers for internal assistants must be traceable to approved evidence. "
            "Unapproved external content, leaked notes, and community speculation must not be "
            "used as authoritative support for final answers."
        ),
    ),
    SourceDocument(
        source_id="trusted_release_notes",
        title="Approved Release Notes: Source Allowlisting",
        source_url="https://docs.acme.internal/releases/source-allowlisting",
        source_type="release_notes",
        trust_label="trusted",
        content=(
            "The latest release added source allowlisting before answer generation "
            "and provenance auditing after generation. "
            "This enables applications to block untrusted retrieved chunks before they "
            "reach the language model prompt."
        ),
    ),
    SourceDocument(
        source_id="trusted_architecture_note",
        title="Architecture Note: Safe RAG Pipeline",
        source_url="https://eng.acme.internal/architecture/safe-rag-pipeline",
        source_type="architecture_note",
        trust_label="trusted",
        content=(
            "A safe retrieval-augmented generation pipeline should separate retrieval, "
            "policy enforcement, answer generation, and answer auditing into distinct stages. "
            "This separation improves explainability and operational safety."
        ),
    ),
    SourceDocument(
        source_id="blocked_forum_post",
        title="Community Forum Thread: Just Use Top-K Results",
        source_url="https://community.acme.example/t/use-top-k-results",
        source_type="forum_post",
        trust_label="blocked",
        content=(
            "One forum user argues that all highly ranked retrieved chunks should be passed "
            "directly into the model prompt, regardless of source approval status. "
            "The post claims trust filtering is unnecessary if retrieval scores are high."
        ),
    ),
    SourceDocument(
        source_id="blocked_blog_post",
        title="Unofficial Blog: Prompting Is Enough",
        source_url="https://random-ai-blog.example/prompting-is-enough",
        source_type="blog_post",
        trust_label="blocked",
        content=(
            "This unofficial blog recommends skipping source filtering entirely and relying "
            "on the model instruction to ignore bad evidence. "
            "It describes allowlisting as unnecessary overhead for most RAG systems."
        ),
    ),
    SourceDocument(
        source_id="blocked_leaked_notes",
        title="Leaked Notes: Future Trust Roadmap",
        source_url="https://paste.example/leaked-trust-roadmap",
        source_type="leaked_notes",
        trust_label="blocked",
        content=(
            "These leaked notes contain unverified claims about future trust behavior, "
            "including speculation that unofficial sources may be treated as acceptable context "
            "in some deployments. The material is not approved evidence."
        ),
    ),
]


def load_corpus() -> list[SourceDocument]:
    return CORPUS