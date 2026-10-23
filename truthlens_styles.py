from html import escape

# Set to a real destination, e.g. "mailto:you@example.com". While empty, the
# Contact link is left out so there is no dead link.
CONTACT_HREF = ""

_NAV_LINKS = [
    ("how-it-works", "How It Works"),
    ("features", "Features"),
    ("about", "About"),
    ("faq", "FAQ"),
]


def build_nav(prefix: str = "") -> str:
    """Build the navbar. On other pages use build_nav('/') so anchors point home."""
    items = [(f"{prefix}#{anchor}", label) for anchor, label in _NAV_LINKS]
    if CONTACT_HREF:
        items.append((CONTACT_HREF, "Contact"))
    links = "".join(
        f'<a href="{escape(href, quote=True)}" target="_self">{escape(label)}</a>'
        for href, label in items
    )
    cta = f'<a class="tl-cta" href="{prefix}#analyze-article" target="_self">Analyze Article</a>'
    return (
        '<div class="tl-nav"><div class="tl-nav-inner">'
        f'<a class="tl-brand" href="{prefix}#tl-top" target="_self">'
        '<span class="tl-brand-mark"></span><span>TruthLens</span></a>'
        f'<nav class="tl-nav-links" aria-label="Primary">{links}</nav>'
        f"{cta}"
        '<details class="tl-menu"><summary aria-label="Open menu">Menu</summary>'
        f'<div class="tl-menu-panel">{links}</div></details>'
        "</div></div>"
    )


NAV_HTML = build_nav()

