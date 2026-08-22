import streamlit as st
from src.scraper import scrape_article
from src.predict import predict_news
from src.news_search import search_related_news
from truthlens_styles import TRUTHLENS_CSS

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens — Fake News Detection",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── Inject CSS ────────────────────────────────────────────────
st.markdown(TRUTHLENS_CSS, unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="tl-hero">
    <div class="tl-hero-badge">Live Analysis &nbsp;·&nbsp; 94% Accuracy</div>
    <h1>Detect fake news with<br><span>AI precision</span></h1>
    <p class="tl-hero-sub">
        Powered by <strong>DistilBERT Multilingual</strong> — paste an article or drop a URL
    </p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────
if "option" not in st.session_state:
    st.session_state.option = "Text"

# ── Input card ────────────────────────────────────────────────
# NOTE: this uses a real Streamlit container (border=True) instead of
# hand-written <div class="tl-card">...</div> markdown split across two
# separate st.markdown() calls. That old pattern never actually wrapped
# the widgets — each st.markdown() is its own isolated DOM node, so the
# opening div rendered alone, auto-closed itself, and just sat there as
# an empty padded white box. That was the blank box under the hero.
with st.container(border=True):
    option = st.radio("Choose input type", ["Text", "URL"], horizontal=True)

    article_text = ""
    result = None

    if option == "Text":
        article_text = st.text_area(
            "News article",
            height=220,
            placeholder="Paste the news article text here…",
        )
    else:
        url = st.text_input(
            "Article URL",
            placeholder="https://bbc.com/news/…",
        )

    analyze_clicked = st.button("🔍 Analyze Article")

# ── Analysis ──────────────────────────────────────────────────
if analyze_clicked:

    if option == "Text":
        if not article_text.strip():
            st.error("Please paste some article text to analyze.")
            st.stop()

    elif option == "URL":
        if not url.strip():
            st.error("Please enter a URL to analyze.")
            st.stop()

        with st.spinner("Extracting article…"):
            article_text = scrape_article(url)

        if not article_text:
            st.error("Couldn't extract the article. Try BBC, Reuters, AP News, or other major outlets.")
            st.stop()

    with st.spinner("Running DistilBERT analysis…"):
        result = predict_news(article_text)

    label      = result["label"]
    confidence = result["confidence"]
    fake_prob  = result["fake_probability"]
    real_prob  = result["real_probability"]

    verdict_class = "real" if label == "REAL" else "fake"
    verdict_icon  = "✅" if label == "REAL" else "⚠️"
    verdict_text  = "Real News" if label == "REAL" else "Fake News"

    # ── Verdict card ──────────────────────────────────────────
    st.markdown(f"""
    <div class="tl-result {verdict_class}">
        <div class="tl-result-icon">{verdict_icon}</div>
        <div>
            <div class="tl-result-label">{verdict_text}</div>
            <div class="tl-result-conf">Model confidence: {confidence}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Probability metrics ───────────────────────────────────
    st.markdown(f"""
    <div class="tl-metrics">
        <div class="tl-metric">
            <div class="tl-metric-value" style="color:#EF4444">{fake_prob}%</div>
            <div class="tl-metric-label">Fake probability</div>
        </div>
        <div class="tl-metric">
            <div class="tl-metric-value" style="color:#10B981">{real_prob}%</div>
            <div class="tl-metric-label">Real probability</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Confidence bar ────────────────────────────────────────
    # Width is driven by the --target-width CSS variable, animated via
    # @keyframes in the stylesheet (see tl-fill-bar), so the bar visibly
    # fills up on each render instead of appearing already-full.
    st.markdown(f"""
    <div class="tl-progress-wrap">
        <div class="tl-progress-label">
            <span>Confidence</span>
            <span>{confidence}%</span>
        </div>
        <div class="tl-progress-track">
            <div class="tl-progress-fill {verdict_class}" style="--target-width:{confidence}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Fact check ────────────────────────────────────────────
    if result.get("fact_check"):
        fact_url_html = ""
        if result.get("fact_url"):
            fact_url_html = f'<a href="{result["fact_url"]}" target="_blank">🔗 Read full fact-check</a>'
        st.markdown(f"""
        <div class="tl-factcheck">
            <div class="tl-factcheck-icon">🔎</div>
            <div class="tl-factcheck-body">
                <p>{result["fact_check"]}</p>
                {fact_url_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    if result.get("verification_note"):
        st.markdown(f"""
        <div class="tl-warning">
            <span>⚡</span>
            <span>{result["verification_note"]}</span>
        </div>
        """, unsafe_allow_html=True)

    # ── Related news ──────────────────────────────────────────
    st.markdown("""
    <div class="tl-divider">
        <div class="tl-divider-line"></div>
        <div class="tl-divider-text">Related trusted sources</div>
        <div class="tl-divider-line"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("Finding corroborating sources…"):
        related_news = search_related_news(article_text)

    if related_news:
        for article in related_news:
            title  = article.get("title", "Untitled")
            source = article.get("source", "Unknown")
            score  = article.get("source_score", "—")
            link   = article.get("url", "#")

            short_link = link.replace("https://", "").replace("http://", "")
            if len(short_link) > 55:
                short_link = short_link[:55] + "…"

            st.markdown(f"""
            <a href="{link}" target="_blank" style="text-decoration:none">
                <div class="tl-article">
                    <div class="tl-article-icon">📰</div>
                    <div class="tl-article-body">
                        <div class="tl-article-title">{title}</div>
                        <div class="tl-article-meta">
                            <span class="tl-article-source">{source}</span>
                            <span class="tl-article-sep">·</span>
                            <span class="tl-article-score">★ {score}/5</span>
                        </div>
                        <span class="tl-article-link">{short_link}</span>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="tl-warning">
            <span>🔍</span>
            <span>No corroborating sources found for this article. Try refining the text.</span>
        </div>
        """, unsafe_allow_html=True)

        # ── ML disclaimer ─────────────────────────────────────────
    st.markdown("""
    <div class="tl-warning" style="margin-top: 1.5rem;">
        <span>🤖</span>
        <span>This result is generated by a machine learning model and is intended to provide an informative starting point. While every effort is made to ensure accuracy, users are kindly encouraged to verify the information through reliable and trusted sources before drawing any conclusions.</span>
    </div>
    """, unsafe_allow_html=True)