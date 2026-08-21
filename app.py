import time
import streamlit as st
from src.scraper import scrape_article
from src.predict import predict_news
from src.news_search import search_related_news

# Page config
st.set_page_config(
    page_title="TruthLens - Fake News Detection",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🔍 TruthLens - Fake News Detection")
st.caption("Powered by DistilBERT Multilingual Model — 94% Accuracy")

# Session state
if "option" not in st.session_state:
    st.session_state.option = "Text"

# Input option
option = st.radio("Choose input type", ["Text", "URL"])

article_text = ""
result = None

if option == "Text":
    article_text = st.text_area("Enter news text", height=250)

elif option == "URL":
    url = st.text_input("Enter news URL")

if st.button("🔍 Predict"):

    if option == "Text":
        if not article_text.strip():
            st.error("Please enter news text")
            st.stop()

    elif option == "URL":
        if not url.strip():
            st.error("Please enter URL")
            st.stop()

        with st.spinner("Extracting article..."):
            article_text = scrape_article(url)

        if not article_text:
            st.error("Could not extract article from URL. Try BBC, Reuters, or other major news sites.")
            st.stop()

    # Prediction
    with st.spinner("Analyzing with DistilBERT..."):
        result = predict_news(article_text)

    # Result display
    label      = result["label"]
    confidence = result["confidence"]
    fake_prob  = result["fake_probability"]
    real_prob  = result["real_probability"]

    if label == "REAL":
        st.success(f"✅ REAL NEWS — Confidence: {confidence}%")
    else:
        st.error(f"⚠️ FAKE NEWS — Confidence: {confidence}%")

    col1, col2 = st.columns(2)
    col1.metric("🔴 Fake Probability", f"{fake_prob}%")
    col2.metric("🟢 Real Probability", f"{real_prob}%")

    st.progress(confidence / 100)

    # Fact check result
    if result.get("fact_check"):
        st.info(result["fact_check"])
        if result.get("fact_url"):
            st.markdown(f"[🔗 Read fact-check]({result['fact_url']})")

    if result.get("verification_note"):
        st.warning(result["verification_note"])

    st.divider()

    # Related news
    st.subheader("🔍 Related Trusted Evidence")
    with st.spinner("Searching related articles..."):
        related_news = search_related_news(article_text)

    if related_news:
        for article in related_news:
            with st.container():
                st.write("📰", article["title"])
                st.write("Source:", article["source"])
                st.write("Trust Score:", article["source_score"], "/5")
                st.write(article["url"])
                st.divider()
    else:
        st.warning("No related articles found")