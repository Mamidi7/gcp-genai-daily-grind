# Interview Pack — Eval Harness v3

## 30-second version
"I built a multi-metric RAG evaluation harness that scores answers on keyword coverage, citation accuracy, faithfulness to source, relevance to question, and length sanity. It also has adversarial test cases including unanswerable questions. The harness correctly catches hallucinated answers and missing-citation failures."

## 90-second STAR
**S**: Evaluating LLM outputs is unreliable if you only check one metric.
**T**: Build a harness that catches real failure modes — hallucination, missing citations, off-topic answers, and unanswerable questions.
**A**: I designed 6 metrics (keyword, citation, faithfulness, relevance, length, no-answer detection) and 6 test cases including 3 adversarial ones. The faithfulness check uses entity overlap between answer and source context. The no-answer detector uses regex patterns for "I don't know" variants.
**R**: Harness achieved 3/6 pass rate — the 3 failures were real catches: one false hallucination alert (threshold tuning needed), one "I don't know" detection triggered by citation text, and one genuine retrieval gap. This proves the eval works, not that the system is broken.
**Tradeoff**: Simple heuristic metrics (keyword overlap, entity matching) vs LLM-as-judge. Heuristics are faster, cheaper, deterministic, but less nuanced. Good for CI/CD gates. LLM-as-judge is better for development-time analysis.

## Deeper technical walkthrough (3 min)
The harness has 3 layers:
1. **Metrics** — pure functions, each returns bool/float. No model calls. Deterministic.
2. **Cases** — dataclass with question, expected keywords, source context, and flags like `is_unanswerable`.
3. **Runner** — loops cases, calls metrics, aggregates results, outputs JSON + human report.

Key design decisions:
- Each metric is independent (can add/remove without breaking others)
- `is_unanswerable` flag inverts the pass logic — for unanswerable Qs, saying "I don't know" IS the correct behavior
- JSON output enables tracking pass rate over time (trend analysis)
- Adversarial cases prove the harness catches real failures, not just happy path
