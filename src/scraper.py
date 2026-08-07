import trafilatura


def scrape_article(url: str) -> str:
    """
    Extract article text from a news URL.
    """

    try:
        downloaded = trafilatura.fetch_url(url)

        if downloaded:
            text = trafilatura.extract(
                downloaded,
                include_comments=False,
                include_tables=False
            )

            if text:
                return text.strip()

        return ""

    except Exception as e:
        print("Scraping error:", e)
        return ""