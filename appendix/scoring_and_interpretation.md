# Evaluation scoring and interpretation

## Five criteria and two ratings

These criterion-specific descriptions clarify the original shared threshold. They are **not** a new retrospectively applied rubric.

| Criterion | Score 1 — limited / insufficient | Score 2 — excellent / nearly perfect |
| --- | --- | --- |
| Correctness | Incorrect objects, actions, player or ball behaviour; inadequate visible-event accuracy | Main visible objects and actions described accurately |
| Completeness | Important visible actions or scene changes omitted | Main visible events comprehensively covered |
| Temporal consistency | Confused event order or unsupported temporal sequence | Observable order faithfully represented |
| Faithfulness | Unsupported or hallucinated visual details | Description grounded in visible evidence |
| Clarity | Vague, confusing or repetitive expression | Clear, concise and understandable expression |

## Score conversion

Each criterion rating `s_j` is either 1 or 2; the total `S = s_1 + s_2 + s_3 + s_4 + s_5` ranges from 5 to 10.

- Criterion percentage of maximum: `100 × mean(s_j) / 2`.
- Overall percentage of maximum: `100 × mean(S) / 10`.

| Total | Percentage of maximum |
| --- | --- |
| 5 | 50% |
| 6 | 60% |
| 7 | 70% |
| 8 | 80% |
| 9 | 90% |
| 10 | 100% |

The percentage is a **normalized rubric score**, not factual correctness prevalence. For example, the manuscript reports mean human correctness rating 1.404858/2 = 70.24% of maximum; separately, 100 of 247 human descriptions (40.49%) received a rating of 2.

A rating proportion counts the fraction of the `N = 247` paired records assigned that rating, for each source and criterion: `100 × number with rating r / 247`.

## Limitations

The original binary rubric did **not** systematically distinguish minor peripheral mistakes from major errors that change the main action, actor/team, possession, outcome or sequence. Such error-severity rates cannot be recovered from the binary rating alone. Both ratings and free-text error reports are produced by an automated judge, not independently validated against complete videos by human experts.
