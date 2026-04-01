# Day 20 Interview Pack — Eval Harness

## 30-Second Version
"I built an automated eval harness that runs 10 test cases against my LLM, scores each on correctness/completeness/safety, logs results to JSON, and produces a pass/fail report. I tracked scores across runs: baseline was 60%, improved run hit 100% after fixing safety guardrails."

---

## 90-Second STAR Answer

**Situation:** I needed to prove my RAG system was actually getting better as I made changes. Without measurement, every "improvement" was just a guess.

**Task:** Build an automated eval harness that could run after every code change and produce a measurable quality score.

**Action:** I built a 3-component system:
1. **Test suite** (Day 19): 10 cases covering factual accuracy, completeness, and safety, each with ground truth and scoring rubrics
2. **Eval runner**: Sends questions to LLM, scores responses against rubrics using key fact matching, logs per-case results
3. **Trend tracker**: Compares runs over time to catch regressions

The baseline run revealed 2 safety failures: one where the model hallucinated a self-healing capability, and one where it disclosed fake PII instead of refusing. After adding safety guardrails, the improved run scored 100%.

**Result:** Every change to the system now has a before/after eval score. Regressions are caught immediately. The eval suite itself became a portfolio artifact I can demo in interviews.

---

## 3-Minute Technical Deep Dive

### Why Evals Matter More Than Models
The model is a commodity. Evals are your competitive advantage.
- Everyone uses the same Gemini/GPT API
- Your eval suite is YOUR domain knowledge encoded as test cases
- "What do you test?" = "What do you care about?" = "What are your business requirements?"

### The 3-Layer Scoring Architecture
```
Layer 1: CORRECTNESS
  - Key fact matching: does the response contain required information?
  - Not exact string match — keyword overlap with threshold (60%)
  - Configurable: min_facts_for_correct controls the bar

Layer 2: COMPLETENESS  
  - Word overlap with ground truth
  - Catches answers that are right but incomplete
  - Example: "2.3M transactions" misses "45 min latency"

Layer 3: SAFETY
  - Forbidden pattern detection
  - Safety violations override everything
  - One safety fail = entire case is INCORRECT, regardless of other scores
```

### Production Considerations
- **Cost**: Each eval run costs 10 API calls. At $0.001/call = $0.01/run. Negligible.
- **Speed**: 10 calls × 2s avg = 20 seconds per run. Fast enough for CI/CD.
- **False positives**: Key fact matching can miss synonyms. Solution: semantic similarity (Day 17).
- **Coverage**: 10 cases is a starting point. Production needs 50-100 minimum.

---

## Common Interview Questions

**Q: How do you handle subjective answers?**
A: Use a 3-level rubric (correct/partial/incorrect) instead of binary pass/fail. Accept that some subjectivity exists. For production, use LLM-as-judge to handle nuanced scoring.

**Q: What if the ground truth is wrong?**
A: Version your test suite. Review and update ground truths regularly. Treat the test suite like production code — it needs PRs and reviews.

**Q: How does this connect to RLHF?**
A: Eval test cases → preference pairs (Day 25) → SFT training data (Day 40). The eval system IS the data collection system for model improvement.
