# Day 19 — Eval Intro: 10 Test Q&A Pairs with Scoring Rubrics

## Objective
Build a test suite for evaluating LLM outputs. Create 10 question-answer pairs with scoring rubrics. This is the #1 hiring signal at both Anthropic and OpenAI.

## Why This Matters
- Evals are mentioned in EVERY role at Anthropic and OpenAI
- "How do you evaluate your LLM outputs?" is the most common interview question
- Without evals, you're flying blind — you can't improve what you can't measure
- This connects directly to Day 20 (Eval Harness) and Day 25 (Preference Eval)

## Architecture
```
┌──────────────┐
│ Test Suite   │  10 Q&A pairs with rubrics
│ (this day)   │  each has: question, ground_truth, rubric
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Eval Runner  │  (Day 20)
│ calls LLM    │  gets response → scores against rubric
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Results Log  │  pass/fail per case, overall accuracy
└──────────────┘
```

## Files
- `solution.py` — Test suite with 10 cases, scoring rubrics, comparison logic
- `exercises.py` — Practice building your own eval cases
- `notes.md` — Concepts and interview prep

## Interview Conversion
- **30s**: "I built an eval suite with 10 test cases and scoring rubrics to measure LLM output quality on a banking ETL domain. Each case has a ground truth answer and a 3-level scoring rubric."
- **90s STAR**: "To measure whether my RAG system was actually improving, I built an eval suite with 10 domain-specific test cases. Each case has a question, expected answer, and a rubric scoring correctness, completeness, and safety. Running this after every change gave me a confidence score I could track over time."
