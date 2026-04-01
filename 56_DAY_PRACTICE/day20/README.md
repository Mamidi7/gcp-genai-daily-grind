# Day 20 — Eval Harness v1: Automated Evaluation Pipeline

## Objective
Build an automated eval harness that runs all test cases, scores LLM outputs, logs results, and produces a summary report. This ties together Days 16-19 into a production eval system.

## Why This Matters
- This is THE artifact: "I built an eval harness that runs 10 cases and logs pass/fail"
- Anthropic role: "Build eval pipelines for model training/deployment"
- OpenAI role: "Build evals + harnesses that capture real-world quality"
- Every hiring manager wants to see that you MEASURE, not just build

## Architecture
```
┌─────────────────┐
│ Test Suite      │  Day 19's 10 test cases
│ (10 cases)      │  question + ground_truth + rubric
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Eval Harness    │  THIS DAY
│ Runner          │  1. Send question to LLM
│                 │  2. Get response
│                 │  3. Score against rubric
│                 │  4. Log result
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│Results │ │Summary │
│Log JSON│ │Report  │
│per case│ │+ trend │
└────────┘ └────────┘
```

## Files
- `solution.py` — Full eval harness with runner, logger, reporter
- `exercises.py` — Practice challenges
- `notes.md` — Debug journal and interview prep
- `eval_results.json` — Sample output (created on run)

## Interview Conversion
- **30s**: "I built an automated eval harness that runs 10 test cases against the LLM, scores each on correctness/completeness/safety, and produces a pass/fail report. I can track eval scores over time as I improve the system."
- **90s STAR**: See interview_pack_day20.md
