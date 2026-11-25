from .checks.brand import check_brand_misuse
from .checks.lexical import (
    check_hyphens, check_ip_host, check_keywords, check_length,
    check_no_https, check_punycode, check_subdomain_depth, check_tld,
    check_userinfo,
)
from .checks.typosquat import check_typosquat
from .models import Finding, Result
from .parsing import parse_url

CHECKS = [
    check_ip_host, check_userinfo, check_subdomain_depth, check_length,
    check_punycode, check_hyphens, check_tld, check_no_https, check_keywords,
    check_brand_misuse, check_typosquat,
]

BRAND_CHECKS = {"brand_misuse", "brand_lookalike", "typosquat"}


def level_for(score: int) -> str:
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


def score_url(url: str) -> Result:
    parsed = parse_url(url)
    findings = []
    for check in CHECKS:
        try:
            findings.extend(check(parsed))
        except Exception:
            continue  # one broken check should never crash the tool

    # Combination signal: impersonating a brand AND sounding urgent is worse than either alone
    names = {f.check for f in findings}
    if names & BRAND_CHECKS and "keywords" in names:
        findings.append(Finding("combo", 20, "Brand impersonation combined with urgent wording"))

    findings.sort(key=lambda f: f.points, reverse=True)
    total = min(100, sum(f.points for f in findings))
    return Result(url=url, score=total, level=level_for(total), findings=findings)