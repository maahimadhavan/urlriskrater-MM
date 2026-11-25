import argparse
import json
from dataclasses import asdict

from urlrisk.scorer import score_url


def show(url, as_json=False):
    r = score_url(url)
    if as_json:
        print(json.dumps(asdict(r), indent=2))
        return
    print(f"\nRisk: {r.score}/100 ({r.level})")
    if not r.findings:
        print("  No red flags found")
    for f in r.findings:
        print(f"  +{f.points:<3} {f.reason}")
    print()


def interactive():
    print("URL Risk Rater. Paste a URL and press Enter (type q to quit).\n")
    while True:
        try:
            url = input("URL> ").strip().strip("'\"")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if url.lower() in {"q", "quit", "exit"}:
            break
        if url:
            show(url)


def main():
    ap = argparse.ArgumentParser(description="Rate the risk of a URL from 0 to 100")
    ap.add_argument("urls", nargs="*", help="URLs to check (optional)")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    if args.urls:
        for url in args.urls:
            print(f"\n{url}", end="")
            show(url, args.json)
    else:
        interactive()


if __name__ == "__main__":
    main()