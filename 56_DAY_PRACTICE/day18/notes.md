# Day 18 Notes

## What I built today
- 3 chunking strategies: fixed-size, sentence-based, semantic
- Comparison engine that tests retrieval quality across strategies
- Sentence splitter with regex
- Semantic chunker that uses adjacent embedding similarity to detect topic boundaries

## Key concepts learned
1. **Fixed-size**: Simple, predictable, production default. Cuts sentences but overlap helps.
2. **Sentence-based**: Respects boundaries. Variable sizes. Better readability.
3. **Semantic**: Groups by meaning. Most expensive (needs embeddings). Best recall in theory.
4. **The real tradeoff**: chunk size controls precision vs recall tradeoff
   - Small chunks → precise retrieval but loses context
   - Large chunks → more context but more noise

## Error I hit
- Sentence splitter confused by abbreviations ("U.S.", "etc.")
- Semantic chunker created single-sentence chunks when threshold was too low
- Fixed-size chunking cut sentences mid-word

## Root cause
- Regex-based sentence splitting is fundamentally limited
- Similarity threshold is hyperparameter — no universal "right" value
- Fixed-size doesn't understand text structure

## Fix applied
- Added overlap to fixed-size to recover cut context
- Threshold tuning: start at 0.5, adjust based on results
- Sentence splitter handles most common cases, documented limitations

## Prevention added
- Always log chunk count, avg size, and size range
- Compare strategies before picking one for production
- Document tradeoff decision in README

## 90-second interview version
"I compared three chunking strategies for RAG retrieval: fixed-size with overlap, sentence-based grouping, and semantic chunking using embedding similarity. Fixed-size is the production default because it's predictable and fast. Sentence-based respects text boundaries. Semantic chunking had the best recall but adds embedding cost to the indexing pipeline. The key insight: chunk size is the most impactful hyperparameter — smaller chunks give better precision, larger chunks give better context."

## How this connects
- Day 18 = chunking (how to split before embedding)
- Day 17 = embeddings (how to vectorize the chunks)
- Day 21 = BigQuery Vector Search (production RAG using these chunks)
- Day 19-20 = eval (how to measure if chunking actually works)
