# Autoresearch - Interview Punch Dialogues

---

## Q1: What is Karpathy's autoresearch?

> "Autoresearch is an AI system that autonomously runs LML training experiments. You give it a goal - minimize validation bits per byte - and it modifies the training code, runs 5-minute experiments, evaluates results, and iterates. One GPU can run ~12 experiments per hour, 100+ overnight while you sleep. It's a proof-of-concept for AI-driven ML research."

---

## Q2: What's the main metric and why?

> "The metric is val_bpb - validation bits per byte. Lower is better. It's vocabulary-independent, so you can compare models with different vocab sizes. It measures how well the model compresses text - essentially how good it is at predicting the next token."

---

## Q3: Explain the Muon optimizer.

> "Muon is a custom optimizer for 2D matrix parameters. It uses orthogonalization - keeps the weight matrices 'diverse' rather than letting them converge to similar patterns. For non-matrix parameters like embeddings, it uses regular AdamW. The key insight: different parameter types need different optimization strategies."

---

## Q4: What is sliding window attention?

> "Instead of attending to all previous tokens, sliding window only looks at the last N tokens - typically half the sequence length for 'short' windows. Layer 0-2 might use short windows for efficiency, while the final layer uses full attention. This reduces memory from O(n²) to O(n×w) where w is window size."

---

## Q5: How does RoPE work?

> "RoPE - Rotary Position Embeddings - encodes position by rotating the query and key vectors. Instead of adding position embeddings, we multiply by rotation matrices based on position. The beauty is it naturally extends to any sequence length - no need to train position embeddings up to the max length."

---

## Q6: What's the 5-minute time budget and why?

> "Fixed 5-minute budget per experiment. This makes results comparable across runs, forces efficient code, and enables overnight experimentation. The AI doesn't need to converge - it just needs to show improvement direction within 5 minutes. You can always run longer later."

---

## Q7: How does the autonomous loop work?

> "The AI modifies train.py, commits the change, runs training, checks val_bpb. If improved, it keeps the commit. If worse, it resets to the previous state. It repeats this indefinitely until stopped. No human needed after setup - it's a true autonomous research agent."

---

## Q8: What's the 'arena is the product' quote mean?

> "Karpathy's insight: design the right constraints and let the AI explore within them. The autoreloop is the product - it generates discoveries. We don't pre-specify the best architecture; we let experimentation find it. Our role shifts from implementer to question-asker."

---

## Q9: How would you build this on GCP?

> "I'd use Vertex AI Training with custom containers. Each experiment is a training job with a 5-minute timeout. Store results in BigQuery. Use Cloud Scheduler to run experiments overnight. For larger scale, use Vertex AI Vizier for hyperparameter search - it's Google's built-in AutoML solution."

---

## Q10: What's the future of ML engineering?

> "More autonomous. Like autoresearch shows, AI can iterate on model architecture and hyperparameters faster than humans. Engineers will define what to optimize and constrain the search space. The bottleneck shifts from 'running experiments' to 'formulating good questions.'"

---

## Quick Reference Table

| Question | One-Line Answer |
|----------|-----------------|
| What is autoresearch? | AI runs ML experiments autonomously |
| Main metric | val_bpb (lower = better) |
| Muon optimizer | Orthogonalization for matrix params |
| Sliding window | O(n×w) instead of O(n²) attention |
| RoPE | Rotary position embeddings |
| Time budget | 5 minutes per experiment |
| Future of ML | Autonomous experimentation |

---

## Story Answer Format

**Question:** "Tell me about a project that shows you understand AI trends."

> "I studied Karpathy's autoresearch - it's a system where AI runs its own ML experiments. The agent gets instructions, modifies training code, runs 5-minute experiments, and keeps improvements automatically. One GPU can do 100+ experiments overnight. It shows how ML engineering is shifting from manual training to defining constraints and letting AI explore. I want to build something similar on Vertex AI for my portfolio - automated hyperparameter tuning with experiment tracking."

---

*Thaggedhe Le — Relentless Execution*
