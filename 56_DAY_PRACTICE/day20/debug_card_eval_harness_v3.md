# Debug Card — eval_harness_v3.py

## Bug 1: Faithfulness false positive on short source context
- **Symptom**: `chunking_reason` fails faithfulness check even though answer is correct
- **Root cause**: Entity overlap heuristic uses capitalized words only. Source context has few capitalized words, so overlap ratio falls below 0.3 threshold
- **Fix**: Lower threshold to 0.2 OR also include lowercased noun extraction
- **Prevention**: Always test with real-length source contexts, not 1-sentence summaries
- **Impact**: False negatives in eval make you chase non-existent hallucination problems

## Bug 2: off_topic_france "I don't know" detection false positive
- **Symptom**: france test fails because answer contains "unknown" in citation field
- **Root cause**: `no_answer_detected()` regex matches "unknown" inside "Source: unknown" citation
- **Fix**: Strip citation lines before running no_answer check, or add word boundary `\bunknown\b`
- **Prevention**: Test regex-based detection against answers WITH citation lines

## Bug 3: edge_case_empty expected to fail (by design)
- **Symptom**: All metrics fail for question not in answer bank
- **Root cause**: This is INTENTIONAL — model returns "I don't know" for answerable Q
- **Fix**: This is the eval working correctly — catching a real failure mode
- **Impact**: Proves the harness catches when RAG has no retrieval result for a valid question
