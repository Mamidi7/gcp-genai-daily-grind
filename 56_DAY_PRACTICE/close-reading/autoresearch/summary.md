# Autoresearch - Summary (Simple Terms)

---

## The Big Picture

Karpathy built a system where:
1. **AI agent** gets instructions (program.md)
2. **Agent modifies** one file (train.py)
3. **Runs training** for exactly 5 minutes
4. **Evaluates** val_bpb metric
5. **Keeps** if better, **discards** if worse
6. **Repeats** autonomously overnight

> "Leave the AI running while you sleep. Wake up to results."

---

## Key Concepts

### 1. val_bpb (Validation Bits Per Byte)

**What:** A metric to measure how well the model compresses text.

- Lower = better (like golf - minimize score)
- **Vocabulary-independent** - works for any vocab size

**Why it matters:** It's the "score" the AI tries to minimize.

---

### 2. Muon Optimizer

**What:** Custom optimizer that treats matrices differently.

- **Matrix parameters** (2D weights): Use Muon (orthogonalization)
- **Other parameters** (embeddings, scalars): Use AdamW

**Why:** Muon keeps weights "diverse" - prevents them from getting too similar.

```python
# Different LR for different parameter types
embedding_lr = 0.2      # Token embeddings
matrix_lr = 0.02        # Model weights (Muon)
scalar_lr = 0.5         # Per-layer scalars
```

---

### 3. RoPE (Rotary Position Embeddings)

**What:** Way to encode position in transformer models.

- Instead of adding position numbers to embeddings
- Rotate the vectors based on position
- **Benefits:** Works for any sequence length!

```python
# RoPE applies rotation to Q and K vectors
q = apply_rotary_emb(q, cos, sin)
k = apply_rotary_emb(k, cos, sin)
```

---

### 4. Sliding Window Attention

**What:** Don't attend to ALL previous tokens - only last N.

- **S = Short window** (half sequence length)
- **L = Long window** (full sequence length)

```python
WINDOW_PATTERN = "SSSL"  # Layer 0-2: short, Layer 3: long
```

**Why:** Faster, less memory, still captures long-range dependencies.

---

### 5. Value Embeddings (ResFormer)

**What:** Add learned "value" information to attention.

- Each layer can have optional value embeddings
- Gated - learned combination with regular values

```python
# Gate determines how much value embedding to add
gate = 2 * sigmoid(ve_gate(x))
v = v + gate * ve  # Residual-style addition
```

---

### 6. 5-Minute Time Budget

**Why fixed time?**
- Makes experiments comparable
- Forces efficiency
- Enables overnight runs

**What happens at 5 minutes?**
- Training stops immediately
- Final evaluation on validation set
- Results recorded

---

## The Experiment Loop

```
┌─────────────────────────────────────┐
│ 1. Read program.md (instructions)  │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ 2. Modify train.py (code changes)  │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ 3. Run 5-minute training           │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│ 4. Check val_bpb (score)           │
└─────────────────┬───────────────────┘
                  ↓
        ┌─────────┴─────────┐
        ↓                   ↓
   Improved?             Worse?
        ↓                   ↓
   Keep commit        Reset to start
        ↓                   ↓
        └─────↑─────↓───────┘
              │
         Repeat!
```

---

## Why This Matters for Krishna

### Interview Answer: "What's the future of ML?"

> "Autonomous experimentation. Karpathy's autoresearch shows AI can run hundreds of experiments overnight, iterating on model architecture, hyperparameters, and training strategies. The human provides ideas, the AI executes. This shifts our role from 'trainer' to 'researcher' - defining what to optimize, not how."

### Project Ideas for GCP

| Project | Description |
|---------|-------------|
| **AutoML on Vertex AI** | Build automated hyperparameter tuning |
| **Experiment Tracker** | Like W&B but with autonomous suggestions |
| **Overnight Training Pipeline** | Cloud Run + Vertex AI for batch experiments |

---

## Simple Code Patterns

### Learning Rate Schedule
```python
def get_lr_multiplier(progress):
    if progress < WARMUP_RATIO:
        return progress / WARMUP_RATIO  # Warmup
    elif progress < 1.0 - WARMDOWN_RATIO:
        return 1.0  # Steady
    else:
        return cooldown * FINAL_LR_FRAC  # Cooldown
```

### Gradient Accumulation
```python
# Large effective batch from small device batches
grad_accum_steps = TOTAL_BATCH_SIZE // (DEVICE_BATCH_SIZE * SEQ_LEN)
for micro_step in range(grad_accum_steps):
    loss = model(x, y)
    loss.backward()  # Accumulate gradients
```

---

## Key Takeaways

1. **Single-file focus** - Only train.py is editable (keeps things simple)
2. **Fixed time budget** - 5 minutes, always
3. **Clear metric** - val_bpb (lower = better)
4. **Autonomous loop** - No human needed after setup
5. **Simple > Complex** - Small improvements with ugly code aren't worth it

---

*Next: See `code-walkthrough.md` for deep dive into train.py*
