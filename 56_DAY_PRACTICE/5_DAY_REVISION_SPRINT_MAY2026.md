# 5-Day Revision Sprint — May 2026

> **Created:** April 30, 2026
> **Start:** May 1, 2026
> **Goal:** Revive everything you learned (Days 1-20), fill gaps, get interview-confident
> **Constraint:** Zero-cost. Health-first pace. 2-3 hours/day max.

---

## The Problem

You completed Days 1-20 solidly (Python, FastAPI, GCP, RAG, Embeddings, Eval).
Then a health emergency paused everything for ~4 weeks.
Now you need to: revive the knowledge, fill gaps, and get back to building.

## The Strategy

Don't re-read everything. Don't start from Day 1.
Instead: **Quiz → Find gaps → Fix gaps → Practice explaining → Move on.**

```
DAY 1 (May 1):  Python + FastAPI Revival
DAY 2 (May 2):  GCP Services + BigQuery SQL Revival
DAY 3 (May 3):  RAG + Embeddings + Chunking Revival
DAY 4 (May 4):  Eval + Agent + Guardrails Revival
DAY 5 (May 5):  Full System Walkthrough + Interview Practice
```

---

## DAY 1 (May 1): Python + FastAPI Revival

### Morning Block (90 min)

**Step 1: Warm-up Quiz — 15 questions (30 min)**

Answer these WITHOUT looking at notes. Write answers in a file.

| # | Question |
|---|----------|
| 1 | What is the difference between a list and a tuple? When would you use each? |
| 2 | Write a list comprehension that filters even numbers from [1,2,3,4,5,6] |
| 3 | What does `*args` do? What does `**kwargs` do? |
| 4 | What is a decorator? Write a simple `@timer` decorator. |
| 5 | What is the difference between `==` and `is`? |
| 6 | What does `yield` do? How is it different from `return`? |
| 7 | Explain `try/except/finally` — what runs when? |
| 8 | What is a context manager? Why use `with open()`? |
| 9 | What is the difference between `deepcopy` and assignment? |
| 10 | Write a function that takes a dict and returns sorted keys. |
| 11 | In FastAPI, what does `@app.post("/chat")` do? |
| 12 | What is Pydantic? Why do we use it with FastAPI? |
| 13 | What HTTP status codes mean: 200, 400, 404, 422, 500, 502, 503? |
| 14 | What is the difference between `async def` and `def` in FastAPI? |
| 15 | How do you test a FastAPI endpoint? (write the test pattern) |

**Step 2: Check answers against your cheat sheet (15 min)**
- File: `56_DAY_PRACTICE/INTERVIEW_CHEAT_SHEET.md`
- File: `56_DAY_PRACTICE/REVISION_PYTHON.md`
- Mark what you got wrong — those are your gaps

**Step 3: Run your Day 12 FastAPI app (45 min)**
```bash
cd 56_DAY_PRACTICE/day12
cat main.py          # Read it. Understand every line.
python -m pytest test_main.py -v   # Run the tests
```
For each endpoint, explain to yourself:
- What goes IN (request body)
- What happens INSIDE (validation, logic, error handling)
- What comes OUT (response shape)

### Afternoon Block (60 min)

**Step 4: Run your Day 13 Validation app (30 min)**
```bash
cd 56_DAY_PRACTICE/day13
cat main.py
python -m pytest test_main.py -v   # Should be 13/13 pass
```

**Step 5: Interview practice — say out loud (30 min)**
Tell this STAR story to an imaginary interviewer (use your phone recorder):

> **S:** Building FastAPI + Gemini endpoint for a RAG app
> **T:** Make it production-safe — no crashes on bad input
> **A:** Added Pydantic validation, custom error handler, retry + timeout wrapper
> **R:** 13/13 tests pass. Invalid inputs fail fast with 422. Clean 502 on upstream failures.

**Deliverable:** Create file `revision_sprint/day1_answers.md` with quiz answers + gaps found.

---

## DAY 2 (May 2): GCP Services + BigQuery SQL Revival

### Morning Block (90 min)

**Step 1: GCP Services Quiz — 10 questions (30 min)**

| # | Question |
|---|----------|
| 1 | Cloud Run vs Cloud Functions — when to use which? |
| 2 | What is WIF (Workload Identity Federation)? Why is it better than service account keys? |
| 3 | What are the 3 storage classes in Cloud Storage? When to use each? |
| 4 | What is IAM? Explain a role, a policy, and a binding. |
| 5 | What is Vertex AI? Name 3 things you can do with it. |
| 6 | What is BigQuery? How is it different from a regular database? |
| 7 | How does Cloud Run auto-scaling work? Scale to zero? |
| 8 | What is Pub/Sub? When would you use it? |
| 9 | What is Eventarc? How does it relate to Cloud Functions? |
| 10 | Explain: GCS upload triggers processing. Draw the architecture. |

**Step 2: Check answers (15 min)**
- File: `56_DAY_PRACTICE/REVISION_GCP.md`
- File: `56_DAY_PRACTICE/INTERVIEW_CHEAT_SHEET.md` → GCP section

**Step 3: BigQuery SQL practice (45 min)**

