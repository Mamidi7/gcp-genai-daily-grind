# INTERLEAVED SESSION PLAN — Days 1-14 Active Recall

**Rule**: Never study one day in a block. Mix 3-4 topics per 20-25 min session.
This forces your brain to choose the right tool, not just repeat one pattern.

---

## How to Use

1. Open a terminal.
2. Run: `cd ~/projects/gcp-genai-daily-grind/56_DAY_PRACTICE/active_recall && python revision_quiz.py`
3. The quiz already interleaves automatically — you don't pick the session.
4. If you want MANUAL control, use the session topics below to quiz yourself verbally or on paper.

---

## Session A — APIs + Python Core (Days 1, 2, 3, 7)
*Focus: Can you write working code under pressure?*

| # | Question ID | Type |
|---|---|---|
| 1 | d01_q03 | Write 4-line Gemini call |
| 2 | d07_q02 | requests.post with timeout |
| 3 | d03_q02 | sum_all(*args) function |
| 4 | d02_q02 | Fix string + int concat |
| 5 | d01_q05 | SDK vs raw HTTP comparison |
| 6 | d07_q03 | JSONDecodeError debug |
| 7 | d03_q03 | Mutable default bug |
| 8 | d07_q01 | GET vs POST recall |

**Time**: 20 min | **Goal**: 6/8 correct without peeking

---

## Session B — OOP + Files + Environment (Days 4, 5, 6)
*Focus: Do you understand object lifecycle and file safety?*

| # | Question ID | Type |
|---|---|---|
| 1 | d04_q03 | Document class from scratch |
| 2 | d05_q02 | Read/write JSON with `with` |
| 3 | d06_q02 | venv create + activate + freeze |
| 4 | d04_q04 | self. vs local variable debug |
| 5 | d05_q03 | File leak without `with` |
| 6 | d06_q03 | ModuleNotFound on colleague's machine |
| 7 | d04_q05 | classmethod vs staticmethod |
| 8 | d05_q04 | os.path vs pathlib |

**Time**: 20 min | **Goal**: 6/8 correct

---

## Session C — GCP Deploy + IAM + Storage (Days 8, 9, 10)
*Focus: Can you deploy safely and choose the right storage?*

| # | Question ID | Type |
|---|---|---|
| 1 | d08_q02 | gcloud deploy command |
| 2 | d09_q02 | BigQuery dataViewer role |
| 3 | d10_q01 | 4 GCS classes + retention |
| 4 | d08_q04 | Cloud Run vs Functions vs GKE |
| 5 | d09_q04 | Primitive vs Predefined vs Custom |
| 6 | d10_q04 | Early deletion fee debug |
| 7 | d08_q03 | Wrong project fix |
| 8 | d10_q05 | Match use cases to storage class |

**Time**: 20 min | **Goal**: 6/8 correct

---

## Session D — Config + FastAPI Core (Days 11, 12, 13)
*Focus: Fail-fast validation and clean error handling.*

| # | Question ID | Type |
|---|---|---|
| 1 | d11_q02 | get_project_id() fail-fast |
| 2 | d12_q02 | POST /echo endpoint |
| 3 | d13_q02 | @field_validator not empty |
| 4 | d12_q01 | 422 vs 500 |
| 5 | d11_q03 | .env committed to git |
| 6 | d13_q03 | exc.errors() JSONResponse crash |
| 7 | d12_q04 | FastAPI vs Flask vs Django |
| 8 | d13_q04 | field_validator vs Field pattern |

**Time**: 20 min | **Goal**: 6/8 correct

---

## Session E — SQL + Data Debugging (Days 14, 10, 5)
*Focus: Can you query correctly and spot bad joins?*

| # | Question ID | Type |
|---|---|---|
| 1 | d14_q02 | CTE + ROW_NUMBER top 3 per tag |
| 2 | d14_q03 | Join cardinality debug |
| 3 | d14_q06 | VECTOR_SEARCH schema design |
| 4 | d05_q05 | ROW_NUMBER vs RANK |
| 5 | d14_q04 | ROW_NUMBER vs RANK vs DENSE_RANK |
| 6 | d14_q05 | INNER vs LEFT vs CROSS |
| 7 | d10_q06 | Cloud Run vs Compute Engine |
| 8 | d14_q01 | What is a CTE |

**Time**: 20 min | **Goal**: 6/8 correct

---

## Session F — Mixed Application (Days 3, 7, 10, 14)
*Focus: Connecting Python functions to real deployment and data.*

| # | Question ID | Type |
|---|---|---|
| 1 | d03_q05 | *args + **kwargs function |
| 2 | d07_q04 | requests vs urllib |
| 3 | d10_q02 | /health endpoint |
| 4 | d10_q03 | Pydantic Field model |
| 5 | d14_q02 | CTE window function |
| 6 | d07_q05 | 200 vs 201 vs 204 |
| 7 | d03_q04 | *args vs **kwargs use case |
| 8 | d10_q04 | Storage class early deletion |

**Time**: 25 min | **Goal**: 6/8 correct

---

## Session G — Mixed Comparison + Design (Days 8, 9, 11, 12)
*Focus: Architecture decisions and security.*

| # | Question ID | Type |
|---|---|---|
| 1 | d09_q01 | Editor vs Owner |
| 2 | d08_q01 | What is Cloud Run |
| 3 | d11_q01 | Why separate config from code |
| 4 | d12_q03 | 422 debug |
| 5 | d09_q03 | Editor can't add IAM |
| 6 | d11_q04 | .env vs JSON vs ConfigMap |
| 7 | d08_q05 | GCS retention mnemonic |
| 8 | d11_q02 | get_project_id fail-fast |

**Time**: 20 min | **Goal**: 6/8 correct

---

## Spaced Repetition Schedule (Auto-Handled by Quiz)

The `revision_quiz.py` script handles this automatically, but here is the manual backup:

| Review | When | Action |
|---|---|---|
| 1st | Immediately after learning | Run quiz, self-test |
| 2nd | +1 day | Re-run quiz |
| 3rd | +3 days | Re-run quiz |
| 4th | +7 days | Re-run quiz |
| 5th | +14 days | Re-run quiz |
| 6th | +30 days | Re-run quiz |

If you rate a question **Again (1)**, its interval resets to 1 day.
If you rate it **Easy (4)**, it jumps ahead faster.

---

## Pass Criteria for Full Mastery

- **Level 1 (recall)**: 90%+ correct instantly
- **Level 2 (application)**: 80%+ correct, code compiles mentally
- **Level 3 (comparison/debug)**: 70%+ correct, can explain tradeoffs in an interview voice

If you fall below these thresholds on any session, that topic goes back to Day 1 spacing.
