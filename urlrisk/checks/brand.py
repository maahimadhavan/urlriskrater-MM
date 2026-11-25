from ..brands import BRANDS
from ..models import Finding, ParsedURL
from ..textutils import normalize, tokens


def check_brand_misuse(u: ParsedURL):
    """Brand name appears in the URL, but the real registered domain isn't that brand."""
    findings = []
    host_tokens = tokens(u.subdomain + " " + u.domain)
    path_tokens = tokens(u.path)

    for t in host_tokens + path_tokens:
        # Registered domain exactly equal to the brand is fine (paypal.com)
        if t == u.domain:
            continue
        if t in BRANDS:
            findings.append(Finding(
                "brand_misuse", 30,
                f"Mentions '{t}' but the real domain is '{u.registered}'"))
            break

    # Lookalike spellings in the subdomain/path, e.g. paypa1-secure.something.xyz
    for t in tokens(u.subdomain) + path_tokens:
        if t not in BRANDS and normalize(t) in BRANDS:
            findings.append(Finding(
                "brand_lookalike", 30,
                f"'{t}' imitates the brand '{normalize(t)}' using lookalike characters"))
            break

    return findings