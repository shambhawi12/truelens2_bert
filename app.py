import threading
from datetime import date
from html import escape

import streamlit as st

from site_config import FAVICON_PATH
from src.scraper import scrape_article
from src.news_search import search_related_news
from truthlens_styles import NAV_HTML, TRUTHLENS_CSS

# Page config
st.set_page_config(
    page_title="TruthLens: Fake News Detection",
    page_icon=FAVICON_PATH,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(TRUTHLENS_CSS, unsafe_allow_html=True)


# Speed: load the model in the background while the page draws
@st.cache_resource(show_spinner=False)
def _warm_up() -> bool:
    def _load():
        try:
            import src.predict  # noqa: F401
        except Exception:
            pass

    threading.Thread(target=_load, daemon=True).start()
    return True


_warm_up()


# Speed: cache repeat work so the same input is not processed twice
@st.cache_data(show_spinner=False, ttl=3600, max_entries=64)
def cached_predict(text: str) -> dict:
    from src.predict import predict_news

    return predict_news(text)


@st.cache_data(show_spinner=False, ttl=900, max_entries=32)
def cached_scrape(url: str) -> str:
    text = scrape_article(url)
    if not text:
        raise ValueError("No article text extracted")
    return text


@st.cache_data(show_spinner=False, ttl=600, max_entries=64)
def cached_search(text: str) -> list:
    return search_related_news(text) or []


# Helpers
def flatten(html: str) -> str:
    """Strip leading whitespace so Markdown never treats indented HTML as code."""
    return " ".join(line.strip() for line in html.splitlines() if line.strip())


def variant() -> str:
    """Alternate between two identical animation sets so they replay on every run."""
    return "a" if st.session_state.get("run_id", 0) % 2 == 0 else "b"


def reveal(html: str, delay: float = 0) -> str:
    """Wrap a snippet in the staggered reveal animation."""
    return f'<div class="v-{variant()}" style="--d:{delay}s">{flatten(html)}</div>'


def show(html: str, delay=None, target=None) -> None:
    body = flatten(html) if delay is None else reveal(html, delay)
    (target if target is not None else st).markdown(body, unsafe_allow_html=True)


def show_loader(target, text: str) -> None:
    target.markdown(
        f'<div class="tl-loader"><div class="tl-loader-text">{escape(text)}</div>'
        '<div class="tl-track"><i></i></div></div>',
        unsafe_allow_html=True,
    )


def safe_url(value) -> str:
    """Allow only http and https links."""
    if isinstance(value, str) and value.lower().startswith(("http://", "https://")):
        return escape(value, quote=True)
    return "#"


def to_pct(value) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(100.0, number))


def count(number: int) -> str:
    return f'<span class="tl-count" style="--t:{number}" aria-label="{number}%"></span>'


SKELETON_HTML = '<div class="tl-skel"><i></i></div>' * 3

# Header and hero
st.markdown(NAV_HTML + '<div id="tl-top"></div>', unsafe_allow_html=True)
show("""
<div class="tl-hero-grid">
    <div>
        <h1 class="tl-intro" style="--d:0.05s">Check a news article <span class="tl-ul">before you share it</span></h1>
        <p class="tl-hero-sub tl-intro" style="--d:0.18s">
            Paste the article text or enter a link. A multilingual DistilBERT model
            estimates whether it is real or fake, and TruthLens lists related coverage
            so you can check the claim yourself.
        </p>
    </div>
    <div class="tl-visual tl-intro" style="--d:0.3s" aria-hidden="true">
        <div class="tl-float">
            <div class="tl-stage">
                <div class="tl-sheet s3"></div>
                <div class="tl-sheet s2"></div>
                <div class="tl-sheet s1">
                    <div class="tl-l t"></div>
                    <div class="tl-l w100"></div>
                    <div class="tl-l w92 m" style="--md:0.2s"></div>
                    <div class="tl-l w85"></div>
                    <div class="tl-l w100"></div>
                    <div class="tl-l w60 m" style="--md:3s"></div>
                    <div class="tl-l w95"></div>
                    <div class="tl-l w80"></div>
                    <div class="tl-l w100 m" style="--md:4.5s"></div>
                    <div class="tl-l w50"></div>
                </div>
                <div class="tl-lens-shadow"></div>
                <div class="tl-lens"></div>
            </div>
            <div class="tl-floor"></div>
        </div>
    </div>
</div>
""")

