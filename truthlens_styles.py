TRUTHLENS_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ─── Reset & Base ─────────────────────────────────────────── */
html, body, [data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #EEF2FF 0%, #F5F3FF 40%, #EFF6FF 100%) !important;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

/* ─── Floating gradient blobs (soft, slow drift) ─────────────
   Two blurred radial blobs living behind the content. They sit
   on the app container itself via pseudo-elements so they never
   depend on widget order or get orphaned like a stray <div>. */
[data-testid="stAppViewContainer"]::before,
[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed;
    z-index: 0;
    border-radius: 50%;
    filter: blur(70px);
    pointer-events: none;
    opacity: 0.55;
}

[data-testid="stAppViewContainer"]::before {
    width: 420px;
    height: 420px;
    top: -120px;
    left: -100px;
    background: radial-gradient(circle, #C7D2FE 0%, transparent 70%);
    animation: tl-float-a 16s ease-in-out infinite alternate;
}

[data-testid="stAppViewContainer"]::after {
    width: 380px;
    height: 380px;
    bottom: -100px;
    right: -80px;
    background: radial-gradient(circle, #BBF7D0 0%, transparent 70%);
    animation: tl-float-b 18s ease-in-out infinite alternate;
}

@keyframes tl-float-a {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(60px, 90px) scale(1.15); }
}
@keyframes tl-float-b {
    0%   { transform: translate(0, 0) scale(1); }
    100% { transform: translate(-50px, -70px) scale(1.1); }
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="block-container"] {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 860px !important;
    position: relative;
    z-index: 1;
}

* {
    font-family: 'Inter', sans-serif !important;
}

/* ─── Hero Section ─────────────────────────────────────────── */
.tl-hero {
    text-align: center;
    padding: 3.5rem 2rem 2rem;
    position: relative;
}

.tl-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.25);
    color: #6366F1;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 1.25rem;
}

.tl-hero-badge::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6366F1;
    animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.85); }
}

.tl-hero h1 {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    line-height: 1.1 !important;
    color: #0F0F1A !important;
    margin: 0 !important;
    padding: 0 !important;
}

.tl-hero h1 span {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.tl-hero-sub {
    color: #6B7280;
    font-size: 1rem;
    font-weight: 400;
    margin-top: 0.75rem;
    letter-spacing: -0.01em;
}

.tl-hero-sub strong {
    color: #374151;
    font-weight: 600;
}

/* ─── Main Card (real Streamlit container, border=True) ──────
   IMPORTANT: this replaces the old approach of opening/closing
   a raw <div class="tl-card"> across two separate st.markdown()
   calls. Each st.markdown() renders as its own isolated element,
   so that pattern never actually wrapped the widgets — it just
   left an empty, styled, unclosed div sitting on the page (the
   "blank box" bug). Use st.container(border=True) in app.py and
   style the real wrapper Streamlit gives you instead. */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border: 1px solid rgba(0,0,0,0.07) !important;
    border-radius: 20px !important;
    padding: 0.75rem !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.04), 0 2px 4px -1px rgba(0,0,0,0.02), 0 20px 40px -10px rgba(99,102,241,0.08) !important;
    margin-bottom: 1.5rem !important;
}

/* ─── Tab Selector ─────────────────────────────────────────── */
[data-testid="stRadio"] {
    margin-bottom: 1.25rem;
}

[data-testid="stRadio"] > label {
    display: none !important;
}

[data-testid="stRadio"] > div {
    display: flex !important;
    gap: 8px !important;
    background: #F3F4F6 !important;
    padding: 4px !important;
    border-radius: 12px !important;
    width: fit-content !important;
}

[data-testid="stRadio"] > div > label {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 8px 20px !important;
    border-radius: 9px !important;
    cursor: pointer !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    transition: all 0.2s ease !important;
    border: none !important;
    background: transparent !important;
}

[data-testid="stRadio"] > div > label:has(input:checked) {
    background: #FFFFFF !important;
    color: #1F2937 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
}

[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
}

