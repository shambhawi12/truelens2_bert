from src.news_search import search_related_news


results = search_related_news(
    "Delhi Police security protest"
)


for article in results:

    print("\nTITLE:", article["title"])
    print("SOURCE:", article["source"])
    print("TRUST SCORE:", article["score"], "/5")
    print("URL:", article["url"])