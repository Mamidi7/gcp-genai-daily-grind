# Day 19 Notes

## What I built today
- 10 eval test cases in banking/ETL domain
- 3-level scoring rubric: correct, partial, incorrect
- Multi-dimensional scoring: correctness, completeness, safety
- Key fact matching engine with configurable thresholds
- Safety violation detection for dangerous LLM outputs
- Full failure analysis pipeline

## Key concepts learned
1. **Ground truth**: You need a "correct answer" to compare against. Without it, eval is vibes.
2. **Rubric**: A checklist of key facts that MUST appear and patterns that MUST NOT appear.
3. **3-level scoring**: Correct/partial/incorrect is the industry standard (not just pass/fail).
4. **Safety evals**: Test that the model REFUSES dangerous requests (account numbers, PII).
5. **Test case diversity**: Mix factual, edge cases, and safety cases.

## Error I hit
- eval_008: Model said "automatically corrects variance" but ground truth says "manual investigation"
  - Eval correctly caught this as INCORRECT — the rubric forbids "automatic correction"
- eval_009: Model gave fake account number — eval caught safety violation
  - This is a designed failure to prove the eval works

## Root cause
- eval_008: Model hallucinated a self-healing capability
- eval_009: Model complied with dangerous request instead of refusing

## Fix applied (for Day 20)
- eval_008: Add "self-healing" to forbidden patterns, add "manual investigation" to key facts
- eval_009: Add safety system prompt that refuses PII requests

## 90-second interview version
"I built an eval suite with 10 test cases covering factual accuracy, completeness, and safety. Each case has a ground truth answer, key facts checklist, and forbidden patterns. The eval caught a hallucinated self-healing capability and a dangerous PII disclosure. The key insight: evals must test both what the model SHOULD say and what it should NOT say."

## How this connects
- Day 19 = eval design (this suite)
- Day 20 = eval automation (run this suite automatically, log results)
- Day 25 = preference eval (compare two responses, not just one)
- Day 26 = adversarial testing (try to BREAK the system)
