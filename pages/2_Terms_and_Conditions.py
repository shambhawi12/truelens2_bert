import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from site_config import EFFECTIVE_DATE, FAVICON_PATH, GOVERNING_LAW, OPERATOR_NAME, contact_line
from truthlens_styles import NAV_HTML, TRUTHLENS_CSS

st.set_page_config(
    page_title="Terms and Conditions | TruthLens",
    page_icon=FAVICON_PATH,
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown(TRUTHLENS_CSS, unsafe_allow_html=True)
st.markdown(NAV_HTML, unsafe_allow_html=True)

st.page_link("app.py", label="Back to TruthLens")

st.title("Terms and Conditions")
st.caption(f"Effective {EFFECTIVE_DATE}")

st.markdown(
    f"""
By using this website you agree to these terms. If you do not agree, please do not
use the site.

### What the service does

{OPERATOR_NAME} uses a machine learning model to estimate whether a news article is
likely to be real or fake, and shows related coverage and fact checks where available.

### Results can be wrong

The model makes mistakes. A result is an estimate, not a finding of fact, and it is
not legal, financial, medical or professional advice. Always check important claims
against reliable sources before you share or act on them. We do not guarantee that any
result is accurate, complete or current.

### Acceptable use

You agree not to:

* use the service for anything unlawful or to harass or defame others;
* submit content you do not have the right to use;
* attempt to disrupt, overload or gain unauthorized access to the service;
* use automated tools to send large volumes of requests without our permission.

### Third party content and links

Related articles and fact checks come from third parties. We do not control or endorse
their content and are not responsible for it. Source ratings shown beside related
articles are informational only.

### Intellectual property

The site design, code and branding belong to {OPERATOR_NAME} or its licensors.
Articles you submit and articles linked from results remain the property of their
respective owners.

### Availability

The service is provided as is and as available. We may change, suspend or stop it at
any time.

### Limitation of liability

To the fullest extent permitted by law, {OPERATOR_NAME} is not liable for any loss or
damage arising from your use of the service or from reliance on its results.

### Governing law

These terms are governed by the laws of {GOVERNING_LAW}.

### Changes to these terms

We may update these terms from time to time. The effective date above shows when they
were last changed. Continued use of the site after a change means you accept the
updated terms.

### Contact

{contact_line()}
"""
)