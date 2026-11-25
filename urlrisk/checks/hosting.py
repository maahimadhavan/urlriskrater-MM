import re

from ..models import Finding, ParsedURL

# Free platforms where anyone can publish a page under a subdomain
FREE_HOSTS = {
    "pages.dev", "vercel.app", "netlify.app", "webflow.io", "weebly.com",
    "blogspot.com", "github.io", "workers.dev", "web.app", "firebaseapp.com",
    "glitch.me", "wixsite.com", "000webhostapp.com", "godaddysites.com",
}

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy",
    "urlz.li", "shorturl.at", "tiny.cc", "ow.ly",
}


def check_free_hosting(u: ParsedURL):
    if u.registered in FREE_HOSTS and u.subdomain:
        return [Finding("free_hosting", 12,
                        f"Hosted on a free page-builder platform ({u.registered}) often used in scams")]
    return []


def check_shortener(u: ParsedURL):
    if u.registered in SHORTENERS:
        return [Finding("shortener", 15, "Shortened link hides the real destination")]
    return []


def check_random_subdomain(u: ParsedURL):
    """Machine-generated names like 'zq1jc-f2z-xy8u-4rehc-30-09-2026-aa'."""
    if not u.subdomain:
        return []
    label = u.subdomain.split(".")[-1]  # the label next to the registered domain
    digits = sum(c.isdigit() for c in label)
    letters = sum(c.isalpha() for c in label)
    has_date = re.search(r"\d{1,2}-\d{1,2}-\d{4}", label) is not None
    mixed = digits >= 2 and letters >= 3 and len(label) >= 8
    if has_date or mixed:
        return [Finding("random_subdomain", 10,
                        f"Machine-generated looking subdomain ('{label[:30]}')")]
    return []