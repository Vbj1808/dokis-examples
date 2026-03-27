from pipeline import run_query

QUERIES = [
    "How does aspirin reduce fever?",
    "What is the treatment for type 2 diabetes?",
    "How do vaccines create immunity?",
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
    print("Demo 01 — Local Files + BM25 + Ollama llama3.2 + Dokis")
    for q in QUERIES:
        print_result(run_query(q))
    print("\nDone.")
