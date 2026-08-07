import yake
import re

def extract_keywords(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text).strip()

    bigram_extractor = yake.KeywordExtractor(
        lan="en",
        n=2,
        dedupLim=0.7,
        top=20
    )

    unigram_extractor = yake.KeywordExtractor(
        lan="en",
        n=1,
        dedupLim=0.7,
        top=20
    )

    bigrams = bigram_extractor.extract_keywords(text[:3000])
    unigrams = unigram_extractor.extract_keywords(text[:3000])

    blacklist = {
        "said", "says", "according", "april", "august", "march",
        "june", "july", "today", "recent", "prime", "minister",
        "government", "stories", "views", "special", "strategic",
        "bringing", "possible", "possibility", "reported", "people",
        "country", "state", "would", "could", "should", "article",
        "news", "also", "first", "last", "year", "years", "time",
        "new", "one", "two", "three", "make", "made", "many"
    }

    clean_bigrams = []
    for phrase, score in bigrams:
        phrase = phrase.lower().strip()
        words = phrase.split()
        # Skip blacklisted or too-short words
        if any(w in blacklist or len(w) < 4 for w in words):
            continue
        # Skip proper noun combos (likely author/person names)
        if all(w[0].isupper() for w in phrase.split() if w):
            continue
        if phrase not in clean_bigrams:
            clean_bigrams.append(phrase)

    clean_unigrams = []
    for word, score in unigrams:
        word = word.lower().strip()
        if word in blacklist or len(word) < 5:
            continue
        already_in_bigram = any(word in bg for bg in clean_bigrams)
        if not already_in_bigram and word not in clean_unigrams:
            clean_unigrams.append(word)

    final_keywords = clean_bigrams[:2] + clean_unigrams[:2]
    final_keywords = final_keywords[:4]

    query = " ".join(final_keywords)

    print("EXTRACTED BIGRAMS:", clean_bigrams[:3])
    print("EXTRACTED UNIGRAMS:", clean_unigrams[:3])
    print("FINAL KEYWORD QUERY:", query)

    return query