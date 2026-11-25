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

## Results

I tested the tool on 300 real phishing URLs from the OpenPhish feed (downloaded November 24, 2026) and 300 legitimate URLs from the Tranco top-sites list. The legitimate URLs came from ranks 10,001-20,000, kept separate from the top 10,000 used for the typosquatting check so the test wasn't rigged.

| Score threshold | Recall (phishing caught) | False positive rate | Precision |
|---|---|---|---|
| 10 | 84.3% | 5.7% | 93.7% |
| 20 | 69.7% | 5.3% | 92.9% |
| 30 | 3.7% | 0.0% | 100% |

I chose 20 as the "warn the user" threshold because a missed scam usually costs more than an extra warning.

## What went wrong, and how I fixed it

**Attempt 1: recall was 3.3%.** My first version caught only 10 of 300 phishing URLs. Looking at the missed ones, I saw the pattern: almost all were hosted on free platforms like `pages.dev`, `netlify.app`, and `webflow.io`. The domains looked ordinary, so the checks I'd written (typos, keywords, IP addresses) had nothing to catch.

**Fix: I added two checks.** One flags free page-builder platforms, and another flags machine-generated names like `zq1jc-f2z-xy8u-4rehc-30-09-2026-aa`. Recall rose from 3.3% to 69.7%.

**A second problem: false positives.** The typosquatting check flagged real sites such as `google.iq` and `zalando.at`, which are legitimate country versions of a brand. I added rules to exempt same-brand country domains and numbered server names. False positives on that check dropped to zero.

**A third problem: my own test was misleading.** The "no HTTPS" check fired on 45% of phishing URLs and 0% of legitimate ones. That wasn't because it was a good signal. I had built the legitimate list with `https://` on every URL. I fixed the benchmark so every URL gets the same scheme.

**The big lesson:** a single signal rarely crosses the warning threshold on its own. My checks were each worth 5-15 points, but the cutoff was 30, so the tool looked broken even when it was detecting things correctly. Tuning how signals combine mattered as much as writing the checks.

## Limitations (what I'd be honest about)

- **The tuning data and the test data overlap.** I added checks after looking at which phishing URLs I'd missed, so 69.7% is likely optimistic. The real test is a fresh feed of URLs I haven't seen.
- **The legitimate set is too easy.** Top-ranked sites rarely use free hosting. A real small business on `netlify.app` would trigger my free-hosting check, so the false positive rate on everyday sites is probably higher than 5%.
- **Hard cases still slip through.** URLs like `qa-amex.ourvacationcenter.com` have a clean-looking domain with a brand name in an unrelated place. Catching those needs signals the tool doesn't have yet.
- **Attackers adapt.** This is a first line of defense, not a guarantee.

## Roadmap

- Domain age lookup (RDAP), since most phishing domains are days old
- Retest on a fresh phishing feed to measure real generalization
- Add legitimate free-hosted sites to the test set
- Learn the check weights from data using logistic regression