import re

UNRELIABLE_DOMAINS = {
    "opindia", "postcard", "sudarshannews", "newspunch",
    "naturalnews", "infowars", "breitbart", "theonion"
}

TIER_5 = {"reuters", "bbc", "ap ", "apnews", "npr", "associated press"}
TIER_4 = {"guardian", "aljazeera", "bloomberg", "nytimes", "washingtonpost",
           "abc news", "nbc news", "cbs news", "hindu", "indian express",
           "hindustan times", "ndtv", "the wire", "scroll"}
TIER_3 = {"times of india", "economic times", "india today", "mint",
           "business standard", "deccan herald", "print", "news18",
           "politico", "forbes", "newsweek", "economist", "cnn"}
TIER_2 = {"yahoo", "msn", "zee news", "republic", "rolling stone",
           "deadline", "variety", "tribune"}


def get_source_score(source):
    if not source:
        return 1

    s = source.lower()

    # Unreliable — straight 0
    for bad in UNRELIABLE_DOMAINS:
        if bad in s:
            return 0

    # Known tiers
    for name in TIER_5:
        if name in s:
            return 5
    for name in TIER_4:
        if name in s:
            return 4
    for name in TIER_3:
        if name in s:
            return 3
    for name in TIER_2:
        if name in s:
            return 2

    # Unknown source — heuristic scoring
    score = 2

    if any(x in s for x in [".gov", ".edu", ".org"]):
        score += 1

    if any(x in s for x in ["blogspot", "wordpress", "medium",
                              "substack", "wix"]):
        score -= 1

    return max(1, min(score, 5))