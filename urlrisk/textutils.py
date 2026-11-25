import re

# Characters attackers swap in to imitate real letters
CONFUSABLES = {
    "0": "o", "1": "l", "3": "e", "5": "s", "$": "s",
    # common Cyrillic lookalikes (for homograph attacks)
    "а": "a", "е": "e", "о": "o", "р": "p", "с": "c", "х": "x", "у": "y",
}
MULTI = [("rn", "m"), ("vv", "w")]


def decode_idna(s: str) -> str:
    """Turn punycode (xn--...) into real Unicode so lookalikes become visible."""
    try:
        return s.encode("ascii").decode("idna")
    except Exception:
        return s


def normalize(s: str) -> str:
    s = s.lower()
    for a, b in MULTI:
        s = s.replace(a, b)
    return "".join(CONFUSABLES.get(c, c) for c in s)


def tokens(s: str) -> list:
    return [t for t in re.split(r"[^a-z0-9]+", s.lower()) if t]


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]