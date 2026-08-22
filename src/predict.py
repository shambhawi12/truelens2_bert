import torch
import numpy as np
import requests
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from src.news_search import search_related_news
from dotenv import load_dotenv

load_dotenv()

# Model path
MODEL_PATH = "models/distilbert_best"
GOOGLE_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

# Load once at startup
from functools import lru_cache


@lru_cache(maxsize=1)
def load_model():
    """Load the DistilBERT model only when it is actually needed."""
    print("Loading DistilBERT model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    print(f"Model loaded on {device} ✅")

    return tokenizer, model, device

# ─────────────────────────────────────────────
# Fact Check API
# ─────────────────────────────────────────────
def check_facts(text: str) -> dict:
    """Google Fact Check Tools API se verify karo"""
    if not GOOGLE_API_KEY:
        return {"found": False}

    try:
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": text[:200],
            "key": GOOGLE_API_KEY,
            "languageCode": "en"
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if "claims" in data and data["claims"]:
            claim = data["claims"][0]
            review = claim["claimReview"][0]
            rating = review.get("textualRating", "").lower()

            return {
                "found": True,
                "text": claim.get("text", ""),
                "rating": review.get("textualRating", "Unknown"),
                "rating_lower": rating,
                "source": review["publisher"].get("name", "Unknown"),
                "url": review.get("url", "")
            }

    except Exception as e:
        print(f"Fact check error: {e}")

    return {"found": False}


# ─────────────────────────────────────────────
# News Verify
# ─────────────────────────────────────────────
def verify_with_news(text: str) -> dict:
    """NewsAPI se trusted sources mein verify karo"""
    try:
        trusted_sources = [
            "reuters", "bbc", "ap news", "associated press",
            "ndtv", "the hindu", "times of india", "india today",
            "bloomberg", "al jazeera", "AFP"
        ]

        related = search_related_news(text)

        trusted_count = sum(
            1 for article in related
            if any(src in article["source"].lower() for src in trusted_sources)
        )

        return {
            "verified": trusted_count > 0,
            "trusted_count": trusted_count,
            "articles": related[:3]
        }

    except Exception as e:
        print(f"News verify error: {e}")
        return {"verified": False, "trusted_count": 0, "articles": []}


# ─────────────────────────────────────────────
# Main Predict Function
# ─────────────────────────────────────────────
def predict_news(text: str) -> dict:
    """
    Predict whether a news article is Fake or Real.
    Uses DistilBERT (94% accuracy) + Google Fact Check + NewsAPI verification.
    """

    # ── Step 1: BERT Prediction ──
    tokenizer, model, device = load_model()

    inputs = tokenizer(
        str(text),
        truncation=True,
        padding="max_length",
        max_length=128,
        return_tensors="pt"
    )

    input_ids      = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        logits  = outputs.logits

    probs = torch.softmax(logits, dim=1).cpu().numpy()[0]

    fake_probability = round(float(probs[0]) * 100, 2)
    real_probability = round(float(probs[1]) * 100, 2)
    confidence       = round(float(np.max(probs)) * 100, 2)
    prediction       = int(np.argmax(probs))
    label            = "FAKE" if prediction == 0 else "REAL"

    # Result object
    result = {
        "label": label,
        "confidence": confidence,
        "fake_probability": fake_probability,
        "real_probability": real_probability,
        "fact_check": None,
        "fact_url": None,
        "news_verified": False,
        "trusted_sources_count": 0,
        "verification_note": None
    }

    # ── Step 2: Google Fact Check ──
    fact = check_facts(text)

    if fact["found"]:
        rating = fact["rating_lower"]

        fake_keywords = ["false", "fake", "misleading", "pants on fire", "incorrect", "fabricated", "manipulated"]
        real_keywords = ["true", "correct", "accurate", "verified", "confirmed"]

        if any(word in rating for word in fake_keywords):
            result["label"] = "FAKE"
            result["fact_check"] = f"⚠️ Fact-checked: {fact['rating']} — by {fact['source']}"
            result["fact_url"]   = fact["url"]

        elif any(word in rating for word in real_keywords):
            result["label"] = "REAL"
            result["fact_check"] = f"✅ Fact-checked: {fact['rating']} — by {fact['source']}"
            result["fact_url"]   = fact["url"]

        else:
            result["fact_check"] = f"ℹ️ Fact-checked: {fact['rating']} — by {fact['source']}"
            result["fact_url"]   = fact["url"]

    # ── Step 3: NewsAPI Verification ──
    news = verify_with_news(text)

    result["news_verified"]        = news["verified"]
    result["trusted_sources_count"] = news["trusted_count"]

    if news["verified"] and result["label"] == "FAKE":
        result["verification_note"] = f"⚠️ Found in {news['trusted_count']} trusted source(s) — manual verification recommended"

    elif news["verified"] and result["label"] == "REAL":
        result["verification_note"] = f"✅ Confirmed in {news['trusted_count']} trusted source(s)"

    elif not news["verified"] and result["label"] == "REAL":
        result["verification_note"] = "⚠️ Not found in trusted sources — verify manually"

    return result