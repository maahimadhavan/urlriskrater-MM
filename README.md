# URL Risk Rater

A human interpretable service which scores links on a 0-100 scale. Designed to educate non-experts how to recognise phishing and scam websites.

## Why I made it

Phishing is a major method of scamming. Current services usually only report whether a website is safe or not. My service also explains its decision, to further educate users on how to recognise a risky site.

## Example

```

$ python cli.py "http://paypa1-secure.login-verify.xyz/update"

Risk: 73/100 (HIGH)
+30  'paypa1' imitates the brand 'paypal' using lookalike characters
+20  Brand impersonation combined with urgent wording
+10  Urgent/official-sounding words: secure, update
+8   Uses a TLD often abused in scams (.xyz)
+5   Does not use HTTPS
```

## How it works

Sites go through various automated rules which give a site a score, along with a human understandable explanation.

Rules include:

**Lexical** – incorrect IP, @ abuse, too many subdomains, lengthy URLs, punycode, hyphenated URLs, unusual TLDs and absence of HTTPS
**Brand impersonation** – inappropriately placed brand words and similar symbols (eg paypa1)
**Typosquatting** - comparing edit distance with a list of well known websites
**Combined rule** - brand impersonation applied with high pressure language increases risk more than both rules in isolation.

## Execute
```

pip install -r requirements.txt
python cli.py "https://example.com"
python -m pytest
```

## Constraints

- Whilst customisable, there is a chance that genuine sites may be reported as risky e.g. local sites which are similar in name to well-known sites.
- Offenders will also evolve methods so this service should therefore act as preliminary protection.

## Future development

- Investigating domain age (via RDAP)
- Following redirects and analysing TLS
- Comparing performance on PhishTank/URLhaus with Tranco data
- Training logistic regression model to determine optimal rule weighting.