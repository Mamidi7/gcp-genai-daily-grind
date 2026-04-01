# Day 20 Notes

## What I built today
- EvalHarness class: automated runner that tests all cases and produces reports
- RunResult: structured output with per-case scores + aggregates
- TrendTracker: compare eval scores across runs to measure improvement
- JSON output for results (machine-readable)
- Formatted report output (human-readable)
- Two demo runs: baseline (60%) and improved (100%)

## Key concepts learned
1. **Eval harness = automated QA for AI**: Just like CI/CD tests code, eval harness tests AI outputs
2. **Run comparison**: Every change to the system should produce a new eval run
3. **Trend matters more than single run**: Going from 60% → 80% → 95% tells a story
4. **Safety failures are hard failures**: Even one PII leak makes the whole run "unsafe"

## Error I hit
- Baseline run showed 60% accuracy with 2 safety failures (eval_008, eval_009)
- eval_008: hallucinated self-healing capability
- eval_009: gave fake account number instead of refusing

## Root cause
- No safety guardrails in the mock LLM
- Model complies with requests instead of evaluating safety

## Fix applied
- Updated mock responses with correct refusal behavior
- Added safety system prompt (will be real in production)
- Re-ran eval → 100% accuracy

## Prevention added
- Every LLM deployment must pass eval harness before going live
- Safety failures block deployment regardless of overall score
- Trend tracker catches regressions

## 90-second interview version
"I built an automated eval harness for my RAG system. It runs 10 test cases covering factual accuracy, completeness, and safety, produces a pass/fail report, and tracks scores across runs. The baseline showed 60% accuracy with a safety failure — the model gave fake account data. After adding safety guardrails and fixing prompt engineering, the improved run hit 100%. The key insight: eval is not optional — it's how you prove your system actually works."

## How this connects
- Day 16-19: building blocks (structured output, embeddings, chunking, test cases)
- Day 20: ties everything together into a measurable system
- Day 25: preference eval (compare TWO responses, not just score one)
- Day 26: adversarial testing (try to break the system on purpose)
- Day 42: ETL pipeline feeding data INTO this eval system
