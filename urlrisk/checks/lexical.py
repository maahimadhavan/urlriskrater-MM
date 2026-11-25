import ipaddress

from ..brands import KEYWORDS, SUSPICIOUS_TLDS
from ..models import Finding, ParsedURL
from ..textutils import tokens


def check_ip_host(u: ParsedURL):
    try:
        ipaddress.ip_address(u.host)
    except ValueError:
        return []
    return [Finding("ip_host", 30, "Uses a raw IP address instead of a domain name")]


def check_userinfo(u: ParsedURL):
    if u.has_userinfo:
        return [Finding("userinfo", 30, "Contains '@' which can disguise the real destination")]
    return []


def check_subdomain_depth(u: ParsedURL):
    depth = len(u.subdomain.split(".")) if u.subdomain else 0
    if depth > 3:
        return [Finding("subdomains", 15, f"Excessive subdomains ({depth} levels)")]
    return []


def check_length(u: ParsedURL):
    n = len(u.raw)
    if n > 120:
        return [Finding("length", 12, f"Very long URL ({n} characters)")]
    if n > 75:
        return [Finding("length", 6, f"Long URL ({n} characters)")]
    return []


def check_punycode(u: ParsedURL):
    if "xn--" in u.host:
        return [Finding("punycode", 20, "Uses punycode (possible lookalike-character attack)")]
    return []


def check_hyphens(u: ParsedURL):
    if u.domain.count("-") >= 2:
        return [Finding("hyphens", 10, "Domain name contains multiple hyphens")]
    return []


def check_tld(u: ParsedURL):
    tld = u.suffix.split(".")[-1]
    if tld in SUSPICIOUS_TLDS:
        return [Finding("tld", 8, f"Uses a TLD often abused in scams (.{tld})")]
    return []


def check_no_https(u: ParsedURL):
    if u.scheme == "http":
        return [Finding("no_https", 5, "Does not use HTTPS")]
    return []


def check_keywords(u: ParsedURL):
    # Look in the subdomain and path only. 'secure' in a registered name is less telling.
    found = sorted(set(tokens(u.subdomain + " " + u.path)) & KEYWORDS)
    if not found:
        return []
    pts = min(15, 5 * len(found))
    return [Finding("keywords", pts, f"Urgent/official-sounding words: {', '.join(found)}")]