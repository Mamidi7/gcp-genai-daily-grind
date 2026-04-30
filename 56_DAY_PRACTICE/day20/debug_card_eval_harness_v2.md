# Debug Card - Day 20 Eval Harness v2

Symptom
- Early run gave false pass even when answer quality was weak.

Root cause
- Citation check was too loose in older logic and thresholds were not explicit.

Fix
- Added explicit min_keyword_score per case.
- Added citation_ok check as mandatory pass condition.
- Added failure_reason text to make misses visible.

Prevention
- Keep thresholds in test case config, not hardcoded in scoring function.
- Always print per-case detail lines, not only aggregate pass rate.

Impact
- Prevents overclaiming quality based on a single aggregate metric.