# Input (anchor target for the navbar Analyze Article button; it only scrolls here)
st.markdown('<div id="analyze-article" class="tl-anchor"></div>', unsafe_allow_html=True)
option = st.radio(
    "Input type",
    ["Text", "URL"],
    horizontal=True,
    label_visibility="collapsed",
)

article_text = ""
url = ""

with st.form("analyze_form", clear_on_submit=False):
    if option == "Text":
        article_text = st.text_area(
            "News article",
            height=220,
            placeholder="Paste the news article text here",
        )
    else:
        url = st.text_input(
            "Article URL",
            placeholder="https://www.bbc.com/news/...",
        )
    analyze_clicked = st.form_submit_button("Analyze article")


def run_analysis(option: str, article_text: str, url: str) -> None:
    """Run the analysis and render results. Returns early on errors."""
    st.session_state["run_id"] = st.session_state.get("run_id", 0) + 1

    loader = st.empty()
    try:
        if option == "Text":
            if not article_text.strip():
                st.error("Please paste some article text to analyze.")
                return
        else:
            if not url.strip():
                st.error("Please enter a URL to analyze.")
                return

            show_loader(loader, "Extracting article")
            try:
                article_text = cached_scrape(url.strip())
            except Exception:
                article_text = ""

            if not article_text:
                st.error(
                    "Could not extract the article. Try a link from BBC, Reuters, "
                    "AP News or another major outlet, or paste the text instead."
                )
                return

        show_loader(loader, "Analyzing article")
        result = cached_predict(article_text)
    finally:
        loader.empty()

    label = result["label"]
    confidence = int(round(to_pct(result["confidence"])))
    fake_exact = to_pct(result["fake_probability"])
    real_exact = to_pct(result["real_probability"])
    fake_int = int(round(fake_exact))
    real_int = int(round(real_exact))
    if abs(fake_exact + real_exact - 100) < 1.5:
        real_int = 100 - fake_int

    verdict_class = "real" if label == "REAL" else "fake"
    verdict_text = "Likely real" if label == "REAL" else "Likely fake"

    # Verdict
    show(f"""
    <div class="tl-verdict {verdict_class}">
        <div class="tl-coin"><div class="tl-badge {verdict_class}"></div></div>
        <div class="tl-verdict-main">
            <div class="tl-kicker">Model verdict</div>
            <div class="tl-verdict-label">{verdict_text}</div>
        </div>
        <div class="tl-verdict-score">
            <div class="tl-verdict-num">{count(confidence)}</div>
            <div class="tl-verdict-cap">model confidence</div>
        </div>
    </div>
    """, delay=0)

    # Probability split
    show(f"""
    <div class="tl-split">
        <div class="tl-split-head">
            <span>Fake <b>{count(fake_int)}</b></span>
            <span>Real <b>{count(real_int)}</b></span>
        </div>
        <div class="tl-split-track">
            <div class="tl-split-fake" style="--w:{fake_exact:.2f}%"></div>
            <div class="tl-split-real" style="--w:{real_exact:.2f}%"></div>
        </div>
    </div>
    """, delay=0.1)

    # Fact check
    if result.get("fact_check"):
        fact_url_html = ""
        if result.get("fact_url"):
            fact_url_html = (
                f'<a href="{safe_url(result["fact_url"])}" target="_blank" '
                f'rel="noopener noreferrer">Read the full fact check</a>'
            )
        show(f"""
        <div class="tl-factcheck">
            <div class="tl-kicker">Fact check</div>
            <p>{escape(str(result["fact_check"]))}</p>
            {fact_url_html}
        </div>
        """, delay=0.2)

    if result.get("verification_note"):
        show(f"""
        <div class="tl-note">{escape(str(result["verification_note"]))}</div>
        """, delay=0.25)

    # Related coverage: skeleton first, real rows once the search returns
    show('<div class="tl-section"><span>Related trusted sources</span></div>', delay=0.3)
    related_slot = st.empty()
    related_slot.markdown(SKELETON_HTML, unsafe_allow_html=True)

    try:
        related_news = cached_search(article_text)
    except Exception:
        related_news = []

    rows = []
    for index, article in enumerate(related_news):
        title = escape(str(article.get("title") or "Untitled"))
        source = escape(str(article.get("source") or "Unknown source"))
        score = article.get("source_score")
        raw_link = article.get("url") or "#"
        link = safe_url(raw_link)

        short_link = str(raw_link).replace("https://", "").replace("http://", "")
        if len(short_link) > 60:
            short_link = short_link[:60] + "..."
        short_link = escape(short_link)

        rating_html = ""
        if score not in (None, ""):
            try:
                value = float(score)
                tone = "hi" if value >= 4 else "mid" if value >= 3 else "lo"
            except (TypeError, ValueError):
                tone = ""
            rating_html = (
                '<span class="tl-article-sep">&middot;</span>'
                f'<span class="tl-rate {tone}">Source rating {escape(str(score))}/5</span>'
            )

        rows.append(reveal(f"""
        <a class="tl-article-link" href="{link}" target="_blank" rel="noopener noreferrer">
            <div class="tl-article">
                <div class="tl-article-title">{title}</div>
                <div class="tl-article-meta"><span>{source}</span>{rating_html}</div>
                <span class="tl-article-url">{short_link}</span>
            </div>
        </a>
        """, delay=round(0.05 + index * 0.07, 2)))

    if not rows:
        rows.append(reveal("""
        <div class="tl-note">
            No related sources were found for this article. Try pasting more of the text.
        </div>
        """, delay=0.05))

    related_slot.markdown(" ".join(rows), unsafe_allow_html=True)

    show("""
    <div class="tl-disclaimer">
        This result comes from a machine learning model and can be wrong. Treat it as a
        starting point and check the claims against sources you trust before you share
        or act on it.
    </div>
    """, delay=0.2)


