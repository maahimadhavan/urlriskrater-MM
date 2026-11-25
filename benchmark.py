import argparse
import random
from collections import Counter

from urlrisk.scorer import score_url


def load(path, limit):
    with open(path, encoding="utf-8", errors="ignore") as f:
        urls = [l.strip() for l in f if l.strip() and not l.startswith("#")]
    random.seed(42)  # same sample every run, so results are reproducible
    random.shuffle(urls)
    urls = ["https://" + u.split("://", 1)[-1] for u in urls]
    return urls[:limit]


def evaluate(bad, good, threshold):
    tp = sum(1 for _, r in bad if r.score >= threshold)
    fn = len(bad) - tp
    fp = sum(1 for _, r in good if r.score >= threshold)
    tn = len(good) - fp
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    fpr = fp / (fp + tn) if fp + tn else 0
    print(f"\n=== Threshold: flag if score >= {threshold} ===")
    print(f"              predicted risky | predicted safe")
    print(f"actual phish  {tp:>15} | {fn:>14}")
    print(f"actual legit  {fp:>15} | {tn:>14}")
    print(f"Precision: {precision:.1%}   Recall: {recall:.1%}   False positive rate: {fpr:.1%}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bad", default="data/bad_urls.txt")
    ap.add_argument("--good", default="data/good_urls.txt")
    ap.add_argument("--n", type=int, default=1000, help="URLs per class")
    args = ap.parse_args()

    bad = [(u, score_url(u)) for u in load(args.bad, args.n)]
    good = [(u, score_url(u)) for u in load(args.good, args.n)]
    print(f"Scored {len(bad)} phishing and {len(good)} legitimate URLs")

    for t in (10, 20, 30, 60):
        evaluate(bad, good, t)

    print("\n=== How often each check fires (phish vs legit) ===")
    cb = Counter(f.check for _, r in bad for f in r.findings)
    cg = Counter(f.check for _, r in good for f in r.findings)
    for name in sorted(set(cb) | set(cg)):
        print(f"{name:<16} phish: {cb[name]/len(bad):>6.1%}   legit: {cg[name]/len(good):>6.1%}")

    print("\n=== Legit sites wrongly flagged (score >= 20) ===")
    wrong = sorted((x for x in good if x[1].score >= 20), key=lambda x: -x[1].score)
    for u, r in wrong[:10]:
        print(f"{r.score:>3}  {u}  ->  {r.findings[0].reason}")

    print("\n=== Phishing missed (score < 20) ===")
    missed = [x for x in bad if x[1].score < 20]
    for u, r in missed[:10]:
        print(f"{r.score:>3}  {u[:90]}")


if __name__ == "__main__":
    main()