_BASE_CSS = """
:root {
    --tl-bg: #F6F5F1;
    --tl-surface: #FFFFFF;
    --tl-ink: #14181F;
    --tl-ink-2: #4A5260;
    --tl-ink-3: #7A8290;
    --tl-line: #E5E3DC;
    --tl-accent: #1F3A5F;
    --tl-accent-hover: #16304F;
    --tl-real: #17653F;
    --tl-fake: #A6282B;
    --tl-slate: #6E87A8;
    --tl-ochre: #B8892B;
    --tl-sage: #6E9A82;
    --tl-tint-blue: #F1F4F8;
    --tl-tint-blue-line: #D6DEE9;
    --tl-tint-real: #F1F7F3;
    --tl-tint-real-line: #CFE3D7;
    --tl-tint-fake: #FBF2F1;
    --tl-tint-fake-line: #EBCFCD;
    --tl-caution-bg: #FAF4E3;
    --tl-caution-line: #E6D8A8;
    --tl-dark: #111C2B;
    --tl-shadow: 0 1px 2px rgba(20, 24, 31, 0.04), 0 8px 24px rgba(20, 24, 31, 0.05);
    --tl-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    --tl-ease: cubic-bezier(0.2, 0.7, 0.2, 1);
}

@property --n {
    syntax: "<integer>";
    inherits: false;
    initial-value: 0;
}

/* Hide Streamlit chrome */
#MainMenu { display: none; }
footer { display: none !important; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDeployButton"] { display: none; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stStatusWidget"] { display: none; }
header[data-testid="stHeader"] { background: transparent; height: 0; }

/* Streamlit adds a hover link icon to every heading. It only reloads the page, so it is hidden. */
.stApp [data-testid="stHeaderActionElements"] { display: none !important; }
.stApp [data-testid="stMarkdownContainer"] :is(h1, h2, h3, h4, h5, h6) > a[href^="#"] { display: none !important; }

/* Base: warm paper with a faint dot grid */
.stApp {
    background-color: var(--tl-bg);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26'><circle cx='1.2' cy='1.2' r='1.2' fill='%23DAD7CC'/></svg>");
    color: var(--tl-ink);
}
.stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp textarea,
.stApp button, .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
    font-family: var(--tl-font);
}
.block-container { padding-top: 6.25rem; padding-bottom: 3rem; max-width: 920px; }

/* Smooth anchor scrolling (Streamlit scrolls stMain, not html) */
html, [data-testid="stMain"] { scroll-behavior: smooth; }
.tl-anchor { scroll-margin-top: 104px; }

/* Intro motion (plays once when the page first draws) */
@keyframes tl-intro {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: none; }
}
.tl-intro { animation: tl-intro 0.7s var(--tl-ease) both; animation-delay: var(--d, 0s); }

/* Navbar: a floating, rounded frosted bar (fallback is a more opaque surface) */
.tl-nav {
    position: fixed;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    width: min(888px, calc(100% - 2rem));
    border-radius: 18px;
    background: rgba(246, 245, 241, 0.94);
    border: 1px solid rgba(20, 24, 31, 0.08);
    box-shadow: 0 1px 2px rgba(20, 24, 31, 0.04), 0 10px 28px rgba(20, 24, 31, 0.08);
}
@supports ((-webkit-backdrop-filter: blur(1px)) or (backdrop-filter: blur(1px))) {
    .tl-nav {
        background: rgba(250, 249, 246, 0.64);
        -webkit-backdrop-filter: saturate(150%) blur(14px);
        backdrop-filter: saturate(150%) blur(14px);
    }
}
.tl-nav-inner {
    box-sizing: border-box; width: 100%; padding: 0 0.65rem 0 1.25rem;
    height: 60px; display: flex; align-items: center; gap: 1.5rem;
}
.tl-nav a { text-decoration: none !important; }
.tl-nav .tl-brand { margin-right: auto; color: var(--tl-ink) !important; padding-right: 0.5rem; }
.tl-nav-links { display: flex; align-items: center; gap: 1.4rem; }
.tl-nav-links a, .tl-menu-panel a {
    position: relative; font-size: 0.92rem; font-weight: 550;
    color: var(--tl-ink-2) !important; padding: 0.35rem 0; transition: color 0.15s ease;
}
.tl-nav-links a::after {
    content: ""; position: absolute; left: 0; right: 0; bottom: 0.1rem; height: 2px;
    background: var(--tl-accent); transform: scaleX(0); transform-origin: left;
    transition: transform 0.2s var(--tl-ease);
}
.tl-nav-links a:hover { color: var(--tl-accent) !important; }
.tl-nav-links a:hover::after { transform: scaleX(1); }
.tl-nav a.tl-cta {
    background: var(--tl-accent); color: #FFFFFF !important; font-size: 0.88rem; font-weight: 600;
    padding: 0.55rem 1rem; border-radius: 12px; white-space: nowrap; transition: background 0.15s ease;
}
.tl-nav a.tl-cta:hover { background: var(--tl-accent-hover); }
.tl-nav a:focus-visible, .tl-nav summary:focus-visible {
    outline: 2px solid var(--tl-accent); outline-offset: 3px; border-radius: 6px;
}
.tl-menu { display: none; position: relative; }
.tl-menu summary {
    list-style: none; cursor: pointer; font-size: 0.88rem; font-weight: 600;
    color: var(--tl-ink-2); padding: 0.5rem 0.8rem; min-height: 40px; box-sizing: border-box;
    border: 1px solid var(--tl-line); border-radius: 12px; display: flex; align-items: center;
}
.tl-menu summary::-webkit-details-marker { display: none; }
.tl-menu-panel {
    position: absolute; right: 0; top: calc(100% + 14px); min-width: 11rem;
    display: flex; flex-direction: column; gap: 0.2rem; padding: 0.6rem 1rem;
    background: rgba(255, 255, 255, 0.96); border: 1px solid var(--tl-line);
    border-radius: 16px; box-shadow: var(--tl-shadow);
}
.tl-menu-panel a { padding: 0.6rem 0; }

/* Brand */
.tl-brand {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    font-weight: 650;
    font-size: 1.05rem;
    letter-spacing: -0.01em;
    color: var(--tl-ink);
}
.tl-brand-mark {
    width: 18px;
    height: 18px;
    border: 3.5px solid var(--tl-accent);
    border-radius: 50%;
    position: relative;
    display: inline-block;
}
.tl-brand-mark::after {
    content: "";
    position: absolute;
    width: 3.5px;
    height: 8px;
    background: var(--tl-accent);
    right: -6px;
    bottom: -7px;
    transform: rotate(-45deg);
    border-radius: 1px;
}

/* Hero */
.tl-hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(0, 0.8fr);
    gap: 3rem;
    align-items: center;
    padding-bottom: 2.5rem;
}
.tl-hero-grid h1 {
    font-size: clamp(2.1rem, 4.6vw, 3.2rem);
    line-height: 1.08;
    font-weight: 650;
    letter-spacing: -0.03em;
    color: var(--tl-ink);
    margin: 0 0 1.1rem 0;
    padding: 0;
}
.tl-ul { position: relative; white-space: nowrap; z-index: 0; isolation: isolate; }
.tl-ul::after {
    content: "";
    position: absolute;
    left: -2px;
    right: -2px;
    bottom: 0.05em;
    height: 0.2em;
    background: rgba(184, 137, 43, 0.32);
    z-index: -1;
    transform-origin: left;
    animation: tl-underline 0.9s 0.7s var(--tl-ease) both;
}
@keyframes tl-underline { from { transform: scaleX(0); } to { transform: scaleX(1); } }
.tl-hero-sub {
    font-size: 1.08rem;
    line-height: 1.65;
    color: var(--tl-ink-2);
    margin: 0;
    max-width: 34rem;
}

/* Hero visual: a stack of pages in real 3D, examined by a lens.
   The scene sways slowly, the lens drifts across the top page and
   highlights passages as it passes over them. */
.tl-visual {
    position: relative;
    height: 290px;
    max-width: 290px;
    width: 100%;
    margin-left: auto;
    perspective: 1100px;
    perspective-origin: 50% 40%;
}
.tl-float { position: absolute; inset: 0; transform-style: preserve-3d; animation: tl-float 8s ease-in-out infinite; }
@keyframes tl-float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
.tl-stage {
    position: absolute;
    inset: 0;
    transform-style: preserve-3d;
    animation: tl-sway 14s ease-in-out infinite;
}
@keyframes tl-sway {
    0%, 100% { transform: rotateX(9deg) rotateY(-17deg) rotateZ(1deg); }
    50% { transform: rotateX(5deg) rotateY(11deg) rotateZ(-1deg); }
}
.tl-sheet {
    position: absolute;
    inset: 0;
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    background: var(--tl-surface);
}
.tl-sheet.s3 { transform: translate3d(20px, 18px, -64px); background: #D9E0EA; }
.tl-sheet.s2 { transform: translate3d(10px, 9px, -32px); background: #EAE5D6; }
.tl-sheet.s1 {
    padding: 22px 20px;
    box-shadow: 0 1px 2px rgba(20, 24, 31, 0.05), 0 18px 36px rgba(20, 24, 31, 0.08);
    overflow: hidden;
    backface-visibility: hidden;
}
.tl-l { height: 8px; background: #E9E7E0; border-radius: 2px; margin-bottom: 11px; position: relative; }
.tl-l.t { height: 12px; width: 68%; background: #B7C3D4; margin-bottom: 18px; }
.tl-l.w100 { width: 100%; }
.tl-l.w95 { width: 95%; }
.tl-l.w92 { width: 92%; }
.tl-l.w85 { width: 85%; }
.tl-l.w80 { width: 80%; }
.tl-l.w60 { width: 60%; }
.tl-l.w50 { width: 50%; }
.tl-l.m::after {
    content: "";
    position: absolute;
    inset: -3px -5px;
    background: rgba(184, 137, 43, 0.3);
    border-radius: 3px;
    opacity: 0;
    animation: tl-mark 9s ease-in-out infinite;
    animation-delay: var(--md, 1s);
}
@keyframes tl-mark {
    0% { opacity: 0; }
    5%, 20% { opacity: 1; }
    30%, 100% { opacity: 0; }
}

/* The lens floats above the page. Its shadow lands on the page itself. */
.tl-lens, .tl-lens-shadow { position: absolute; left: 0; top: 0; width: 86px; height: 86px; }
.tl-lens { transform-style: preserve-3d; animation: tl-lens 9s ease-in-out infinite; }
.tl-lens::before {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 50%;
    border: 5px solid var(--tl-accent);
    background: radial-gradient(circle at 30% 26%, rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.14) 58%);
    box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.6), inset 0 -6px 12px rgba(31, 58, 95, 0.12);
}
.tl-lens::after {
    content: "";
    position: absolute;
    width: 9px;
    height: 44px;
    background: linear-gradient(90deg, #CDA650, #9A7120);
    border-radius: 5px;
    left: 70px;
    top: 66px;
    transform-origin: top center;
    transform: rotate(-45deg);
}
.tl-lens-shadow {
    border-radius: 50%;
    background: radial-gradient(circle, rgba(20, 24, 31, 0.2), rgba(20, 24, 31, 0) 68%);
    filter: blur(5px);
    transform: translate3d(0, 0, 1px);
    animation: tl-lens-shadow 9s ease-in-out infinite;
}
@keyframes tl-lens {
    0%, 100% { transform: translate3d(14px, 34px, 64px); }
    28% { transform: translate3d(150px, 66px, 64px); }
    55% { transform: translate3d(44px, 150px, 64px); }
    80% { transform: translate3d(140px, 192px, 64px); }
}
@keyframes tl-lens-shadow {
    0%, 100% { transform: translate3d(34px, 62px, 1px) scale(1.05); }
    28% { transform: translate3d(170px, 94px, 1px) scale(1.05); }
    55% { transform: translate3d(64px, 178px, 1px) scale(1.05); }
    80% { transform: translate3d(160px, 220px, 1px) scale(1.05); }
}
.tl-floor {
    position: absolute;
    left: 14%;
    right: 14%;
    bottom: -36px;
    height: 26px;
    border-radius: 50%;
    background: radial-gradient(ellipse at center, rgba(20, 24, 31, 0.16), rgba(20, 24, 31, 0) 70%);
    filter: blur(6px);
    animation: tl-floor 8s ease-in-out infinite;
}
@keyframes tl-floor {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(0.9); opacity: 0.75; }
}

/* Input type switch */
.stApp [data-testid="stRadio"] { margin-bottom: 0.25rem; }
.stApp [data-testid="stRadio"] label p { font-weight: 550; color: var(--tl-ink-2); }

/* Input card */
.stApp [data-testid="stForm"] {
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: var(--tl-shadow);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stApp [data-testid="stForm"]:focus-within {
    border-color: rgba(31, 58, 95, 0.55);
    box-shadow: var(--tl-shadow), 0 0 0 4px rgba(31, 58, 95, 0.07);
}
.stApp [data-testid="stWidgetLabel"] p {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--tl-ink-2);
}
.stApp .stTextArea textarea, .stApp .stTextInput input {
    border-radius: 6px;
    border: 1px solid var(--tl-line);
    background: #FCFCFA;
    color: var(--tl-ink);
    font-size: 1rem;
    transition: border-color 0.15s ease, box-shadow 0.15s ease, background 0.15s ease;
}
.stApp .stTextArea textarea:focus, .stApp .stTextInput input:focus {
    border-color: var(--tl-accent);
    background: #FFFFFF;
    box-shadow: 0 0 0 3px rgba(31, 58, 95, 0.12);
}

/* Buttons */
.stApp [data-testid="stFormSubmitButton"] > button {
    width: 100%;
    min-height: 3rem;
    background: var(--tl-accent);
    color: #FFFFFF;
    border: 1px solid var(--tl-accent);
    border-radius: 6px;
    font-weight: 600;
    letter-spacing: 0.01em;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), 0 2px 0 var(--tl-accent-hover);
    transition: background 0.15s ease, transform 0.1s ease, box-shadow 0.2s ease;
}
.stApp [data-testid="stFormSubmitButton"] > button p {
    display: inline-flex;
    align-items: center;
    color: #FFFFFF;
}
.stApp [data-testid="stFormSubmitButton"] > button p::after {
    content: "";
    width: 7px;
    height: 7px;
    margin-left: 10px;
    border-top: 2px solid currentColor;
    border-right: 2px solid currentColor;
    transform: rotate(45deg);
    transition: transform 0.2s var(--tl-ease);
}
.stApp [data-testid="stFormSubmitButton"] > button:hover {
    background: var(--tl-accent-hover);
    border-color: var(--tl-accent-hover);
    color: #FFFFFF;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.14), 0 2px 0 #0F2440, 0 8px 18px rgba(31, 58, 95, 0.25);
}
.stApp [data-testid="stFormSubmitButton"] > button:hover p::after { transform: translateX(4px) rotate(45deg); }
.stApp [data-testid="stFormSubmitButton"] > button:active { transform: translateY(2px); box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1); color: #FFFFFF; }
.stApp [data-testid="stFormSubmitButton"] > button:focus:not(:active) { color: #FFFFFF; border-color: var(--tl-accent-hover); }

/* Loading state: a page being read by a moving lens line */
.tl-loader {
    margin-top: 1.5rem;
    padding: 1.25rem 1.5rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    box-shadow: var(--tl-shadow);
}
.tl-loader-text { font-size: 0.92rem; font-weight: 600; color: var(--tl-ink-2); margin-bottom: 0.8rem; }
.tl-track { position: relative; height: 3px; background: #E6E3DA; border-radius: 2px; overflow: hidden; }
.tl-track i {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 34%;
    background: var(--tl-accent);
    border-radius: 2px;
    animation: tl-slide 1.15s ease-in-out infinite;
}
@keyframes tl-slide { from { left: -34%; } to { left: 100%; } }

/* Skeleton rows while related sources load */
.tl-skel {
    position: relative;
    height: 78px;
    margin-bottom: 0.65rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 10px;
    overflow: hidden;
}
.tl-skel::before, .tl-skel::after {
    content: "";
    position: absolute;
    left: 1.4rem;
    background: #ECEAE3;
    border-radius: 2px;
}
.tl-skel::before { top: 1.3rem; width: 52%; height: 11px; }
.tl-skel::after { top: 2.9rem; width: 28%; height: 8px; }
.tl-skel i {
    position: absolute;
    inset: 0;
    background: linear-gradient(100deg, transparent 30%, rgba(255, 255, 255, 0.85) 50%, transparent 70%);
    transform: translateX(-100%);
    animation: tl-shimmer 1.6s ease-in-out infinite;
}
@keyframes tl-shimmer { to { transform: translateX(100%); } }

/* Verdict */
.tl-verdict {
    position: relative;
    overflow: hidden;
    margin-top: 1.75rem;
    padding: 1.5rem 1.75rem 1.5rem 2rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    box-shadow: var(--tl-shadow);
    display: flex;
    align-items: center;
    gap: 1.25rem;
}
.tl-verdict::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; transform-origin: top; }
.tl-verdict.real::before { background: var(--tl-real); }
.tl-verdict.fake::before { background: var(--tl-fake); }
.tl-verdict.real { background: var(--tl-tint-real); border-color: var(--tl-tint-real-line); }
.tl-verdict.fake { background: var(--tl-tint-fake); border-color: var(--tl-tint-fake-line); }
/* One light pass across the card when the verdict lands */
.tl-verdict::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(105deg, transparent 38%, rgba(255, 255, 255, 0.75) 50%, transparent 62%);
    transform: translateX(-120%);
    pointer-events: none;
}

/* The badge is a coin: it spins into place on its vertical axis */
.tl-coin { flex: none; perspective: 420px; }
.tl-badge {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    border: 2px solid currentColor;
    position: relative;
    transform-style: preserve-3d;
    box-shadow: inset 0 -3px 6px rgba(20, 24, 31, 0.08), 0 3px 8px rgba(20, 24, 31, 0.1);
}
.tl-badge.real { color: var(--tl-real); background: rgba(23, 101, 63, 0.08); }
.tl-badge.real::after {
    content: "";
    position: absolute;
    left: 15px;
    top: 8px;
    width: 10px;
    height: 18px;
    border: solid currentColor;
    border-width: 0 3px 3px 0;
    transform: rotate(45deg);
}
.tl-badge.fake { color: var(--tl-fake); background: rgba(166, 40, 43, 0.08); }
.tl-badge.fake::before, .tl-badge.fake::after {
    content: "";
    position: absolute;
    left: 50%;
    top: 50%;
    width: 20px;
    height: 3px;
    margin: -1.5px 0 0 -10px;
    background: currentColor;
    border-radius: 1px;
}
.tl-badge.fake::before { transform: rotate(45deg); }
.tl-badge.fake::after { transform: rotate(-45deg); }
.tl-verdict-main { flex: 1; }
.tl-kicker {
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    color: var(--tl-ink-3);
    margin-bottom: 0.35rem;
}
.tl-verdict-label { font-size: 2rem; font-weight: 650; letter-spacing: -0.02em; line-height: 1.1; }
.tl-verdict.real .tl-verdict-label { color: var(--tl-real); }
.tl-verdict.fake .tl-verdict-label { color: var(--tl-fake); }
.tl-verdict-score { text-align: right; }
.tl-verdict-num {
    font-size: 2.6rem;
    font-weight: 650;
    letter-spacing: -0.03em;
    line-height: 1;
    font-variant-numeric: tabular-nums;
    color: var(--tl-ink);
}
.tl-verdict-cap { font-size: 0.82rem; color: var(--tl-ink-3); margin-top: 0.3rem; }

/* Count up numbers (shows the final value when animation is unavailable) */
.tl-count { --n: var(--t); counter-reset: num var(--n); display: inline-block; min-width: 1ch; }
.tl-count::after { content: counter(num) "%"; }

/* Probability split: bars have a little depth */
.tl-split {
    margin-top: 1rem;
    padding: 1.25rem 1.75rem 1.5rem 1.75rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
}
.tl-split-head { display: flex; justify-content: space-between; font-size: 0.92rem; color: var(--tl-ink-2); margin-bottom: 0.7rem; }
.tl-split-head span::before {
    content: "";
    display: inline-block;
    width: 8px;
    height: 8px;
    margin-right: 0.45rem;
    border-radius: 2px;
    vertical-align: 0.5px;
}
.tl-split-head span:first-child::before { background: var(--tl-fake); }
.tl-split-head span:last-child::before { background: var(--tl-real); }
.tl-split-head b { color: var(--tl-ink); font-variant-numeric: tabular-nums; }
.tl-split-track {
    display: flex;
    height: 12px;
    background: #ECEAE3;
    border-radius: 4px;
    overflow: hidden;
    gap: 2px;
    box-shadow: inset 0 1px 2px rgba(20, 24, 31, 0.12);
}
.tl-split-fake, .tl-split-real {
    height: 100%;
    width: var(--w);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.28), inset 0 -2px 0 rgba(0, 0, 0, 0.14);
}
.tl-split-fake { background: var(--tl-fake); }
.tl-split-real { background: var(--tl-real); }

/* Fact check and notes */
.tl-factcheck {
    margin-top: 1rem;
    padding: 1.2rem 1.75rem;
    background: var(--tl-tint-blue);
    border: 1px solid var(--tl-tint-blue-line);
    border-left: 4px solid var(--tl-accent);
    border-radius: 12px;
}
.tl-factcheck p { margin: 0.2rem 0 0.6rem 0; line-height: 1.6; color: var(--tl-ink); }
.tl-factcheck a { color: var(--tl-accent); font-weight: 600; text-decoration: none; border-bottom: 1px solid rgba(31, 58, 95, 0.35); }
.tl-factcheck a:hover { border-bottom-color: var(--tl-accent); }
.tl-note {
    margin-top: 1rem;
    padding: 0.9rem 1.2rem;
    background: var(--tl-caution-bg);
    border: 1px solid var(--tl-caution-line);
    border-radius: 8px;
    font-size: 0.92rem;
    line-height: 1.55;
    color: var(--tl-ink);
}

/* Section heading */
.tl-section { margin: 2.25rem 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }
.tl-section span {
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--tl-accent);
    white-space: nowrap;
}
.tl-section::after { content: ""; flex: 1; height: 1px; background: var(--tl-line); }

/* Related sources: cards tilt toward the cursor in perspective */
.tl-article-link { display: block; text-decoration: none !important; color: inherit !important; perspective: 900px; }
.tl-article {
    position: relative;
    margin-bottom: 0.65rem;
    padding: 1rem 3rem 1rem 1.4rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 10px;
    transform-origin: 50% 100%;
    transition: border-color 0.2s ease, transform 0.25s var(--tl-ease), box-shadow 0.25s ease;
}
.tl-article::after {
    content: "";
    position: absolute;
    right: 1.4rem;
    top: 50%;
    width: 7px;
    height: 7px;
    border-top: 2px solid var(--tl-ink-3);
    border-right: 2px solid var(--tl-ink-3);
    transform: translateY(-50%) rotate(45deg);
    transition: border-color 0.18s ease, right 0.18s ease;
}
.tl-article-link:hover .tl-article {
    border-color: #C9C6BB;
    transform: rotateX(3deg) translateY(-3px);
    box-shadow: 0 2px 4px rgba(20, 24, 31, 0.05), 0 14px 26px rgba(20, 24, 31, 0.08);
}
.tl-article-link:hover .tl-article::after { border-color: var(--tl-accent); right: 1.1rem; }
.tl-article-title { font-weight: 600; line-height: 1.4; color: var(--tl-ink); }
.tl-article-meta { margin-top: 0.3rem; font-size: 0.85rem; color: var(--tl-ink-3); }
.tl-rate { display: inline-flex; align-items: center; gap: 0.4rem; }
.tl-rate::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: var(--tl-ink-3); }
.tl-rate.hi::before { background: var(--tl-sage); }
.tl-rate.mid::before { background: var(--tl-ochre); }
.tl-rate.lo::before { background: var(--tl-fake); }
.tl-article-sep { margin: 0 0.45rem; }
.tl-article-url { display: block; margin-top: 0.2rem; font-size: 0.8rem; color: var(--tl-ink-3); word-break: break-all; }

.tl-disclaimer { margin-top: 1.75rem; font-size: 0.85rem; line-height: 1.6; color: var(--tl-ink-3); }

/* How it works: a sequence, so the numbering is real. Cards sit in perspective. */
.tl-steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.1rem; margin-top: 2.5rem; perspective: 1100px; }
.tl-step {
    padding: 1.3rem 1.4rem 1.5rem 1.4rem;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid var(--tl-line);
    border-top: 3px solid var(--c, var(--tl-slate));
    border-radius: 12px;
    transform-origin: 50% 100%;
    transition: transform 0.3s var(--tl-ease), border-color 0.2s ease, box-shadow 0.3s ease, background 0.2s ease;
}
.tl-step:hover {
    transform: rotateX(4deg) translateY(-4px);
    border-color: #C9C6BB;
    background: #FFFFFF;
    box-shadow: 0 2px 4px rgba(20, 24, 31, 0.04), 0 16px 30px rgba(20, 24, 31, 0.08);
}
.tl-step:nth-child(1) { --c: var(--tl-slate); }
.tl-step:nth-child(2) { --c: var(--tl-ochre); }
.tl-step:nth-child(3) { --c: var(--tl-sage); }
.tl-step-num {
    font-size: 2.3rem;
    font-weight: 300;
    line-height: 1;
    letter-spacing: -0.03em;
    color: var(--c, var(--tl-slate));
    opacity: 0.55;
    font-variant-numeric: tabular-nums;
    transition: opacity 0.2s ease;
}
.tl-step:hover .tl-step-num { opacity: 1; }
.tl-step-title { margin: 0.9rem 0 0.35rem 0; font-weight: 650; color: var(--tl-ink); }
.tl-step-text { font-size: 0.92rem; line-height: 1.6; color: var(--tl-ink-2); margin: 0; }

/* Sections added for navigation */
.tl-block { margin-top: 3.5rem; }
.tl-block h2 {
    font-size: 1.5rem; font-weight: 650; letter-spacing: -0.02em; margin: 0 0 0.6rem 0;
    color: var(--tl-ink); padding: 0;
}
.tl-block p { color: var(--tl-ink-2); line-height: 1.65; margin: 0; max-width: 40rem; }

/* Features: each card has a quiet top rule that draws in on hover */
.tl-feat-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1.2rem; }
.tl-feat {
    position: relative;
    overflow: hidden;
    padding: 1.2rem 1.4rem 1.3rem;
    background: rgba(255, 255, 255, 0.72);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    transition: transform 0.3s var(--tl-ease), border-color 0.2s ease, box-shadow 0.3s ease, background 0.2s ease;
}
.tl-feat::before {
    content: "";
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    height: 3px;
    background: var(--c, var(--tl-slate));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s var(--tl-ease);
}
.tl-feat:nth-child(1) { --c: var(--tl-slate); }
.tl-feat:nth-child(2) { --c: var(--tl-ochre); }
.tl-feat:nth-child(3) { --c: var(--tl-sage); }
.tl-feat:nth-child(4) { --c: var(--tl-accent); }
.tl-feat:hover {
    transform: translateY(-3px);
    background: #FFFFFF;
    border-color: #D3D0C5;
    box-shadow: 0 2px 4px rgba(20, 24, 31, 0.04), 0 14px 26px rgba(20, 24, 31, 0.07);
}
.tl-feat:hover::before { transform: scaleX(1); }
.tl-feat b { display: block; color: var(--tl-ink); margin-bottom: 0.3rem; font-weight: 650; }
.tl-feat span { font-size: 0.92rem; line-height: 1.6; color: var(--tl-ink-2); }

/* About */
.tl-about-grid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: 2.25rem; align-items: start; margin-top: 0.4rem; }
.tl-about-text p + p { margin-top: 0.95rem; }
.tl-glance {
    padding: 1.2rem 1.4rem;
    background: var(--tl-surface);
    border: 1px solid var(--tl-line);
    border-radius: 12px;
    box-shadow: var(--tl-shadow);
}
.tl-glance-title { font-size: 0.88rem; font-weight: 600; color: var(--tl-accent); margin-bottom: 0.4rem; }
.tl-glance-row { padding: 0.7rem 0; border-top: 1px solid var(--tl-line); }
.tl-glance-row:first-of-type { border-top: 0; }
.tl-glance-row span { display: block; font-size: 0.78rem; color: var(--tl-ink-3); margin-bottom: 0.15rem; }
.tl-glance-row b { font-size: 0.93rem; font-weight: 600; color: var(--tl-ink); line-height: 1.45; }

/* FAQ */
.tl-faq details { border-bottom: 1px solid var(--tl-line); padding: 0; }
.tl-faq details:first-of-type { border-top: 1px solid var(--tl-line); margin-top: 1rem; }
.tl-faq summary {
    cursor: pointer; font-weight: 600; color: var(--tl-ink); list-style: none;
    display: flex; align-items: center; justify-content: space-between; gap: 1rem;
    padding: 1rem 0; transition: color 0.15s ease;
}
.tl-faq summary::-webkit-details-marker { display: none; }
.tl-faq summary::after {
    content: ""; flex: none; width: 8px; height: 8px;
    border-right: 2px solid var(--tl-ink-3); border-bottom: 2px solid var(--tl-ink-3);
    transform: rotate(45deg) translate(-2px, -2px);
    transition: transform 0.25s var(--tl-ease), border-color 0.15s ease;
}
.tl-faq summary:hover, .tl-faq details[open] summary { color: var(--tl-accent); }
.tl-faq details[open] summary::after { transform: rotate(-135deg) translate(-2px, -2px); border-color: var(--tl-accent); }
.tl-faq details p { margin: 0 0 1.1rem 0; }

/* Footer: a dark rounded panel. The container key adds the st-key-tl_footer class. */
.st-key-tl_footer {
    position: relative;
    margin-top: 4rem;
    padding: 2.5rem 2.5rem 1.5rem;
    gap: 0.5rem;
    background-color: var(--tl-dark);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='26' height='26'><circle cx='1.2' cy='1.2' r='1.2' fill='%23FFFFFF' fill-opacity='0.045'/></svg>");
    border-radius: 22px;
    box-shadow: 0 24px 48px rgba(17, 28, 43, 0.2);
}
.tl-footer { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr); gap: 2.5rem; }
.tl-footer .tl-brand { color: #FFFFFF; margin-bottom: 0.8rem; }
.tl-footer .tl-brand-mark { border-color: #A9BDD8; }
.tl-footer .tl-brand-mark::after { background: #A9BDD8; }
.tl-footer-tag { font-weight: 600; color: #D9B25E; font-size: 0.95rem; margin: 0 0 0.5rem 0; }
.tl-footer-desc { font-size: 0.9rem; line-height: 1.65; color: rgba(255, 255, 255, 0.62); margin: 0; max-width: 28rem; }
.tl-footer-cta {
    display: inline-block; margin-top: 1.3rem; padding: 0.6rem 1.1rem;
    background: #F6F5F1; color: var(--tl-ink) !important; font-size: 0.9rem; font-weight: 600;
    border-radius: 10px; text-decoration: none !important;
    transition: transform 0.2s var(--tl-ease), background 0.15s ease, box-shadow 0.2s ease;
}
.tl-footer-cta:hover { background: #FFFFFF; transform: translateY(-2px); box-shadow: 0 8px 18px rgba(0, 0, 0, 0.25); }
.tl-footer-head { font-size: 0.82rem; font-weight: 600; color: rgba(255, 255, 255, 0.45); margin-bottom: 0.8rem; }
.tl-footer-links { display: flex; flex-direction: column; gap: 0.55rem; }
.tl-footer-links a { font-size: 0.92rem; color: rgba(255, 255, 255, 0.78) !important; text-decoration: none !important; width: fit-content; transition: color 0.15s ease, transform 0.2s var(--tl-ease); }
.tl-footer-links a:hover { color: #FFFFFF !important; transform: translateX(3px); }
.tl-footer-rule { height: 1px; background: rgba(255, 255, 255, 0.1); margin: 1.2rem 0 0.4rem; }
.tl-footer-note { font-size: 0.85rem; color: rgba(255, 255, 255, 0.5); text-align: right; padding-top: 0.45rem; }
.stApp .st-key-tl_footer [data-testid="stPageLink-NavLink"] { padding-left: 0; background: transparent; }
.stApp .st-key-tl_footer [data-testid="stPageLink-NavLink"] p { font-size: 0.88rem; color: rgba(255, 255, 255, 0.72); }
.stApp .st-key-tl_footer [data-testid="stPageLink-NavLink"]:hover { background: transparent; }
.stApp .st-key-tl_footer [data-testid="stPageLink-NavLink"]:hover p { color: #FFFFFF; }

/* Legal pages */
.stApp h1 { font-weight: 650; letter-spacing: -0.02em; }
.stApp h3 { font-weight: 650; letter-spacing: -0.01em; margin-top: 1.5rem; }
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li { line-height: 1.7; }

@media (max-width: 800px) {
    .tl-hero-grid { grid-template-columns: 1fr; gap: 1.5rem; }
    .tl-visual { display: none; }
    .tl-steps { grid-template-columns: 1fr; }
    .tl-verdict { flex-wrap: wrap; }
    .tl-verdict-score { text-align: left; width: 100%; }
    .tl-verdict-label { font-size: 1.7rem; }
    .tl-nav { top: 8px; width: calc(100% - 1.25rem); border-radius: 16px; }
    .tl-nav-links { display: none; }
    .tl-menu { display: block; }
    .tl-nav-inner { gap: 0.6rem; padding: 0 0.55rem 0 1rem; }
    .tl-feat-grid, .tl-about-grid, .tl-footer { grid-template-columns: 1fr; }
    .tl-about-grid { gap: 1.5rem; }
    .st-key-tl_footer { padding: 1.75rem 1.4rem 1.2rem; border-radius: 18px; }
    .tl-footer { gap: 1.75rem; }
    .tl-footer-note { text-align: left; }
}

@media (prefers-reduced-motion: reduce) {
    .tl-intro, .tl-ul::after, .tl-float, .tl-stage, .tl-lens, .tl-lens-shadow,
    .tl-floor, .tl-l.m::after, .tl-track i, .tl-skel i { animation: none !important; }
    .tl-stage { transform: rotateX(7deg) rotateY(-12deg); }
    .tl-lens { transform: translate3d(100px, 70px, 64px); }
    .tl-lens-shadow { transform: translate3d(120px, 98px, 1px); }
    .tl-l.m::after { opacity: 1; }
    .tl-article, .tl-article::after, .tl-step, .tl-feat, .tl-feat::before,
    .tl-footer-cta, .tl-footer-links a, .tl-faq summary::after { transition: none !important; }
    html, [data-testid="stMain"] { scroll-behavior: auto; }
}
"""

