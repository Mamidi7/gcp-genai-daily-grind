# Next 15 Days Rich Context Playbook (Day 16-30)

Use with `COMING_DAYS_INDUSTRY_GRADE_TRACK.md` and each `dayXX/README.md`.

## How to run each day

- Build block: implement one working component.
- Failure block: intentionally trigger one realistic failure.
- Debug block: isolate root cause and patch.
- Interview block: speak your 90-second story out loud.

## Day 16: API Reliability
- Business context: checkout assistant calls external LLM API; outages hurt conversion.
- Build: timeout + retry with exponential backoff.
- Simulate failure: API timeout and 429 rate limit.
- Interview proof: "I improved resilience under transient failures."

## Day 17: Structured Logging
- Business context: support team cannot triage incidents quickly.
- Build: structured JSON logs with request_id and error_type.
- Simulate failure: malformed payload causing 500.
- Interview proof: "I reduced mean-time-to-debug via structured telemetry."

## Day 18: Data Contracts
- Business context: bad input breaks pipeline silently.
- Build: schema validation before processing.
- Simulate failure: missing required field and wrong datatype.
- Interview proof: "I moved failures earlier using contract checks."

## Day 19: Batch Pipeline Skeleton
- Business context: nightly demand signal pipeline for recommendations.
- Build: extract -> transform -> load stages with checkpoints.
- Simulate failure: partial write or duplicate batch run.
- Interview proof: "I designed restart-safe pipeline stages."

## Day 20: Incremental Load
- Business context: full refresh too expensive and slow.
- Build: watermark-based incremental load + late-arrival lookback.
- Simulate failure: watermark corruption.
- Interview proof: "I balanced freshness and cost with incremental design."

## Day 21: DQ + SLA
- Business context: trust in analytics is dropping.
- Build: null/duplicate/late-data checks and pass/warn/fail status.
- Simulate failure: sudden spike in late data.
- Interview proof: "I introduced measurable data reliability gates."

## Day 22: RAG Ingestion
- Business context: support bot gives stale/irrelevant answers.
- Build: chunking with metadata and source tracking.
- Simulate failure: over-large chunks reducing retrieval precision.
- Interview proof: "I improved retrievability by optimizing ingestion strategy."

## Day 23: Retrieval Evaluation
- Business context: bot accuracy uncertain; no eval process.
- Build: simple benchmark with precision@k and failure labels.
- Simulate failure: top-k retrieves wrong domain docs.
- Interview proof: "I built measurable retrieval evaluation before scaling."

## Day 24: Prompt Robustness
- Business context: prompt injection and policy bypass risks.
- Build: instruction hierarchy and content filtering.
- Simulate failure: adversarial prompt trying to bypass rules.
- Interview proof: "I hardened prompt layer against common attacks."

## Day 25: Tool-Calling Agent
- Business context: user tasks require calculation/search/tool chaining.
- Build: tool registry and safe invocation rules.
- Simulate failure: wrong tool selection loop.
- Interview proof: "I constrained agent behavior for predictable execution."

## Day 26: Feature Dataset Safety
- Business context: training leakage gives fake performance gains.
- Build: point-in-time safe joins.
- Simulate failure: accidental future feature leakage.
- Interview proof: "I enforced leakage-safe feature generation."

## Day 27: Model Baseline
- Business context: team has no baseline to compare improvements.
- Build: baseline model + clear metric report.
- Simulate failure: class imbalance distorting accuracy.
- Interview proof: "I chose metrics aligned to business risk."

## Day 28: Model Serving API
- Business context: model works offline, fails in serving path.
- Build: prediction API with strict request validation and fallbacks.
- Simulate failure: invalid schema and missing features.
- Interview proof: "I closed train-serve gap with strict contracts."

## Day 29: Monitoring + Drift
- Business context: quality drops in production unnoticed.
- Build: drift checks + latency/error dashboards.
- Simulate failure: feature distribution shift.
- Interview proof: "I added early warning signals for model decay."

## Day 30: Postmortem + Portfolio
- Business context: leadership wants repeatable engineering, not hero debugging.
- Build: postmortem with timeline, root cause, actions, and owner.
- Simulate failure: missed alert due to poor threshold.
- Interview proof: "I turned incidents into process improvements."

## Minimum evidence to keep each day

- 1 code snippet or query
- 1 captured error log
- 1 root-cause note
- 1 fix commit or patch
- 1 prevention action
- 1 spoken interview answer

## End of Day 30 package

- System diagram
- 10+ debug cards
- 2 postmortems
- 1 metrics summary table
- 1 portfolio README

This package gives you credible, discussion-ready evidence in interviews.
