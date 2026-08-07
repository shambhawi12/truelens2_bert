import re
import string
import nltk
from nltk.corpus import stopwords

# Download stopwords (only first time)
nltk.download("stopwords")

# Load English stopwords
stop_words = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    """
    Clean and preprocess news article text.
    """
    text = str(text).lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = " ".join(
        word for word in text.split()
        if word not in stop_words
    )

    return text