# Exercise 8: Embedding Cache + Vector DB Fallback Chain

## Goal (one line)
Build a retrieval system that checks a Redis cache first, falls back to a vector DB, and falls back again to a web search.

## Why This Matters
Interview question: "Your RAG system is slow. How do you speed it up?"
Bad: "I use a faster model."
Good: "I cache embedding results in Redis (5ms lookup). Cache hit = instant response.
Cache miss → vector search in BigQuery (50ms). That fails → web search fallback (2s).
95% of queries hit cache. Total p99: 50ms instead of 2 seconds."

## Architecture

```
User Query: "What is Vertex AI?"
         │
         ▼
┌─────────────────┐
│ Step 1: Redis    │ ──→ Cache HIT  → Return cached answer (5ms)
│ Embedding Cache  │     (key = hash of query embedding)
└────────┬────────┘
         │ Cache MISS
         ▼
┌─────────────────┐
│ Step 2: Vector   │ ──→ Found results → Rank + Return (50ms)
│ DB (BigQuery     │     (VECTOR_SEARCH with cosine similarity)
│ VECTOR_SEARCH)   │
└────────┬────────┘
         │ No good results (similarity < threshold)
         ▼
┌─────────────────┐
│ Step 3: Web      │ ──→ Search → Scrape → Answer (2000ms)
│ Search Fallback  │     (only used for novel queries)
└────────┬────────┘
         │ Web search also fails
         ▼
┌─────────────────┐
│ Step 4: Fallback │ ──→ "I don't have information on that topic."
│ Response         │     (honest failure, not hallucination)
└─────────────────┘
```

## What You Build

### 1. Retrieval Chain (`retrieval_chain.py`)
```python
class RetrievalChain:
    async def query(self, prompt: str) -> dict:
        # Step 1: Check Redis cache
        cached = await self.redis_get(prompt)
        if cached and cached["confidence"] > 0.85:
            return {**cached, "source": "cache"}

        # Step 2: Vector search
        results = await self.vector_search(prompt, top_k=5)
        if results and results[0]["similarity"] > 0.7:
            await self.redis_set(prompt, results[0])  # populate cache
            return {**results[0], "source": "vector_db"}

        # Step 3: Web search fallback
        web_result = await self.web_search(prompt)
        if web_result:
            await self.redis_set(prompt, web_result)  # populate cache
            return {**web_result, "source": "web_search"}

        # Step 4: Honest failure
        return {"answer": None, "source": "fallback", "confidence": 0}
```

### 2. Redis Cache Layer
```python
# Key: SHA256(query)[:16]
# Value: JSON {answer, source, confidence, timestamp, tokens_used}
# TTL: 24 hours (stale answers expire)
```

### 3. Metrics
- cache_hit_rate, vector_db_hit_rate, web_search_rate, fallback_rate
- Track per-source latency

## Common Mistake
Caching the raw query text instead of the embedding.
Why bad: "What is Vertex AI?" and "Tell me about Vertex AI" are the same intent
but different text. They'd be separate cache entries.
Fix: Cache by embedding hash (similar embeddings = same cache entry).

## Check Question
Why is the fallback chain ordered this way (cache → vector DB → web → fail)?
(Answer: ordered by speed + cost. Cache is 5ms and free.
Vector DB is 50ms and cheap. Web search is 2s and expensive.
Fail is instant and honest.)

## Tiny Exercise
1. Start Redis: `docker run -d -p 6379:6379 redis:7-alpine`
2. Run retrieval_chain.py
3. First query = cache miss (vector DB hit)
4. Same query again = cache hit (notice the speed difference)
5. Query something weird = web search or fallback
6. Check metrics: what's your cache hit rate after 20 queries?
