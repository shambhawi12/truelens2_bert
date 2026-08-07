import requests
import os
import re
import feedparser
from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.source_checker import get_source_score
from src.keyword_extractor import extract_keywords


load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

# Semantic similarity model
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_query(query):
    if not query:
        return ""
    query = re.sub(r"\s+", " ", query)
    query = re.sub(r"[^\w\s]", "", query)
    return query.strip()


def filter_related_news(original_text, articles):
    if not articles:
        return []

    try:
        original_embedding = similarity_model.encode(original_text[:2000])
        related = []

        for article in articles:
            text = article.get("title", "") + " " + article.get("description", "")
            if not text.strip():
                continue

            article_embedding = similarity_model.encode(text)
            score = cosine_similarity([original_embedding], [article_embedding])[0][0]

            print("SIMILARITY:", article.get("title"), round(score, 3))

            if score >= 0.25:
                article["similarity_score"] = round(score * 100, 2)
                related.append(article)

        related.sort(key=lambda x: x["similarity_score"], reverse=True)
        return related[:5]

    except Exception as e:
        print("SIMILARITY ERROR:", e)
        return []


def fetch_articles(url, params, seen):
    """NewsAPI se articles fetch karo"""
    response = requests.get(url, params=params, timeout=10)
    print("STATUS CODE:", response.status_code)

    data = response.json()
    if data.get("status") != "ok":
        print("NEWS API ERROR:", data)
        return []

    print("TOTAL RESULTS:", data.get("totalResults", 0))

    articles = []
    for article in data.get("articles", []):
        article_url = article.get("url", "")
        if not article_url or article_url in seen:
            continue
        seen.add(article_url)

        source = article.get("source", {}).get("name", "Unknown")
        articles.append({
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "source": source,
            "source_score": get_source_score(source),
            "published_at": article.get("publishedAt", ""),
            "url": article_url
        })

    return articles


def search_google_news(query, seen, max_results=20):
    """Google News RSS se search karo - Indian news ke liye better"""
    try:
        encoded_query = requests.utils.quote(query)
        rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
        
        print("GOOGLE NEWS QUERY:", query)
        feed = feedparser.parse(rss_url)
        print("GOOGLE NEWS RESULTS:", len(feed.entries))

        articles = []
        for entry in feed.entries[:max_results]:
            article_url = entry.get("link", "")
            if not article_url or article_url in seen:
                continue
            seen.add(article_url)

            source_name = "Google News"
            if hasattr(entry, "source") and entry.source:
                source_name = entry.source.get("title", "Google News")
            print("SOURCE NAME:", source_name)
            articles.append({
                "title": entry.get("title", ""),
                "description": entry.get("summary", ""),
                "source": source_name,
                "source_score": get_source_score(source_name),
                "published_at": entry.get("published", ""),
                "url": article_url
            })

        return articles

    except Exception as e:
        print("GOOGLE NEWS ERROR:", e)
        return []


def search_related_news(article_text):
    original_text = article_text

    # Clean and extract keywords
    query = clean_query(article_text)
    search_query = extract_keywords(query)

    print("FINAL KEYWORD QUERY:", search_query)

    if not search_query:
        print("No keywords extracted")
        return []

    seen = set()
    articles = []

    # ── Step 1: NewsAPI ──
    if API_KEY:
        api_url = "https://newsapi.org/v2/everything"
        params = {
            "q": search_query,
            "language": "en",
            "sortBy": "relevancy",
            "pageSize": 30,
            "searchIn": "title,description",
            "apiKey": API_KEY
        }

        try:
            articles = fetch_articles(api_url, params, seen)
            print("NEWSAPI RESULTS:", len(articles))

            # Fallback: agar 0 results toh pehle word se retry
            if len(articles) == 0:
                fallback_words = search_query.split()
                fallback = next((w for w in fallback_words if len(w) > 4), "")
                if fallback:
                    print("RETRYING NEWSAPI WITH FALLBACK:", fallback)
                    params["q"] = fallback
                    articles = fetch_articles(api_url, params, seen)
                    print("NEWSAPI FALLBACK RESULTS:", len(articles))

        except Exception as e:
            print("NEWSAPI ERROR:", e)

    else:
        print("NEWS_API_KEY missing — skipping NewsAPI")

    # ── Step 2: Google News RSS (agar NewsAPI se kam results) ──
    if len(articles) < 5:
        print("FEW RESULTS — trying Google News RSS...")
        google_articles = search_google_news(search_query, seen)

        # Agar main query se bhi kam aaye toh unigram fallback
        if len(google_articles) == 0:
            fallback_words = search_query.split()
            fallback = next((w for w in fallback_words if len(w) > 4), "")
            if fallback:
                print("GOOGLE NEWS FALLBACK:", fallback)
                google_articles = search_google_news(fallback, seen)

        articles.extend(google_articles)
        print("TOTAL AFTER GOOGLE NEWS:", len(articles))

    # ── Step 3: Similarity filter ──
    print("BEFORE SIMILARITY FILTER:", len(articles))
    articles = filter_related_news(original_text, articles)
    print("AFTER SIMILARITY FILTER:", len(articles))

    return articles