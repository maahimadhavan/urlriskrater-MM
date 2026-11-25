from urllib.parse import urlparse

import tldextract

from .models import ParsedURL

# suffix_list_urls=() uses the bundled suffix list, so no network is needed
_extract = tldextract.TLDExtract(suffix_list_urls=())


def parse_url(raw: str) -> ParsedURL:
    raw = raw.strip()
    to_parse = raw if "://" in raw else "http://" + raw
    p = urlparse(to_parse)
    host = (p.hostname or "").lower()
    ext = _extract(host)
    return ParsedURL(
        raw=raw,
        scheme=p.scheme.lower(),
        host=host,
        subdomain=ext.subdomain,
        domain=ext.domain,
        suffix=ext.suffix,
        path=p.path.lower(),
        query=p.query.lower(),
        has_userinfo=p.username is not None,
    )