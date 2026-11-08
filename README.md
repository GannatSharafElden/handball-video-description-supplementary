# Handball Video Description Dataset — Supplementary Materials

This repository accompanies the research paper **“Handball Event Recognition Video Dataset”** and provides documentation of the handball-specific annotation rubric and the automated video-description evaluation prompt.

## Study overview

Professional handball footage was segmented into 16-second clips. A handball-experienced annotator wrote descriptions of visible events; Qwen3-VL-8B-Instruct produced independent descriptions. Kimi-K2.6 evaluated one description at a time against 12 regularly sampled frames from each clip using five criteria: correctness, completeness, temporal consistency, faithfulness, and clarity. The paper reports analyses for **247 clips with valid paired evaluations**.

## Supplementary appendix

| File | Contents | Status |
| --- | --- | --- |
| [`appendix/prompts/evaluation_judge_prompt.txt`](appendix/prompts/evaluation_judge_prompt.txt) | Full automated judge rubric and JSON output template | Transcribed from the paper's Appendix A |
| [`appendix/annotation_guidelines.md`](appendix/annotation_guidelines.md) | Handball-specific description rubric, examples, and evidence restrictions | Summary reconstructed from paper §3.2; **not** represented as the exact original annotator instructions |
| [`appendix/scoring_and_interpretation.md`](appendix/scoring_and_interpretation.md) | Criterion anchors, scoring transformations, rating proportions and limitations | Supplementary explanation of paper §§3.3–6 |
| [`scripts/paired_statistics.py`](scripts/paired_statistics.py) | Post-hoc paired analysis: exact McNemar tests (binary criteria), Wilcoxon signed-rank test and rank-biserial r (overall score), Holm correction, clip- and match-level bootstrap 95% CIs, per-match differences, and counts of judge-listed hallucinations / incorrect / missing details | Code used for paper §4.3 (Table 5) and §5 (Table 7) |

## Evaluation design

Each description received five integer ratings, either 1 or 2. The overall rating was the sum (range: 5–10). A value such as 70.24% correctness is **the mean rating divided by the possible maximum of 2**, not the fraction of factually correct descriptions. The paper separately reports rating counts and proportions. Scores are outputs of an automated judge and were not independently validated as factual accuracy rates.

## Scope and reproducibility

These files document the evaluation instructions and rubric as described in the manuscript. They do **not** include video footage, third-party datasets, model weights, evaluation outputs, or API credentials. The analysis script in `scripts/` is included; it runs on the per-clip score file (`matched_scores.csv`) and the raw judge outputs (`exp2_*.jsonl`), which are not part of this repository:

```
python scripts/paired_statistics.py matched_scores.csv <judging_dir>
```

Requirements: Python 3 with `numpy` and `scipy`. Bootstrap results use 10,000 resamples with seed 2026. The original description-generation prompt is **not included**, because its complete verbatim text is not available in the supplied manuscript. If an exact archived prompt becomes available, it can be added and clearly identified.

## Citation

Cite the accompanying research paper when referring to the study. In the paper, reference this repository as supplementary materials, preferably using a commit-pinned link or archived release.

## License and rights

No license is assigned in this starter repository. Check author/coauthor agreement, the publisher's policies and any third-party content rights before public release. Add a suitable license if appropriate.