if analyze_clicked:
    run_analysis(option, article_text, url)

# How it works (always rendered so the navbar anchor works after an analysis too)
show("""
<div id="how-it-works" class="tl-anchor"></div>
<div class="tl-steps">
    <div class="tl-step tl-intro" style="--d:0.45s">
        <div class="tl-step-num">01</div>
        <div class="tl-step-title">Add an article</div>
        <p class="tl-step-text">Paste the text or enter the link to a news page.</p>
    </div>
    <div class="tl-step tl-intro" style="--d:0.55s">
        <div class="tl-step-num">02</div>
        <div class="tl-step-title">The model reads it</div>
        <p class="tl-step-text">A multilingual DistilBERT model scores how likely the text is real or fake.</p>
    </div>
    <div class="tl-step tl-intro" style="--d:0.65s">
        <div class="tl-step-num">03</div>
        <div class="tl-step-title">Check the context</div>
        <p class="tl-step-text">Related coverage and fact checks are listed so you can verify the claim.</p>
    </div>
</div>
""")

# Features, About, FAQ (only facts that are visible in this codebase)
show("""
<div id="features" class="tl-block tl-anchor">
    <h2>Features</h2>
    <div class="tl-feat-grid">
        <div class="tl-feat"><b>Text or link</b><span>Paste the article text or enter a URL and the article is extracted for you.</span></div>
        <div class="tl-feat"><b>Real or fake estimate</b><span>A multilingual DistilBERT model returns a verdict, a confidence score and the fake/real probability split.</span></div>
        <div class="tl-feat"><b>Fact checks</b><span>When a matching fact check is found, it is shown with a link to the full write-up.</span></div>
        <div class="tl-feat"><b>Related coverage</b><span>Related articles are listed with a source rating so you can read further and check the claim yourself.</span></div>
    </div>
</div>
<div id="about" class="tl-block tl-anchor">
    <h2>About TruthLens</h2>
    <div class="tl-about-grid">
        <div class="tl-about-text">
            <p>TruthLens is a small tool for people who want to pause before sharing a news article. You give it the
            text of a story, or a link to one, and it returns an estimate of whether the writing looks real or fake,
            along with a confidence score and the split between the two probabilities.</p>
            <p>The estimate comes from a multilingual DistilBERT model that reads the article text. Alongside it,
            TruthLens shows a matching fact check when one is found, and lists related coverage from other outlets
            with a source rating, so you can compare what different sources say about the same claim.</p>
            <p>The result is meant to be a starting point, not a final verdict. A machine learning model can be wrong,
            so the related sources and fact checks are there to help you do the last step yourself: read, compare
            and decide.</p>
        </div>
        <aside class="tl-glance">
            <div class="tl-glance-title">At a glance</div>
            <div class="tl-glance-row"><span>You provide</span><b>Article text or a link</b></div>
            <div class="tl-glance-row"><span>Model</span><b>Multilingual DistilBERT</b></div>
            <div class="tl-glance-row"><span>You get</span><b>Verdict, confidence and probability split</b></div>
            <div class="tl-glance-row"><span>For context</span><b>Fact checks and related sources</b></div>
        </aside>
    </div>
</div>
<div id="faq" class="tl-block tl-anchor tl-faq">
    <h2>FAQ</h2>
    <details><summary>Is the result proof that an article is real or fake?</summary>
        <p>No. It comes from a machine learning model and can be wrong. Related sources are for comparison and do not prove a claim true or false.</p></details>
    <details><summary>What does the confidence score mean?</summary>
        <p>It shows how sure the model is about its own verdict. It is not a measure of how true the article is, so a high score can still be mistaken.</p></details>
    <details><summary>What is the Fake and Real split?</summary>
        <p>It shows how the model divides its estimate between the two outcomes. The two values add up to 100%, and the verdict follows the larger one.</p></details>
    <details><summary>Should I paste the text or use a link?</summary>
        <p>Both work. A link is quicker, but some pages cannot be read automatically. If a link fails, paste the article text instead.</p></details>
    <details><summary>What if a link cannot be read?</summary>
        <p>Try a link from a major outlet such as BBC, Reuters or AP News, or paste the article text instead.</p></details>
    <details><summary>What do the related sources show?</summary>
        <p>They list coverage on the same topic, with a source rating, so you can read other reports and compare.</p></details>
    <details><summary>How do I read the source rating?</summary>
        <p>The rating is out of 5 and describes the outlet, not the individual article. The dot beside it is green for 4 and above, amber for 3 and above, and red below 3.</p></details>
    <details><summary>Why is there no fact check on my result?</summary>
        <p>A fact check appears only when a matching one is found. If there is none, that does not mean the claim is true, so check it against the related sources.</p></details>
    <details><summary>Does it work with articles that are not in English?</summary>
        <p>The model is multilingual, so it is not limited to English. Results can still vary between languages and topics, so treat them with the same care.</p></details>
    <details><summary>How is my data handled?</summary>
        <p>Please read the Privacy Policy and the Terms and Conditions, linked at the bottom of this page, for details on how your input is handled.</p></details>
</div>
""")

