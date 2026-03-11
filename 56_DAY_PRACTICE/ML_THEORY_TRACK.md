# 🧠 ML Fundamentals Track
## Parallel to 56-Day Plan — 30 min after main work

**Goal:** Master ML theory for interviews WITHOUT breaking your build schedule

---

## 📅 Integration Schedule

| Your Day | Main Focus | ML Theory (30 min after) |
|----------|-----------|---------------------------|
| Day 6 (today!) | Classes + OOP | Decision Trees intro |
| Day 7 | APIs | Decision Trees deep dive |
| Day 8-14 | GCP Week | Bias-Variance Tradeoff |
| Day 15-21 | RAG Core | Precision/Recall + ROC-AUC |
| Day 22-28 | RAG Production | Random Forests |
| Day 29-35 | RAGAS + Pipelines | Logistic Regression |
| Day 36-42 | MLOps | Neural Networks intro |
| Day 43-56 | Interview War Room | All topics review |

---

## 🎯 Priority Mapping (Interview-Weighted)

### MUST-KNOW (⭐⭐⭐⭐⭐) — Cover in Days 6-14

| Topic | Day | MLU-Explain Link | Interview Question |
|-------|-----|------------------|---------------------|
| Decision Trees | 6-7 | [Link](https://mlu-explain.github.io/decision-tree/) | "How does entropy decide splits?" |
| Bias-Variance | 8-9 | [Link](https://mlu-explain.github.io/bias-variance/) | "Draw the U-curve" |
| Precision/Recall | 10-11 | [Link](https://mlu-explain.github.io/precision-recall/) | "When prefer precision over recall?" |
| ROC-AUC | 12-13 | [Link](https://mlu-explain.github.io/roc-auc/) | "What's good AUC? 0.7 means?" |

### SHOULD-KNOW (⭐⭐⭐⭐) — Cover in Days 15-28

| Topic | Day | MLU-Explain Link | Interview Question |
|-------|-----|------------------|---------------------|
| Random Forests | 18-20 | [Link](https://mlu-explain.github.io/random-forest/) | "Why random features at splits?" |
| Logistic Regression | 22-24 | [Link](https://mlu-explain.github.io/logistic-regression/) | "Why sigmoid function?" |
| Cross-Validation | 25-27 | [Link](https://mlu-explain.github.io/cross-validation/) | "K-fold vs single split?" |

### NICE-TO-KNOW (⭐⭐⭐) — Cover in Days 29-42

| Topic | Day | MLU-Explain Link | Interview Question |
|-------|-----|------------------|---------------------|
| Neural Networks | 35-37 | [Link](https://mlu-explain.github.io/nn/) | "Explain backpropagation" |
| Linear Regression | 38-39 | [Link](https://mlu-explain.github.io/linear-regression/) | "OLS vs gradient descent" |
| Double Descent | 40-41 | [Link](https://mlu-explain.github.io/double-descent/) | "Why big models work" |

---

## 📋 Daily ML Routine

```
After main 4-hour block (around 11:30 AM):
├── Read MLU-Explain page (15 min)
├── Write 1-sentence summary in notes.md
├── Practice 1 interview question out loud
└── Move to next day
```

---

## ✅ Checkpoint System

| Checkpoint | Target Day | Topics Covered |
|------------|------------|----------------|
| CP1 | Day 14 | Decision Trees, Bias-Variance |
| CP2 | Day 28 | + Precision/Recall, Random Forests |
| CP3 | Day 42 | + Logistic Regression, Neural Networks |
| CP4 | Day 56 | All topics review + mock questions |

---

## 📁 Where to Save Notes

Create: `56_DAY_PRACTICE/ML_THEORY/notes.md`

Format per topic:
```markdown
## [Topic Name]

**Date:** Day X
**Resource:** MLU-Explain [Topic]

### 1-Sentence Summary
[Write your own - forces understanding]

### Key Formula
[Entropy = -Σp*log₂(p), etc.]

### Interview Answer Ready?
- [ ] Can explain in 2 min
- [ ] Can answer follow-up question
```

---

## 🎤 Punch Dialogues for ML Topics

Add to `INTERVIEW_PUNCH_DIALOGUES.md`:

### Decision Trees
> "A decision tree splits data based on features to maximize information gain — essentially asking 'what question separates the most data?' at each step. It's intuitive, interpretable, and serves as the foundation for Random Forests."

### Bias-Variance
> "The bias-variance tradeoff is the tension between underfitting and overfitting. Low bias = simple model (misses patterns), low variance = stable across datasets. The goal is the sweet spot that minimizes total error. That's why cross-validation is critical."

---

## 🔗 Links to All Resources

| # | Topic | URL |
|---|-------|-----|
| 1 | Decision Trees | https://mlu-explain.github.io/decision-tree/ |
| 2 | Random Forests | https://mlu-explain.github.io/random-forest/ |
| 3 | Neural Networks | https://mlu-explain.github.io/nn/ |
| 4 | Linear Regression | https://mlu-explain.github.io/linear-regression/ |
| 5 | Logistic Regression | https://mlu-explain.github.io/logistic-regression/ |
| 6 | Bias-Variance | https://mlu-explain.github.io/bias-variance/ |
| 7 | Precision & Recall | https://mlu-explain.github.io/precision-recall/ |
| 8 | ROC & AUC | https://mlu-explain.github.io/roc-auc/ |
| 9 | Cross-Validation | https://mlu-explain.github.io/cross-validation/ |
| 10 | Reinforcement Learning | https://mlu-explain.github.io/reinforcement-learning/ |
| 11 | Double Descent | https://mlu-explain.github.io/double-descent/ |

---

*Track created: Day 6 (2026-03-02)*
*Integration: Parallel to main 56-day plan*
