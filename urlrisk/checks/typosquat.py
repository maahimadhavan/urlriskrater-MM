import re
from pathlib import Path

from ..models import Finding, ParsedURL
from ..textutils import decode_idna, levenshtein, normalize

DATA = Path(__file__).resolve().parents[2] / "data" / "top_domains.txt"


def _load():
    domains = []
    if DATA.exists():
        for line in DATA.read_text().splitlines():
            line = line.strip().lower()
            if not line or line.startswith("#"):
                continue
            domains.append(line.split(",")[-1])  # supports Tranco "rank,domain" rows
    return domains


TOP = _load()
TOP_SET = set(TOP)


def _has_digit(s: str) -> bool:
    return any(c.isdigit() for c in s)


def check_typosquat(u: ParsedURL):
    reg = u.registered
    if reg in TOP_SET or len(u.domain) < 5:
        return []

    cand = normalize(decode_idna(reg))
    best = None  # (distance, top_domain)

    for top in TOP:
        if len(top) < 6 or abs(len(top) - len(cand)) > 2:
            continue

        # Same brand on a different country domain (google.iq, zalando.at) is legitimate
        if top.split(".")[0] == u.domain and len(u.suffix.split(".")[-1]) == 2:
            continue

        # Numbered hosts (awsdns-39 vs awsdns-09) differ only by their digits
        if _has_digit(reg) and _has_digit(top) and re.sub(r"\d", "", reg) == re.sub(r"\d", "", top):
            continue

        d = levenshtein(cand, top)
        if best is None or d < best[0]:
            best = (d, top)

    if best is None:
        return []

    d, top = best
    if d == 0:
        return [Finding("typosquat", 35,
                        f"Lookalike characters imitate '{top}'")]
    limit = 1 if len(top) < 9 else 2
    if d <= limit:
        pts = 30 if d == 1 else 20
        return [Finding("typosquat", pts,
                        f"Within {d} character edit of popular site '{top}'")]
    return []