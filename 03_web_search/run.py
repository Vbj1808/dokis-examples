from pipeline import run_query

QUERIES = [
    "What are the side effects of aspirin?",
    "How is type 2 diabetes treated?",
    "How do mRNA vaccines work?",
]

SEP = "─" * 60


def print_result(r: dict) -> None:
    print(f"\n{SEP}")
    print(f"QUERY      : {r['query']}")
    print(f"CHUNKS     : {r['retrieved']} retrieved → {r['clean']} after filter")
    if r["blocked"]:
        print(f"BLOCKED    : {r['blocked']}")
    print(f"RESPONSE   :\n{r['response']}")
    print(f"\nDOKIS")
    print(f"  compliance : {r['compliance_rate']:.0%}  passed={r['passed']}")
    for claim, url in r["provenance_map"].items():
        print(f"  ✓ {claim[:70]}...")
        print(f"    → {url}")
    for v in r["violations"]:
        print(f"  ✗ {v[:70]}...")
    print(SEP)


if __name__ == "__main__":
    print("Demo 03 — Live Web Search + Allowed Domains + llama3.2 + Dokis")
    print("Search provider: Serper API")
    for q in QUERIES:
        print_result(run_query(q))
    print("\nDone.")