# Footer: one dark panel (the key gives the container its own CSS class)
with st.container(key="tl_footer"):
    show("""
    <div class="tl-footer">
        <div>
            <div class="tl-brand"><span class="tl-brand-mark"></span><span>TruthLens</span></div>
            <p class="tl-footer-tag">Check the context. Question the claim.</p>
            <p class="tl-footer-desc">A multilingual DistilBERT model estimates whether a news article is real or fake,
            and TruthLens lists related coverage so you can check the claim yourself.</p>
            <a class="tl-footer-cta" href="#analyze-article" target="_self">Analyze an article</a>
        </div>
        <div>
            <div class="tl-footer-head">Explore</div>
            <div class="tl-footer-links">
                <a href="#how-it-works" target="_self">How It Works</a>
                <a href="#features" target="_self">Features</a>
                <a href="#about" target="_self">About</a>
                <a href="#faq" target="_self">FAQ</a>
            </div>
        </div>
    </div>
    <div class="tl-footer-rule"></div>
    """)
    footer_left, footer_right, footer_note = st.columns([1, 1.4, 1.6])
    with footer_left:
        st.page_link("pages/1_Privacy_Policy.py", label="Privacy Policy")
    with footer_right:
        st.page_link("pages/2_Terms_and_Conditions.py", label="Terms and Conditions")
    with footer_note:
        show(f'<div class="tl-footer-note">&copy; {date.today().year} TruthLens</div>')