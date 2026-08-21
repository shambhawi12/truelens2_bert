import trafilatura
import requests


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def scrape_article(url: str) -> str:
    """
    Extract article text from a news URL.
    """
    try:
        # Attempt 1: requests with browser headers → trafilatura extract
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()

        text = trafilatura.extract(
            response.text,
            include_comments=False,
            include_tables=False,
            favor_recall=True,
        )

        if text:
            return text.strip()

        # Attempt 2: trafilatura's own fetcher as fallback
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False,
                favor_recall=True,
            )
            if text:
                return text.strip()

        return ""

    except Exception as e:
        print(f"Scraping error for {url}: {e}")
        return ""