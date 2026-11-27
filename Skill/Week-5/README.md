# Week 5 — Token Economics (Experiment 5)

**Cost and rate-limit budgeting before building an LLM feature.**
Estimate tokens, API cost, and RPM/TPM capacity for a proposed feature
(sample: an FAQ assistant) *before* writing the feature, and get a
go / no-go planning recommendation. No LLM API is called in this lab.

> Folder note: the guide (Section 4) names this folder `TokenEconomics`.
> This pack uses your standard `week-5` folder name, same as Weeks 1–4 —
> the files inside are exactly the guide's TokenEconomics files. If your
> teacher asks for the folder by the guide's name, just rename `week-5`
> to `TokenEconomics`.

## Files
- `budget.py` — the budget planner (guide Section 5, code as given)
- `test_budget.py` — the guide's 4 automated tests (Section 7)
- `.env` — planning values from the guide (prices, limits, budgets) —
  these are **not** API credentials, they are just numbers
- `requirements.txt` — `python-dotenv`
- `output.txt` — a verified run (tests 4/4, report figures match the guide)
- `LAB_REPORT.md` — completed write-up incl. the Section 8 what-if analysis

## Run in VS Code (PowerShell terminal)
Extract `week-5` into `C:\Users\PRANAV\Desktop\KLH\Generative AI\`,
open the `week-5` folder in VS Code, Terminal → New Terminal, then:

```powershell
..\skill\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_budget.py
python budget.py
```

Your prompt must start with `(skill)`. If you prefer the guide's own
venv route instead: `python -m venv .venv` then
`.venv\Scripts\activate` then `pip install python-dotenv` — same result.

## Expected result
- Tests: **4 passed, OK**
- Report: 2,400,000 input + 600,000 output = 3,000,000 tokens/day,
  **$1.44/day, $43.20/month**, peak RPM 36, peak TPM 54,000
- Checks: RPM PASS, TPM PASS, Daily budget PASS, **Monthly budget REVIEW**

## ⚠ One guide inconsistency — read this before your viva
The guide's Section 6 interpretation says the sample is *within* the
monthly budget. Its own code disagrees: the budget checks apply the 20%
safety margin, so $43.20 × 1.2 = **$51.84 > $50** monthly budget →
Monthly = REVIEW, recommendation = REVISE. The code is delivered
exactly as the guide wrote it and all 4 guide tests pass — the
paragraph in the guide is the part that is wrong. This is actually the
lab's best talking point: *the safety margin is what pushes the feature
over budget; shortening answers (output 300 → 150 tokens) brings it
back WITHIN all limits* ($32.40/month, $38.88 with margin). Full
numbers in `LAB_REPORT.md`.