# Result animations come in two identical sets (a and b). The app alternates
# between them on every analysis so the animations replay on repeat runs.
_VARIANT_CSS = """
@keyframes tl-rise-__V__ { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: none; } }
@keyframes tl-settle-__V__ {
    from { opacity: 0; transform: perspective(1000px) rotateX(9deg) translateY(18px); }
    to { opacity: 1; transform: perspective(1000px) rotateX(0) translateY(0); }
}
@keyframes tl-coin-__V__ {
    0% { opacity: 0; transform: rotateY(-540deg) scale(0.7); }
    25% { opacity: 1; }
    100% { opacity: 1; transform: rotateY(0) scale(1); }
}
@keyframes tl-bar-__V__ { from { transform: scaleY(0); } to { transform: scaleY(1); } }
@keyframes tl-grow-__V__ { from { width: 0; } }
@keyframes tl-count-__V__ { from { --n: 0; } }
@keyframes tl-sheen-__V__ { from { transform: translateX(-120%); } to { transform: translateX(120%); } }
.v-__V__ { animation: tl-rise-__V__ 0.6s var(--tl-ease) both; animation-delay: var(--d, 0s); }
.v-__V__ .tl-verdict { animation: tl-settle-__V__ 0.8s var(--tl-ease) both; }
.v-__V__ .tl-verdict::before { animation: tl-bar-__V__ 0.7s var(--tl-ease) 0.2s both; }
.v-__V__ .tl-verdict::after { animation: tl-sheen-__V__ 1.1s ease-in-out 0.9s both; }
.v-__V__ .tl-badge { animation: tl-coin-__V__ 1.1s var(--tl-ease) 0.25s both; }
.v-__V__ .tl-split-fake, .v-__V__ .tl-split-real { animation: tl-grow-__V__ 1s var(--tl-ease) 0.35s both; }
.v-__V__ .tl-count { animation: tl-count-__V__ 1.2s var(--tl-ease) 0.25s both; }
@media (prefers-reduced-motion: reduce) {
    .v-__V__, .v-__V__ .tl-verdict, .v-__V__ .tl-verdict::before, .v-__V__ .tl-verdict::after,
    .v-__V__ .tl-badge, .v-__V__ .tl-split-fake, .v-__V__ .tl-split-real,
    .v-__V__ .tl-count { animation: none !important; }
}
"""

TRUTHLENS_CSS = (
    "<style>"
    + _BASE_CSS
    + _VARIANT_CSS.replace("__V__", "a")
    + _VARIANT_CSS.replace("__V__", "b")
    + "</style>"
)