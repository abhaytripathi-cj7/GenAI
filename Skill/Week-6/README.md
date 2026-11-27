# Week 6 — Golden Question Set + First Baseline Run (Release v0.1)

Write a **golden question set** (30 questions with expected answers,
keywords and sources), then run a **first baseline evaluation**: ask
every question to local **llama3.2 via Ollama**, score each answer by
keyword coverage, save `baseline_results.csv`, and label the
experiment **Release v0.1**.

## Files
- `golden_set.json` — the guide's 30 questions (Q001–Q030), taken
  exactly from the Week 6 document: question, expected_answer,
  keywords, source for each
- `main.py` — the baseline runner (guide Steps 1–8)
- `requirements.txt` — `requests`
- `test_week6.py` — offline tests (golden-set integrity + scoring) —
  extra file, not in the guide, so you can verify before the live run
- `output.txt` — what Muse verified before delivery, and what is
  still yours to run live
- `LAB_REPORT.md` — write-up for your record

## Before you run — Ollama (PowerShell, Terminal 1)
```powershell
ollama --version
ollama pull llama3.2
ollama list
```
The guide's machine showed Ollama 0.40.13 — any recent version is
fine. `llama3.2` is a ~2 GB download, once. Leave Ollama running
(system tray) while `main.py` runs. You already pulled llama3.2 in
Week 2, so this may already be done — `ollama list` tells you.

## Run in VS Code (PowerShell terminal, Terminal 2)
Extract `week-6` into `C:\Users\PRANAV\Desktop\KLH\Generative AI\`,
open the `week-6` folder in VS Code, then:

```powershell
..\skill\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_week6.py
python main.py
```

- `test_week6.py` → **8 tests, OK** (no Ollama needed)
- `main.py` → asks all 30 questions one by one at temperature 0.
  Allow several minutes. It prints each answer, matched/missing
  keywords, score and PASS (≥60%) / REVIEW, then the summary, and
  creates **`baseline_results.csv`** (header + 30 rows, Release v0.1).

## Guide fixes applied
1. Guide Step 5 says `pip install requirements.py` — a typo. Correct:
   `python -m pip install -r requirements.txt`.
2. The guide's `main.py` runs everything at import time. The delivered
   version wraps the run in `main()` under
   `if __name__ == "__main__":` — identical behaviour when run, but
   `test_week6.py` can import `calculate_score` without triggering a
   full evaluation.
3. Guide folder path is `D:\KLH\Gen AI\Programs\week6` — yours is
   `C:\Users\PRANAV\Desktop\KLH\Generative AI\week-6`, as in Weeks 1–5.

## Troubleshooting
| Symptom | Cause / fix |
|---|---|
| All 30 rows `ERROR`, Failed Requests: 30 | Ollama not running — launch Ollama, wait a few seconds, re-run `python main.py` |
| `model 'llama3.2' not found` | Run `ollama pull llama3.2` in Terminal 1 and let it finish |
| `ModuleNotFoundError: requests` | `(skill)` missing in prompt, or re-run the pip install line |
| Run seems slow | Normal — 30 sequential local generations; first answer is slowest while the model loads |
