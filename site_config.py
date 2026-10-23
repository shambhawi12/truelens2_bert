"""Shared site settings. Fill in the two values below before you publish.

They appear on the Privacy Policy and Terms pages.
"""
from pathlib import Path

# Set these to your real details.
OPERATOR_NAME = "TruthLens"
CONTACT_EMAIL = ""  # e.g. "contact@yourdomain.com"
GOVERNING_LAW = "India"

EFFECTIVE_DATE = "October 23, 2026"

FAVICON_PATH = str(Path(__file__).resolve().parent / "assets" / "favicon.png")


def contact_line() -> str:
    if CONTACT_EMAIL.strip():
        return f"You can contact us at {CONTACT_EMAIL.strip()}."
    return "Contact details are available from the site operator."