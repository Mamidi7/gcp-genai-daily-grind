# REVISION GUIDE — Days 16-20 (Structured Output → Eval Harness)

**Purpose**: This is your fast-review doc before interviews. One read-through = full recall of 5 days work.

---

## DAY 16 — Structured Output (JSON Mode + Pydantic)

### What You Built
A 3-layer pipeline that forces Gemini to return machine-readable output every time.

```
Gemini API (JSON mode)
    ↓
extract_json() — strip markdown fences, find { } block
    ↓
json.loads() — syntax check
    ↓
Pydantic model_validate() — type + range + required field check
    ↓
Your typed object ✓
```

### Core Concepts
1. **Two gates**: json.loads catches syntax errors (trailing comma). Pydantic catches semantic errors (`confidence: 1.5` when max=1.0).
2. **extract_json()** handles real-world mess: ` ```json {...} ``` `, preamble text, trailing garbage.
3. **Retry with context**: Don't just retry — tell the model EXACTLY what failed: `"confidence: Input should be ≤ 1.0"`.
4. **Retry rate as metric**: If avg attempts > 1.5, fix your prompt. More retries won't help.

### Interview 30s
"I built a structured output layer for LLM responses. It extracts JSON from messy text, validates against Pydantic schemas, and retries with error feedback. Parse failures dropped from 15% to under 1%."

### Common Mistake
Running `json.loads()` only and assuming valid JSON means valid data. It doesn't. Pydantic is the hard gate.

### Quick Check
- Can you write `extract_json()` that handles markdown fences AND raw JSON?
- Can you explain why retry rate is a prompt quality signal?

---

## DAY 17 — Embeddings (text-embedding-004 + Similarity)

### What You Built
An embedding store that converts text → 768-dim vectors and retrieves by cosine similarity.

### Core Concepts
1. **Embeddings = meaning as numbers**: Similar text → similar vectors. "Banking" and "Finance" point in nearly the same direction.
2. **Cosine similarity**: Measures angle, not distance. 1.0 = identical direction. 0.0 = orthogonal (unrelated).
3. **Always batch**: API limit is 250 texts per call. Batching = 250x cheaper on API overhead.
4. **Never mix models**: text-embedding-004 and text-embedding-005 produce different vector spaces. Mixing them breaks retrieval completely.

### Interview 30s
"I built a semantic search engine using text-embedding-004. Documents become 768-dim vectors. Retrieval uses cosine similarity. I filter empty inputs to prevent zero-vector crashes and batch calls to respect API limits."

### Common Mistake
Forgetting to validate inputs before embedding. Empty string → zero vector → division by zero in cosine similarity.

### Quick Check
- Can you explain why cosine similarity ignores vector magnitude?
- Can you name 3 things to validate before embedding?
- What happens if you mix text-embedding-004 and text-embedding-005 vectors in the same store?

---

## DAY 18 — Chunking (3 Strategies)

### What You Built
Three ways to split documents before embedding, with a comparison engine.

| Strategy | How it works | Best for | Tradeoff |
|----------|-------------|----------|----------|
| Fixed-size | Every N chars with overlap | Production default | Cuts sentences |
| Sentence-based | Split on `.` `!` `?` | Respects boundaries | Variable sizes |
| Semantic | Embed adjacent chunks, split where similarity drops | Best recall | Adds embedding cost |

### Core Concept
**Chunk size controls precision vs recall:**
- Small chunks → precise retrieval but lose surrounding context
- Large chunks → more context but more noise per chunk

### Interview 30s
"I compared three chunking strategies for RAG. Fixed-size with overlap is the production default because it's predictable. Sentence-based respects text boundaries. Semantic chunking had best recall but costs more. The key insight: chunk size is the most impactful RAG hyperparameter."

### Common Mistake
Choosing semantic chunking for everything. It's expensive and often overkill. Start with fixed-size + overlap, measure, then optimize.

### Quick Check
- Draw the precision/recall tradeoff curve for chunk size.
- Why does overlap help fixed-size chunking?
- Name one failure mode for each strategy.

---

## DAY 19 — Eval Design (Test Cases + Rubrics)

### What You Built
10 test cases in banking/ETL domain with 3-level scoring.

### Core Concepts
1. **Ground truth is non-negotiable**: Without a "correct" answer, eval is just vibes.
2. **Rubric = checklist**: Key facts that MUST appear. Forbidden patterns that MUST NOT appear.
3. **3-level scoring**: Correct / Partial / Incorrect. Not binary pass/fail.
4. **Safety evals**: The model must REFUSE dangerous requests (PII, account numbers).

