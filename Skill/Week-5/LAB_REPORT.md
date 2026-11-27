# Week 5 Lab Report — Token Economics
**Experiment 5: Cost and Rate-Limit Budgeting Before Building an LLM Feature**
Student: K.Pranav (2520030477), KLH — GenAI (Y25)

## Aim
Before implementing an LLM-powered feature, estimate its token usage,
API cost, and whether expected traffic fits provider RPM/TPM limits.
Build a budgeting tool that takes feature assumptions, calculates
usage and cost, checks limits with a safety margin, and reports a
go / no-go recommendation.

## Concepts (guide Section 1)
- **Input tokens** — system prompt + user prompt + history + retrieved context + tool schemas.
- **Output tokens** — tokens the model generates; usually priced differently from input.
- **RPM / TPM** — provider caps on requests/minute and tokens/minute.
- **Safety margin** — capacity reserved for spikes, estimation error and retries (20% here).
- A feature can be affordable but exceed rate limits, or fit rate limits but exceed budget — both checks are needed.

## Setup (guide Section 4)
Folder with `.env`, `budget.py`, `test_budget.py`, `requirements.txt`
(`python-dotenv`). Sample feature assumptions: 2,000 requests/day,
1,200 input + 300 output tokens/request, peak 30 requests/minute,
input $0.30 / output $1.20 per 1M tokens, RPM limit 60, TPM limit
100,000, daily budget $2, monthly budget $50, safety margin 20%.

## Formulas (guide Section 3)
- Input tokens/day = R × I; Output tokens/day = R × O; Total = R × (I + O)
- Daily cost = [(R × I × Pi) + (R × O × Po)] / 1,000,000; Monthly = Daily × 30
- Peak TPM = peak requests/minute × (I + O); margin applied × 1.2 for planning checks

## Result — baseline run (verified, matches guide Section 6 table exactly)
| Metric | Value |
|---|---|
| Input tokens/day | 2,400,000 |
| Output tokens/day | 600,000 |
| Total tokens/day | 3,000,000 |
| Daily cost | $1.44 |
| Monthly cost (30 days) | $43.20 |
| Peak RPM with margin | 36.0 (limit 60) — PASS |
| Peak TPM with margin | 54,000 (limit 100,000) — PASS |
| Daily budget ($2) | $1.44 × 1.2 = $1.728 — PASS |
| Monthly budget ($50) | $43.20 × 1.2 = $51.84 — **REVIEW** |

**Automated tests: 4/4 passed** (cost estimate, capacity pass,
RPM-limit fail case, monthly-budget fail case).

**Recommendation for the baseline: REVISE** — because the safety
margin pushes the monthly figure over budget. Note: the guide's
Section 6 paragraph claims the sample is within the monthly budget;
that holds only *without* the margin ($43.20 < $50). The guide's own
code applies the margin to the budget checks, so REVIEW is the
correct output of the delivered program.

## What-if analysis (guide Section 8 — all rows are real runs of budget.py)
| Scenario | Daily | Monthly | Peak RPM | Peak TPM | Result |
|---|---|---|---|---|---|
| Baseline | $1.44 | $43.20 | 36.0 | 54,000 | Monthly REVIEW (margin) |
| Double requests/day (4,000) | $2.88 | $86.40 | 36.0 | 54,000 | Daily + Monthly FAIL |
| Larger context (input 3,000) | $2.52 | $75.60 | 36.0 | 118,800 | TPM + budgets FAIL |
| Shorter answers (output 150) | $1.08 | $32.40 | 36.0 | 48,600 | **ALL PASS — WITHIN** |
| Peak 50 req/min | $1.44 | $43.20 | 60.0 | 90,000 | RPM at limit, PASS |
| Peak 51 req/min | $1.44 | $43.20 | 61.2 | 91,800 | **RPM FAILS first** |
| Peak 56 req/min | $1.44 | $43.20 | 67.2 | 100,800 | RPM + TPM FAIL |
| Pricier model (in $1.20 / out $4.80) | $5.76 | $172.80 | 36.0 | 54,000 | Budgets FAIL, capacity unchanged |

Findings:
1. Cost scales linearly with requests/day and token sizes; capacity (RPM/TPM) does not depend on daily volume, only on the peak minute.
2. RPM is the first capacity limit hit (peak 51/min), TPM next (peak 56/min).
3. Longer retrieved context is expensive twice: it raises input cost *and* TPM.
4. Raising model price changes cost only — token volume and capacity are untouched.

## Go / No-Go recommendation
**Conditional GO after one design change:** cap average output at
~150 tokens (response-length target). That single change brings every
check inside its limit with the 20% margin kept ($32.40/month,
$38.88 with margin, TPM 48,600). Without it, the honest answer for
the baseline assumptions is NO-GO on the monthly budget once the
safety margin is applied — which is exactly the kind of problem this
pre-build budgeting step exists to catch.

## Conclusion
Token budgeting, cost estimation, RPM/TPM capacity checks, safety
margins and budget thresholds were implemented and tested in a
reusable Python planner. The estimate is a planning tool, not a
billing guarantee: real usage must be measured with the provider's
tokenizer/usage metadata before launch, and retries are not free.