Write these 5 queries (on paper or in a file). Use BigQuery public dataset if available.

```sql
-- 1. Window function: Rank products by sales within each category
-- 2. CTE: Find top 10 customers who bought the most in last 30 days
-- 3. UNNEST: Split comma-separated tags and count each tag
-- 4. PARTITION BY: Query only last 7 days of data (cost optimization)
-- 5. JOIN debug: Find orders with no matching customer (LEFT JOIN + IS NULL)
```

### Afternoon Block (60 min)

**Step 4: Read your Cloud Run deployment notes (30 min)**
```bash
cat 56_DAY_PRACTICE/day10_cloud_storage/README.md
```
Remind yourself: How did you deploy? What worked? What failed?

**Step 5: Interview practice — say out loud (30 min)**

> **GCP Hero Story:**
> "I deployed a FastAPI + Gemini service to Cloud Run using WIF for auth — zero API keys in code. It auto-scales to zero when idle, so cost stays minimal. I used GCS for document storage and BigQuery for analytics."

**Deliverable:** `revision_sprint/day2_answers.md` with quiz answers + SQL queries.

---

## DAY 3 (May 3): RAG + Embeddings + Chunking Revival

### Morning Block (90 min)

**Step 1: RAG + Embeddings Quiz — 12 questions (30 min)**

| # | Question |
|---|----------|
| 1 | What is RAG? Why not just use a raw LLM? |
| 2 | Draw the RAG pipeline: User Query → ... → Answer |
| 3 | What are embeddings? What dimension does text-embedding-004 produce? |
| 4 | What is cosine similarity? Write the formula conceptually. |
| 5 | What is the difference between keyword search and vector search? |
| 6 | Name 3 chunking strategies. Which one preserves context best? |
| 7 | What is a chunk overlap? Why is it needed? |
| 8 | What happens if chunks are too small? Too large? |
| 9 | What is hybrid retrieval? (keyword + vector) |
| 10 | What is a citation in RAG? Why does it matter? |
| 11 | What is a "no-answer" response? When should RAG say "I don't know"? |
| 12 | How do you measure retrieval quality? |

**Step 2: Check answers (15 min)**
- File: `56_DAY_PRACTICE/REVISION_AI_LLM.md`
- File: `56_DAY_PRACTICE/INTERVIEW_CHEAT_SHEET.md` → AI section

**Step 3: Read your Day 16-18 code (45 min)**
```bash
cat 56_DAY_PRACTICE/day16/solution.py    # Structured output
cat 56_DAY_PRACTICE/day17/solution.py    # Embeddings + cosine similarity
cat 56_DAY_PRACTICE/day18/solution.py    # Chunking strategies
```
For each file: What goes in? What happens inside? What comes out?

### Afternoon Block (60 min)

**Step 4: Draw the RAG architecture (30 min)**

Draw this on paper or type it out:
```
User Query
    |
    v
[FastAPI /chat endpoint]
    |
    v
[Input Validation] -- Pydantic checks query
    |
    v
[Retrieval Layer]
    |
    +---> [Keyword Search]  -- BM25 / simple match
    +---> [Vector Search]   -- cosine similarity on embeddings
    |
    v
[Context Builder] -- top-K chunks + citations
    |
    v
[Gemini API] -- prompt = context + query + "cite sources"
    |
    v
[Response Validation] -- grounded? citations present?
    |
    v
Answer to User
```

For each box, write one sentence: "What fails here? How do I detect it?"

**Step 5: Interview practice (30 min)**

> **RAG Hero Story:**
> "I built a hybrid RAG system combining keyword and vector search. I tested 3 chunking strategies — sentence-boundary gave 40% better retrieval than fixed-size because it preserved context boundaries. My eval harness caught 3 hallucinations in testing."

**Deliverable:** `revision_sprint/day3_answers.md` + RAG architecture diagram.

---

## DAY 4 (May 4): Eval + Agent + Guardrails Revival

### Morning Block (90 min)

**Step 1: Eval + Agent Quiz — 10 questions (30 min)**

| # | Question |
|---|----------|
| 1 | What is an eval harness? Why can't you ship without one? |
| 2 | What metrics does RAGAS measure? Name 3. |
| 3 | What is "Faithfulness" in RAG eval? |
| 4 | What is "LLM-as-judge"? How is it different from automated metrics? |
| 5 | What is an AI agent? How is it different from a simple API call? |
| 6 | Draw the agent loop: Observe → Think → Act → ... |
| 7 | What are agent guardrails? Name 3 types. |
| 8 | What is a max_iterations limit? Why is it needed? |
| 9 | What is tool validation? Why whitelist allowed functions? |
| 10 | What happens if an agent gets stuck in a loop? |

**Step 2: Check answers (15 min)**
- File: `56_DAY_PRACTICE/REVISION_AI_LLM.md`
- Your Day 19-20 eval harness code

**Step 3: Read your eval code (45 min)**
```bash
cat 56_DAY_PRACTICE/day19/solution.py    # Eval intro
cat 56_DAY_PRACTICE/day20/solution.py    # Eval harness v1
```
Understand: How does scoring work? What's the trend tracking?