/* ─── Text Area ────────────────────────────────────────────── */
[data-testid="stTextArea"] textarea,
[data-testid="stTextInput"] input {
    background: #F9FAFB !important;
    border: 1.5px solid #E5E7EB !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1F2937 !important;
    padding: 14px 16px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    line-height: 1.6 !important;
}

[data-testid="stTextArea"] textarea:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
    background: #FFFFFF !important;
    outline: none !important;
}

[data-testid="stTextArea"] label,
[data-testid="stTextInput"] label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: #374151 !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
    margin-bottom: 6px !important;
}

/* ─── Button ────────────────────────────────────────────────── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(99,102,241,0.35) !important;
    margin-top: 1rem !important;
}

[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.45) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ─── Shared entrance animation ──────────────────────────────
   Every result block fades + rises in on render, staggered, so
   the whole analysis panel feels like it just finished loading
   rather than popping in all at once. */
@keyframes tl-fade-up {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes tl-pop {
    0%   { opacity: 0; transform: scale(0.85); }
    60%  { transform: scale(1.04); }
    100% { opacity: 1; transform: scale(1); }
}

/* ─── Result Cards ──────────────────────────────────────────── */
.tl-result {
    border-radius: 16px;
    padding: 1.5rem 1.75rem;
    margin: 1.5rem 0;
    border: 1.5px solid;
    display: flex;
    align-items: flex-start;
    gap: 14px;
    animation: tl-fade-up 0.5s ease-out both;
}

.tl-result.real {
    background: linear-gradient(135deg, #F0FDF4 0%, #ECFDF5 100%);
    border-color: rgba(16, 185, 129, 0.3);
}

.tl-result.fake {
    background: linear-gradient(135deg, #FFF5F5 0%, #FEF2F2 100%);
    border-color: rgba(239, 68, 68, 0.3);
}

.tl-result-icon {
    font-size: 1.75rem;
    line-height: 1;
    flex-shrink: 0;
    animation: tl-pop 0.55s cubic-bezier(.34,1.56,.64,1) 0.1s both;
}

.tl-result-label {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.2;
    animation: tl-pop 0.5s cubic-bezier(.34,1.56,.64,1) 0.15s both;
}

.real .tl-result-label { color: #065F46; }
.fake .tl-result-label { color: #7F1D1D; }

.tl-result-conf {
    font-size: 0.85rem;
    font-weight: 500;
    margin-top: 3px;
    color: #6B7280;
    animation: tl-fade-up 0.5s ease-out 0.25s both;
}

/* ─── Metrics Grid ──────────────────────────────────────────── */
.tl-metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    margin: 1rem 0;
    animation: tl-fade-up 0.5s ease-out 0.15s both;
}

.tl-metric {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    text-align: center;
}

.tl-metric-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.75rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1;
    animation: tl-pop 0.5s cubic-bezier(.34,1.56,.64,1) 0.35s both;
}

.tl-metric-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #9CA3AF;
    margin-top: 4px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

/* ─── Progress Bar ──────────────────────────────────────────── */
.tl-progress-wrap {
    margin: 1rem 0;
    animation: tl-fade-up 0.5s ease-out 0.2s both;
}

.tl-progress-label {
    display: flex;
    justify-content: space-between;
    font-size: 0.78rem;
    font-weight: 600;
    color: #6B7280;
    margin-bottom: 6px;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.tl-progress-track {
    background: #F3F4F6;
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
}

/* Animated fill: driven by a CSS variable set inline per-card
   (--target-width), animated with @keyframes rather than
   `transition`, since transition needs a property CHANGE after
   paint to fire — and this HTML is injected once, fully-formed,
   so a transition would never actually trigger. */
.tl-progress-fill {
    height: 100%;
    border-radius: 100px;
    width: 0%;
    animation: tl-fill-bar 1.1s cubic-bezier(.65,0,.35,1) 0.3s forwards;
}

@keyframes tl-fill-bar {
    from { width: 0%; }
    to   { width: var(--target-width, 0%); }
}

.tl-progress-fill.real { background: linear-gradient(90deg, #34D399, #10B981); }
.tl-progress-fill.fake { background: linear-gradient(90deg, #F87171, #EF4444); }

/* ─── Fact Check Banner ─────────────────────────────────────── */
.tl-factcheck {
    background: linear-gradient(135deg, #EFF6FF 0%, #EDE9FE 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    margin: 1rem 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    animation: tl-fade-up 0.5s ease-out 0.3s both;
}

.tl-factcheck-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }

.tl-factcheck-body p {
    font-size: 0.875rem;
    color: #374151;
    margin: 0 0 6px 0;
    line-height: 1.55;
}

.tl-factcheck-body a {
    font-size: 0.8rem;
    font-weight: 600;
    color: #6366F1;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.tl-factcheck-body a:hover { text-decoration: underline; }

.tl-warning {
    background: #FFFBEB;
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 14px;
    padding: 1rem 1.25rem;
    margin: 0.75rem 0;
    font-size: 0.875rem;
    color: #92400E;
    display: flex;
    gap: 8px;
    align-items: flex-start;
    line-height: 1.5;
    animation: tl-fade-up 0.5s ease-out 0.3s both;
}

/* ─── Section Divider ───────────────────────────────────────── */
.tl-divider {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0 1.5rem;
    animation: tl-fade-up 0.5s ease-out 0.35s both;
}

.tl-divider-line {
    flex: 1;
    height: 1px;
    background: #E5E7EB;
}

.tl-divider-text {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #9CA3AF;
    white-space: nowrap;
}

/* ─── Related Articles ──────────────────────────────────────── */
.tl-article {
    background: #FFFFFF;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 1.1rem 1.25rem;
    margin-bottom: 10px;
    transition: all 0.2s ease;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    animation: tl-fade-up 0.45s ease-out both;
}

.tl-article:hover {
    border-color: #C7D2FE;
    box-shadow: 0 4px 12px rgba(99,102,241,0.08);
    transform: translateY(-1px);
}

.tl-article-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #EEF2FF, #F5F3FF);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}

.tl-article-body { flex: 1; min-width: 0; }

.tl-article-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #1F2937;
    line-height: 1.4;
    margin-bottom: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.tl-article-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
}

.tl-article-source {
    font-size: 0.75rem;
    font-weight: 600;
    color: #6366F1;
}

.tl-article-sep { color: #D1D5DB; font-size: 0.75rem; }

.tl-article-score {
    font-size: 0.72rem;
    font-weight: 600;
    background: #F0FDF4;
    color: #065F46;
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 100px;
    padding: 2px 8px;
}

.tl-article-link {
    font-size: 0.75rem;
    color: #9CA3AF;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    margin-top: 3px;
    display: block;
}

/* ─── Spinner Override ──────────────────────────────────────── */
[data-testid="stSpinner"] > div {
    border-color: #6366F1 !important;
    border-right-color: transparent !important;
}

/* ─── Error / Success / Info overrides ─────────────────────── */
[data-testid="stAlert"] {
    border-radius: 14px !important;
    border-left-width: 0 !important;
    border-width: 1px !important;
}

/* ─── Hide default Streamlit chrome ────────────────────────── */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ─── Default metric & progress overrides ───────────────────── */
[data-testid="stMetricValue"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2rem !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, #6366F1, #8B5CF6) !important;
    border-radius: 100px !important;
}
[data-testid="stProgress"] > div {
    border-radius: 100px !important;
    background: #E5E7EB !important;
}

/* Respect reduced-motion preference */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after,
    .tl-result, .tl-result-icon, .tl-result-label, .tl-result-conf,
    .tl-metrics, .tl-metric-value, .tl-progress-wrap, .tl-progress-fill,
    .tl-factcheck, .tl-warning, .tl-divider, .tl-article,
    .tl-hero-badge::before {
        animation: none !important;
    }
    .tl-progress-fill { width: var(--target-width, 0%) !important; }
}
</style>
"""