# Week 6 Lab Report — Golden Question Set & Baseline Run v0.1
**Subject: GenAI (Y25) — Student: K.Pranav (2520030477), KLH**

## Aim
Create a golden question set with expected answers and sources, then
perform the first baseline run of a local LLM (llama3.2 via Ollama)
against it and officially label the experiment **Release v0.1**.

## The golden set
`golden_set.json` holds **30 questions (Q001–Q030)** covering Weeks
1–5 concepts: tokenization (BPE / WordPiece / SentencePiece, token,
token ID, token ratio), input/output tokens and API cost, context
window and rate limits, autoregressive generation, next-token
prediction, probability distributions, greedy decoding, sampling,
temperature, top-k and top-p, embeddings, and positional encoding
(sinusoidal and RoPE). Each item has:
- `question` and `expected_answer` (the reference answer),
- `keywords` (3–4 terms a correct answer should contain — used for scoring),
- `source` (Hugging Face Transformers docs, Google Gemini API docs, or the original papers).

## Method
1. Check Ollama (`ollama --version`) and pull the model (`ollama pull llama3.2`).
2. `main.py` loads the golden set and sends each question to
   `http://localhost:11434/api/generate` with `temperature: 0`
   (deterministic — the same run should be reproducible).
3. **Keyword scoring:** score = matched keywords ÷ total keywords × 100
   (case-insensitive substring match). ≥ 60% = PASS, below = REVIEW.
4. Every result (answer, matched/missing keywords, score, status,
   source, model, release) is written to `baseline_results.csv`.
5. A summary prints totals, pass/review/error counts and average
   keyword coverage, dated, labelled Release v0.1.

## Verification done before the live run
- Golden set integrity: 30 items, IDs Q001–Q030 in order, all fields
  present — **automated test, passed**.
- Scoring function: 100% / 50% / 0% cases, case-insensitivity,
  empty-keyword edge case — **automated tests, passed (8/8 total)**.
- Full pipeline (request → score → CSV → summary) run end-to-end
  against a local stub of the Ollama API: 30/30 responses processed,
  CSV with header + 30 rows created, completion banner printed.
- Error path: with Ollama stopped, all 30 rows record ERROR and the
  CSV is still saved — the program fails safe, it does not crash.

## Live baseline result
**To be filled from your own run** (`python main.py` with Ollama
running): paste the BASELINE EVALUATION SUMMARY block here —
Total Questions 30, Passed __, Review __, Errors __, Average Keyword
Coverage __%. Those numbers are the Release v0.1 baseline that later
releases (prompt changes, model changes) will be compared against.
They are deliberately not pre-filled: a baseline is only meaningful
if it is the real model's output.

## Conclusion
A reusable evaluation harness now exists: a sourced golden set, a
deterministic local model run, transparent keyword scoring, and a
CSV record per question. Keyword coverage is a rough signal, not a
judgement of answer quality — a fluent wrong answer can score well
and a correct paraphrase can score poorly — which is why the CSV
keeps the full answer text for manual review of the REVIEW rows.