### Afternoon Block (60 min)

**Step 4: Agent guardrails exercise (30 min)**

Write pseudocode (or real code) for an agent with 3 safety layers:
```python
MAX_ITERATIONS = 5
TIMEOUT_PER_TOOL = 10  # seconds
ALLOWED_TOOLS = {"search_docs", "query_bigquery", "call_gemini"}

def agent_loop(query):
    for i in range(MAX_ITERATIONS):
        # 1. Think: what tool to call?
        tool_name, tool_args = think(query)
        # 2. Validate tool
        if tool_name not in ALLOWED_TOOLS:
            return safe_fallback("Tool not allowed")
        # 3. Execute with timeout
        result = execute_with_timeout(tool_name, tool_args, TIMEOUT_PER_TOOL)
        # 4. Check if done
        if is_final_answer(result):
            return result
    return safe_fallback("Max iterations reached")
```

**Step 5: Interview practice (30 min)**

> **Agent + Eval Hero Story:**
> "I built an eval harness that scores RAG answers on 10 Q&A pairs. It caught 3 hallucinations where the model made up facts not in the source docs. I fixed this by raising the similarity threshold and adding citation enforcement. Re-ran eval — hallucinations dropped to zero."

**Deliverable:** `revision_sprint/day4_answers.md` + agent guardrails code.

---

## DAY 5 (May 5): Full System Walkthrough + Interview Practice

### Morning Block (90 min)

**Step 1: Full system walkthrough — explain everything (60 min)**

Set a 3-minute timer. Explain your ENTIRE system out loud:

```
START:
"I'm a banking ETL engineer who built production AI systems on GCP."

FASTAPI:
"I built a FastAPI service with Pydantic validation, deployed on Cloud Run.
13/13 tests pass. Invalid inputs fail fast with 422.
Upstream failures return clean 502, not stack traces."

RAG:
"I built hybrid RAG — keyword + vector search.
Tested 3 chunking strategies. Sentence-boundary gave best results.
Eval harness with 10 Q&A pairs catches hallucinations."

GCP:
"Deployed using WIF — zero API keys.
GCS for docs, BigQuery for analytics, Vertex AI for embeddings.
Cloud Run auto-scales to zero for cost optimization."

AGENT:
"Added agent loop with 3 guardrails:
iteration limit, tool whitelist, per-call timeout.
Every step is logged as structured JSON."

EVAL:
"Built scoring pipeline with trend tracking.
Catches when retrieval quality drops.
Production monitoring thinking."

CLOSE:
"Everything is on GitHub. Real code, real tests, real debugging evidence."
```

**Step 2: Identify remaining gaps (30 min)**
- What couldn't you explain well?
- What felt shaky?
- Write those down — those become your next builds

### Afternoon Block (90 min)

**Step 3: Mock interview — Claude plays interviewer (45 min)**

I will ask you:
1. "Tell me about yourself" (2 min)
2. "Explain your RAG system architecture" (3 min)
3. "What's the hardest bug you've debugged?" (90 sec STAR)
4. "Why Cloud Run over GKE?" (1 min)
5. "How do you evaluate LLM output quality?" (2 min)
6. "Write a function that chunks text with overlap" (live code)
7. "How would you detect hallucinations in production?" (2 min)
8. "Tell me about a time you handled a production failure" (90 sec STAR)

**Step 4: Final commit + plan next steps (45 min)**
1. Commit all revision sprint artifacts
2. Push to GitHub (restart your green streak!)
3. Based on gaps found, pick your next build:
   - If agent was weak → Day 21 (LangGraph)
   - If eval was weak → Day 25 (Preference eval)
   - If deployment was weak → Day 23 (CI/CD)
   - If system design was weak → Day 9 practice

---

## Daily Checklist

At the end of EACH day, check these:

- [ ] Quiz completed (no peeking at notes first)
- [ ] Gaps identified and written down
- [ ] Code re-read and understood (not just skimmed)
- [ ] STAR story practiced OUT LOUD (not just in head)
- [ ] Artifact saved to `revision_sprint/` folder
- [ ] One commit pushed to GitHub

---

## What Happens After Day 5

You'll have:
- ✅ Revived Python + FastAPI knowledge
- ✅ Revived GCP service understanding
- ✅ Revived RAG + Embeddings + Eval understanding
- ✅ 3 polished hero STAR stories
- ✅ A gap list showing exactly what to build next
- ✅ GitHub green streak restarted
- ✅ Interview confidence back

Then we resume the Day 21+ build plan with fresh energy.

---

## Folder Structure

```
56_DAY_PRACTICE/revision_sprint/
├── day1_answers.md      # Python + FastAPI quiz + gaps
├── day2_answers.md      # GCP + BigQuery quiz + SQL
├── day3_answers.md      # RAG + Embeddings quiz + architecture
├── day4_answers.md      # Eval + Agent quiz + guardrails code
├── day5_walkthrough.md  # Full system explanation + mock notes
└── GAP_LIST.md          # Prioritized gaps to fix after sprint
```

---

*Thaggedhe Le. Health comes first. Then we build.*
*You've already done the hard part (Days 1-20). Now we revive it.*
