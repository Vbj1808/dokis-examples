import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; DokisDemo/1.0)"}
TIMEOUT = 8


def fetch_paragraphs(url: str, fallback: str = "") -> list[str]:
    """
    Fetch url and return a list of clean paragraph strings.
    Falls back to [fallback] if the page cannot be fetched.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        paragraphs = []
        for p in soup.find_all("p"):
            text = p.get_text(separator=" ", strip=True)
            if len(text) > 40:
                paragraphs.append(text)
        return paragraphs[:20] if paragraphs else ([fallback] if fallback else [])
    except Exception:
        return [fallback] if fallback else []
