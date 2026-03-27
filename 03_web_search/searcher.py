import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_URL = "https://google.serper.dev/search"

ALLOWED_DOMAINS = [
    "pubmed.ncbi.nlm.nih.gov",
    "cancer.gov",
    "who.int",
    "cdc.gov",
    "medlineplus.gov",
]


def _domain(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc or parsed.path
    return host.lstrip("www.")


def search(query: str, max_results: int = 5) -> list[dict]:
    """
    Search via Serper and return results from allowed domains only.
    Each result: {"url": str, "title": str, "snippet": str}
    """
    if not SERPER_API_KEY:
        raise RuntimeError(
            "SERPER_API_KEY not found. Add it to .env as SERPER_API_KEY=your_key"
        )

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"q": query, "num": max_results * 3}

    resp = requests.post(SERPER_URL, headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    results = []
    for item in data.get("organic", []):
        url = item.get("link", "")
        if any(_domain(url).endswith(d) for d in ALLOWED_DOMAINS):
            results.append({
                "url": url,
                "title": item.get("title", ""),
                "snippet": item.get("snippet", ""),
            })
        if len(results) >= max_results:
            break

    return results
