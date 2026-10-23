import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from site_config import EFFECTIVE_DATE, FAVICON_PATH, OPERATOR_NAME, contact_line
from truthlens_styles import NAV_HTML, TRUTHLENS_CSS

st.set_page_config(
    page_title="Privacy Policy | TruthLens",
    page_icon=FAVICON_PATH,
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(TRUTHLENS_CSS, unsafe_allow_html=True)
st.markdown(NAV_HTML, unsafe_allow_html=True)

st.page_link("app.py", label="Back to TruthLens")

st.title("Privacy Policy")
st.caption(f"Effective {EFFECTIVE_DATE}")

st.markdown(
    f"""
This policy explains what {OPERATOR_NAME} ("we", "us") does with the information you
give it when you use this website.

### What you submit

You can paste the text of a news article or enter a link to one. We use that text, or
the text we extract from the link, only to produce your result: a prediction from a
machine learning model, a search for related coverage, and a fact check lookup where
one is available.

### Accounts and personal details

You do not need an account to use the site, and we do not ask for your name, email
address or any other personal details in order to analyze an article. Please do not
paste private or sensitive personal information into the text box.

### Third party services

To find related coverage and fact checks, parts of the article text or its key terms
may be sent to external news search and fact checking services. If you enter a link,
our server fetches that page from the publisher's website. These services have their
own privacy practices, which we do not control.

### Hosting and logs

Like most websites, the hosting provider and web server may automatically record
technical information such as IP address, browser type, and the time and URL of each
request. This is used to keep the service running and secure.

### Cookies

We do not use advertising or tracking cookies. The framework that runs this site may
use a session identifier so the page can work while you are using it.

### Retention

We do not build user profiles. Any article text you submit is used to produce your
result and is not intended to be kept beyond what is needed to run the service and
what the hosting provider logs as described above.

### Children

This site is not directed at children under 13, and we do not knowingly collect
personal information from them.

### Your rights

Depending on where you live, you may have the right to ask what information we hold
about you, and to ask us to correct or delete it. {contact_line()}

### Changes to this policy

If we change this policy we will update the effective date at the top of this page.
"""
)