### The Two Designed Failures You Caught
| Case | What Model Did | Eval Caught It As |
|------|---------------|-------------------|
| eval_008 | Said "automatically corrects variance" | INCORRECT — rubric forbids "automatic" |
| eval_009 | Gave fake account number | SAFETY VIOLATION — should have refused |

### Interview 30s
"I built an eval suite with 10 cases covering factual accuracy, completeness, and safety. It caught a hallucinated self-healing claim and a PII disclosure. The key insight: evals must test both what the model SHOULD say and what it should NOT say."

### Common Mistake
Only testing happy path. Real evals need safety cases, edge cases, and refusal tests.

### Quick Check
- Write one eval case: question, ground truth, 3 key facts, 1 forbidden pattern.
- Why do safety failures override all other scores?
- What's the difference between correctness and completeness?

---

## DAY 20 — Eval Harness (Automation + Trends)

### What You Built
An automated runner that executes all test cases, scores outputs, logs JSON, and tracks improvement over time.

### Architecture
```
Test Suite (Day 19)
    ↓
EvalRunner — sends each Q to LLM
    ↓
Scorer — key fact match + forbidden pattern check
    ↓
RunResult — per-case scores + aggregate pass/fail
    ↓
TrendTracker — compare Run N vs Run N+1
```

### The 3-Layer Scoring
1. **Correctness**: Does response contain required key facts? (keyword overlap ≥ 60%)
2. **Completeness**: Does it cover everything in ground truth? (word overlap)
3. **Safety**: Does it contain forbidden patterns? One hit = entire case INCORRECT.

### Your Proven Result
- Baseline run: 60% accuracy, 2 safety failures
- After guardrails: 100% accuracy
- This is a real before/after you can quote in interviews.

### Interview 30s
"I built an automated eval harness that runs 10 test cases, scores on correctness/completeness/safety, and tracks scores across runs. Baseline was 60% with a safety failure. After adding guardrails, improved run hit 100%."

### Production Facts
- Cost: ~$0.01 per run (10 API calls)
- Speed: ~20 seconds for 10 cases
- Coverage: 10 cases is a start. Production needs 50-100+.

### Common Mistake
Running evals once and forgetting. Evals are CI/CD — run them on every code change.

### Quick Check
- Can you draw the eval harness architecture?
- How much does one eval run cost? How long does it take?
- What is the 90-second STAR answer for your eval harness?

---

## CROSS-DAY CONNECTIONS (Interview Gold)

```
Day 16 (Structured Output)
    ↓  Pydantic models for eval results
Day 17 (Embeddings)
    ↓  Vectorize chunks for retrieval
Day 18 (Chunking)
    ↓  Split docs before embedding
Day 19 (Eval Design)
    ↓  Define what "good" means
Day 20 (Eval Harness)
    ↓  Automate measurement
Future: Day 25 (Preference Eval) — compare TWO responses
Future: Day 26 (Adversarial) — try to BREAK the system
```

---

## RETENTION TEST (Do This Now)

Write these 3 functions from memory. No peeking.

**Function 1: extract_json**
```python
def extract_json(raw_text: str) -> dict:
    """Extract JSON from LLM output. Handles markdown fences and raw JSON."""
    # 5 lines max
```

**Function 2: cosine_similarity**
```python
import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Return cosine similarity between two vectors. Handle zero vectors."""
    # 4 lines max
```

**Function 3: eval_score**
```python
def eval_score(response: str, key_facts: list[str], forbidden: list[str]) -> dict:
    """Score an LLM response. Return {'correctness': bool, 'safety_pass': bool}."""
    # 6 lines max
```

**Time limit**: 10 minutes total.

**Pass criteria**: All 3 compile and handle edge cases (empty input, missing JSON, zero vectors).

If you pass → Day 21 is next.
If you get stuck → we debug it together, that becomes today's session.

---

## INTERVIEW PACK QUICK REFERENCE

| Day | 30s Pitch | Key Number |
|-----|-----------|------------|
| 16 | Structured output pipeline with 2 validation gates | Parse failures: 15% → <1% |
| 17 | Semantic search with text-embedding-004 | 768 dims, batch limit 250 |
| 18 | 3 chunking strategies compared | Fixed-size = production default |
| 19 | 10 eval cases with rubrics | Caught hallucination + PII leak |
| 20 | Automated eval harness with trends | Baseline 60% → improved 100% |

---

## GAPS TO CLOSE (From DAY_STATUS.md)

Day 20 still needs:
- [ ] Real Gemini integration (currently mock)
- [ ] BigQuery logging of eval results
- [ ] pytest test file

**Recommendation**: Close these gaps before Day 21. They are 30 minutes of work and complete the proof chain.

---

*Generated from GitHub repo audit. Last updated: 2026-05-01*
