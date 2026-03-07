# 📅 DAY 12: REINFORCEMENT LEARNING INTRODUCTION

## 🎯 Today's Mission

**Main Topic:** RL Fundamentals
**Why:** Anthropic hired 65+ RL engineers. RL = how agents improve from feedback.

---

## 🧠 Core RL Concepts (Study 30 min)

**Resource:** Andrej Karpathy — "Neural Networks: Zero to Hero" RL video (YouTube)

### The RL Loop:
```
Agent → Action → Environment → Reward → Agent (learns)
```

### Key Terms:
| Term | Meaning |
|------|---------|
| **State (S)** | Current situation |
| **Action (A)** | What agent does |
| **Reward (R)** | Feedback (+1 good, -1 bad) |
| **Policy (π)** | Strategy: S → A |
| **Q-Value** | Expected future reward |

---

## 🔥 RL in LLM Context

### RLHF (Reinforcement Learning from Human Feedback)
- Human rates AI responses
- AI learns what humans prefer
- Used to make Claude/GPT safe & helpful

### DPO (Direct Preference Optimization)
- Newer, simpler than RLHF
- Directly optimizes from preference data
- Anthropic uses this!

### Agentic RL
- Agent takes actions in environment
- Gets rewards for good decisions
- Learns to improve over time

---

## 🛠️ Hands-On: Understand RLHF

**Task:** Read about RLHF in 10 minutes

**Resource:** Hugging Face docs — "RLHF" (huggingface.co/docs/transformers/en/reinforcement_learning)

**Key insight:**
```
RLHF = Reward Model + Proximal Policy Optimization (PPO)
- Step 1: Train reward model from human feedback
- Step 2: Use PPO to optimize LLM using reward model
```

---

## 🏭 Industry Standard: Real-World RL Agents (GOLD STANDARD)

*Researched: March 7, 2026*

### 1. KARL (Databricks) - The Gold Standard

**What:** Knowledge Agents via Reinforcement Learning - enterprise RAG agent that beats Claude 4.6 & GPT-4.2

**Training Approach:**
| Phase | Technique |
|-------|-----------|
| **Data** | Synthetic data generation (not human-labeled) |
| **RL Algorithm** | OAPL (Optimal Advantage-based Policy Optimization) |
| **Training** | Multi-task RL across 6 search behaviors |
| **Iterations** | Up to 3 rounds with data regeneration |

**Key Innovation - Synthetic Data Pipeline:**
```
Stage 1: Question-Answer Synthesis
  → Agent explores corpus with vector search
  → Generates Q&A pairs

Stage 2: Solution Generation + Filtering
  → Multiple solver agents generate answers
  → Pass-rate filtering removes trivial/impossible questions
  → Deduplication against evaluation sets
```

**Performance Results:**
| Metric | Value |
|--------|-------|
| Matches | Claude 4.6, GPT-4.2 |
| Cost/query | <$0.10 (33% lower than Claude Opus 4.6) |
| Latency | 47% lower than Claude Opus 4.6 |
| Out-of-distribution | Generalizes to FreshStack, FinanceBench |

**The 6 Search Behaviors KARL Mastered:**
1. Constraint-driven entity search
2. Cross-document synthesis
3. Tabular reasoning
4. Exhaustive entity retrieval
5. Procedural reasoning
6. Fact aggregation

**Why This Matters for GCP:**
- Shows how to train agents that beat frontier models
- Synthetic data = scalable training (few thousand GPU hours)
- Enterprise RAG is the killer use case

---

### 2. OpenAI Operator / Deep Research

**What:** Agent that uses browser autonomously to complete tasks

**Training Approach:**
- **RL Fine-tuning** with grader-based feedback
- **Process reward models** for multi-step tasks
- **Browser automation** as action space

**Key Concept:** Reinforcement Fine-tuning (RFT)
```
For each prompt:
1. Sample multiple responses
2. Score with grader model
3. Apply policy-gradient updates
4. Repeat until convergence
```

---

### 3. Google Gemini Enterprise Agents

**What:** Prebuilt agents for customer service, shopping, productivity

**Training:**
- Built on Gemini models
- Agent Builder (no-code tool)
- Data grounding + security focus

**GCP Connection:**
- Vertex AI Agent Builder
- Enterprise-grade security controls
- Data sovereignty support

---

## 📝 Interview Talking Points

> "I understand RLHF — it's how Claude/GPT learn from human feedback. Anthropic is hiring heavily for RL engineers, and I see RLHF becoming standard in production AI systems."

> "The cutting edge is using RL to train agents on synthetic data — Databricks' KARL beats Claude 4.6 at 33% lower cost. They use a 2-stage pipeline: Q&A synthesis + solution filtering, then OAPL for multi-task RL. This is how enterprise agents will be built."

---

## ✅ Checkpoint

- [ ] Can explain: State, Action, Reward, Policy
- [ ] Understand RLHF concept
- [ ] Know DPO is newer/better than RLHF
- [ ] See connection: RL → Agents → Self-improving AI
- [ ] Know KARL training approach (synthetic data + OAPL)
- [ ] Can explain 6 search behaviors enterprise agents need
