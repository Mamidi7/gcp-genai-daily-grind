# ML Learning Resources 📚

Curated resources to master ML fundamentals for GCP AI/ML interviews.

---

## MLU-Explain Complete Collection (14 Interactive Topics)

All resources: [https://mlu-explain.github.io/](https://mlu-explain.github.io/)

---

### 1. Decision Trees 🌳
**URL:** https://mlu-explain.github.io/decision-tree/

**What it covers:**
- Farmer analogy (classifying tree trunks)
- Entropy & Information Gain (CORE MATH - memorize this!)
- ID3 algorithm
- Overfitting vs underfitting
- Gini impurity
- Links to Random Forests

**Interview Weight:** ⭐⭐⭐⭐⭐
> "How does information gain decide which feature to split on?"

---

### 2. Random Forests 🌲🌲🌲
**URL:** https://mlu-explain.github.io/random-forest/

**What it covers:**
- Ensemble learning (combine many models)
- Condorcet's Jury Theorem
- Bagging (Bootstrap Aggregating)
- Feature randomness for diversity
- Why diversity = stronger predictions

**Interview Weight:** ⭐⭐⭐⭐⭐
> "Why is random feature selection at each split important?"

---

### 3. Neural Networks 🧠
**URL:** https://mlu-explain.github.io/nn/

**What it covers:**
- Perceptrons & activation functions
- Forward propagation
- Backpropagation (the magic!)
- Gradient descent
- Layers & hidden units

**Interview Weight:** ⭐⭐⭐⭐⭐
> "Explain backpropagation in 2 minutes"

---

### 4. Linear Regression 📈
**URL:** https://mlu-explain.github.io/linear-regression/

**What it covers:**
- Fitting a line to data
- Ordinary Least Squares (OLS)
- Gradient descent vs closed-form
- R² & MSE metrics
- Regularization (Ridge/Lasso)

**Interview Weight:** ⭐⭐⭐⭐
> "What's the difference between Ridge and Lasso?"

---

### 5. Logistic Regression 🎯
**URL:** https://mlu-explain.github.io/logistic-regression/

**What it covers:**
- Sigmoid function
- Binary classification
- Log-odds & logit
- Cross-entropy loss
- Decision boundaries

**Interview Weight:** ⭐⭐⭐⭐⭐
> "Why do we use sigmoid function in logistic regression?"

---

### 6. The Bias-Variance Tradeoff ⚖️
**URL:** https://mlu-explain.github.io/bias-variance/

**What it covers:**
- Bias = oversimplification (underfitting)
- Variance = over-sensitivity (overfitting)
- Test error = bias² + variance + irreducible error
- The "sweet spot"
- LOESS & KNN examples

**Interview Weight:** ⭐⭐⭐⭐⭐
> "Draw the U-shaped bias-variance curve"

---

### 7. Precision & Recall 🎯📊
**URL:** https://mlu-explain.github.io/precision-recall/

**What it covers:**
- Confusion matrix
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 Score (harmonic mean)
- When to use which metric

**Interview Weight:** ⭐⭐⭐⭐⭐
> "When would you optimize for precision over recall?"

---

### 8. ROC & AUC 📈📐
**URL:** https://mlu-explain.github.io/roc-auc/

**What it covers:**
- True Positive Rate vs False Positive Rate
- Threshold selection
- AUC = Area Under Curve
- AUC = 0.5 (random) to 1.0 (perfect)
- Model comparison

**Interview Weight:** ⭐⭐⭐⭐
> "What's a good AUC score? What does AUC of 0.7 mean?"

---

### 9. Cross-Validation 🔄
**URL:** https://mlu-explain.github.io/cross-validation/

**What it covers:**
- K-Fold cross-validation
- Leave-one-out (LOOCV)
- Train/validation/test split
- Hyperparameter tuning
- Avoiding data leakage

**Interview Weight:** ⭐⭐⭐⭐
> "Why is k-fold CV better than a single train/test split?"

---

### 10. Reinforcement Learning 🎮
**URL:** https://mlu-explain.github.io/reinforcement-learning/

**What it covers:**
- Agent & Environment
- Rewards & Actions
- Policy optimization
- Q-learning basics
- Exploration vs Exploitation

**Interview Weight:** ⭐⭐⭐
> "What's the difference between model-based and model-free RL?"

---

### 11. Double Descent 📉📈
**URL:** https://mlu-explain.github.io/double-descent/

**What it covers:**
- Traditional bias-variance
- Modern double descent phenomenon
- interpolation regime
- Why bigger models can be better
- Neural network intuition

**Interview Weight:** ⭐⭐⭐
> "Why do very large neural networks generalize well?"

---

### 12. Train, Test, Validation Sets 📊
**URL:** https://mlu-explain.github.io/train-test-validation/

**What it covers:**
- Proper data splitting
- Validation set for tuning
- Test set for final evaluation
- Common ratios (80/20, 60/20/20)
- Data leakage prevention

**Interview Weight:** ⭐⭐⭐⭐

---

### 13. Equality of Odds ⚖️
**URL:** https://mlu-explain.github.io/equality-of-odds/

**What it covers:**
- Fairness in ML
- Protected attributes
- Equalized odds
- Demographic parity
- Ethics in AI

**Interview Weight:** ⭐⭐
> GCP BigQuery ML fairness considerations

---

### 14. Gradient Descent (implied) 🏔️
**Key concept used across all optimization topics**

**What it covers:**
- Learning rate
- Convergence
- Stochastic vs Batch vs Mini-batch
- Local minima
- Momentum

**Interview Weight:** ⭐⭐⭐⭐⭐

---

## 🎯 Priority Order for Your 45-Day Prep

| Priority | Topic | Why |
|----------|-------|-----|
| 1 | Bias-Variance, Decision Trees | Foundation |
| 2 | Precision/Recall, ROC-AUC | Most asked |
| 3 | Random Forests, Logistic Regression | Next level |
| 4 | Neural Networks, Linear Regression | Deep learning base |
| 5 | Cross-Validation, Double Descent | Pro topics |

---

## 🔗 Related GCP Topics

| MLU-Explain Topic | GCP Service |
|-------------------|-------------|
| Decision Trees | Vertex AI AutoML |
| Random Forests | BigQuery ML |
| Neural Networks | Vertex AI, TensorFlow |
| Linear/Logistic Regression | BigQuery ML |
| Precision/Recall | Vertex AI Model Evaluation |

---

## 🎯 Integration with Your 56-Day Plan

**File:** `ML_THEORY_TRACK.md` — Parallel schedule (30 min after main work)

**Today's Action (Day 6):**
- Finish Python day → then read Decision Trees (MLU-Explain)
- Write 1-sentence summary in `ML_THEORY/notes.md`

---

*Last Updated: Day 6 (2026-03-02)*
*Track: Parallel to main 56-day plan*
*Source: MLU-Explain Interactive Collection*
