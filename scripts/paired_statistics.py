"""
Uncertainty estimates and judge error-list counts for the handball paper.

Uses existing outputs only (no new model runs):
  matched_scores.csv  - per-clip paired scores written by full_pipeline.py
  exp2_*.jsonl        - raw judge outputs (base + retry runs)

Reports, per criterion and for the overall score:
  * mean paired difference (human - model)
  * 95% bootstrap CI resampling clips, and resampling whole source matches
    (cluster bootstrap; match id = first token of the clip file name)
  * exact McNemar test for the five binary criteria (scores 1/2),
    Wilcoxon signed-rank test + rank-biserial r for the overall score
  * Holm correction across the six tests
  * per-match mean differences
And, for each source, the totals of the judge's hallucinations /
incorrect_details / missing_details lists over the paired clips.

Usage:
  python paired_statistics.py <matched_scores.csv> <judging_dir>
"""

import csv
import json
import os
import sys

import numpy as np
from scipy.stats import binomtest, wilcoxon

CRITERIA = ["correctness", "completeness", "temporal_consistency", "faithfulness", "clarity"]
B = 10000
SEED = 2026


def match_id(path):
    return path.replace("\\", "/").split("/")[-1].split("_")[0]


def rank_biserial(d):
    nz = d[d != 0]
    if len(nz) == 0:
        return 0.0
    order = np.argsort(np.abs(nz), kind="mergesort")
    ranks = np.empty(len(nz))
    absd = np.abs(nz)[order]
    i = 0
    while i < len(absd):  # average ranks for ties
        j = i
        while j + 1 < len(absd) and absd[j + 1] == absd[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    pos, neg = ranks[nz > 0].sum(), ranks[nz < 0].sum()
    return (pos - neg) / (pos + neg)


def holm(pvals):
    items = sorted(pvals.items(), key=lambda t: t[1])
    out, running = {}, 0.0
    for i, (k, p) in enumerate(items):
        running = max(running, min(1.0, (len(items) - i) * p))
        out[k] = running
    return out


def uncertainty(scores_csv):
    rows = list(csv.DictReader(open(scores_csv, encoding="utf-8")))
    matches = np.array([match_id(r["video_path"]) for r in rows])
    ids = np.unique(matches)
    rng = np.random.default_rng(SEED)
    results, pvals = {}, {}
    for c in CRITERIA + ["overall"]:
        h = np.array([float(r[f"{c}_hum"]) for r in rows])
        g = np.array([float(r[f"{c}_gen"]) for r in rows])
        d = h - g
        n = len(d)
        clip_boot = [d[rng.integers(0, n, n)].mean() for _ in range(B)]
        match_boot = [np.concatenate([d[matches == k] for k in rng.choice(ids, len(ids))]).mean()
                      for _ in range(B)]
        wins, losses = int((d > 0).sum()), int((d < 0).sum())
        if c == "overall":
            test, p = "Wilcoxon", wilcoxon(h, g, zero_method="wilcox").pvalue
        else:
            test, p = "McNemar (exact)", binomtest(wins, wins + losses, 0.5).pvalue if wins + losses else 1.0
        pvals[c] = p
        results[c] = dict(
            diff=d.mean(), clip_ci=np.percentile(clip_boot, [2.5, 97.5]),
            match_ci=np.percentile(match_boot, [2.5, 97.5]), wins=wins, ties=int((d == 0).sum()),
            losses=losses, test=test, p=p, r=rank_biserial(d),
            per_match={k: d[matches == k].mean() for k in ids})
    adj = holm(pvals)
    print(f"n = {len(rows)} paired clips, {len(ids)} matches, B = {B}, seed = {SEED}\n")
    for c, v in results.items():
        pm = sum(1 for x in v["per_match"].values() if x > 0)
        print(f"{c:21} diff={v['diff']:+.3f}  clipCI=[{v['clip_ci'][0]:+.3f},{v['clip_ci'][1]:+.3f}]  "
              f"matchCI=[{v['match_ci'][0]:+.3f},{v['match_ci'][1]:+.3f}]  W/T/L={v['wins']}/{v['ties']}/{v['losses']}  "
              f"{v['test']} p={v['p']:.3g} Holm p={adj[c]:.3g}  r={v['r']:+.2f}  matches human>model={pm}/{len(ids)}")
        print("      per match: " + ", ".join(f"{k}={x:+.3f}" for k, x in v["per_match"].items()))


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def merged_valid(judging_dir, base, retry):
    retry_by = {d["video_path"]: d for d in load_jsonl(os.path.join(judging_dir, retry))}
    rows = [retry_by.get(d["video_path"], d) if d.get("status") == "error" else d
            for d in load_jsonl(os.path.join(judging_dir, base))]
    return {d["video_path"]: d for d in rows
            if d.get("status") != "error" and all(f"{c}_points" in d for c in CRITERIA)}


def error_lists(judging_dir):
    model = merged_valid(judging_dir, "exp2_results.jsonl", "exp2_New_results.jsonl")
    human = merged_valid(judging_dir, "exp2_human_results.jsonl", "exp2_New_Human_results.jsonl")
    pairs = sorted(set(model) & set(human))
    print(f"\nJudge error lists over {len(pairs)} paired clips")
    for name, src in (("human", human), ("model", model)):
        for field in ("hallucinations", "incorrect_details", "missing_details"):
            c = np.array([len(src[p].get(field) or []) for p in pairs])
            print(f"{name:5} {field:18} total={c.sum():5d}  mean={c.mean():.2f}  "
                  f">=1: {int((c > 0).sum())} ({100 * (c > 0).mean():.1f}%)")
        for fp in (1, 2):
            c = [len(src[p].get("hallucinations") or []) for p in pairs if src[p]["faithfulness_points"] == fp]
            if c:
                print(f"      faithfulness={fp}: n={len(c)}, mean hallucinations={np.mean(c):.2f}, "
                      f"empty lists={sum(1 for x in c if x == 0)}")


if __name__ == "__main__":
    uncertainty(sys.argv[1])
    if len(sys.argv) > 2:
        error_lists(sys.argv[2])
