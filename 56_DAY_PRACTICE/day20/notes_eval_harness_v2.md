# Day 20 Notes - Eval Harness v2

Goal
- Build measurable quality checks for RAG answers.

What goes in
- Question
- Expected keywords
- Expected citation marker

What happens
- Score keyword overlap (simple precision proxy)
- Check if expected citation appears
- Decide pass/fail from thresholds

What comes out
- Pass rate
- Per-case failure reason

Why this matters in interviews
- Shows reliability mindset, not just generation demo.
- You can talk in metrics: pass rate and failure buckets.

30s answer
"I built an eval harness that checks keyword relevance and citation presence per test case, then reports pass rate and exact failure reason. This turned my RAG demo into a measurable system."

90s STAR
- S: I had a RAG demo but no reliability proof.
- T: Add objective quality checks before claiming readiness.
- A: I created EvalCase/EvalResult models, scoring functions, thresholds, and a report generator.
- R: I get pass/fail metrics plus failure reasons per case, so debugging and iteration are faster.
