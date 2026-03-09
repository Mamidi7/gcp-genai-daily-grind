# Autoresearch - Code Walkthrough (train.py)

---

## Overview

`train.py` is the **only file** the AI agent can modify. Contains:
- GPT model architecture
- Muon optimizer
- Training loop
- Hyperparameters

---

## Section 1: Configuration

```python
@dataclass
class GPTConfig:
    sequence_len: int = 2048
    vocab_size: int = 32768
    n_layer: int = 12
    n_head: int = 6
    n_kv_head: int = 6
    n_embd: int = 768
    window_pattern: str = "SSSL"
```

**Key insight:** Simple config dataclass. Easy for AI to modify.

---

## Section 2: Model Architecture

### GPT Model
```python
class GPT(nn.Module):
    def __init__(self, config):
        self.transformer = nn.ModuleDict({
            "wte": nn.Embedding(config.vocab_size, config.n_embd),  # Token embeddings
            "h": nn.ModuleList([Block(config, i) for i in range(config.n_layer)]),  # Layers
        })
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)  # Output
```

**Key insight:** Standard transformer - embedding + layers + output projection.

### Attention (CausalSelfAttention)
```python
class CausalSelfAttention(nn.Module):
    def __init__(self, config, layer_idx):
        self.c_q = nn.Linear(self.n_embd, self.n_head * self.head_dim, bias=False)
        self.c_k = nn.Linear(self.n_embd, self.n_kv_head * self.head_dim, bias=False)
        self.c_v = nn.Linear(self.n_embd, self.n_kv_head * self.head_dim, bias=False)
        self.c_proj = nn.Linear(self.n_embd, self.n_embd, bias=False)
```

**Key insight:** Separate Q, K, V projections. No bias vectors (common in modern transformers).

### RoPE Application
```python
def apply_rotary_emb(x, cos, sin):
    x1, x2 = x[..., :d], x[..., d:]
    y1 = x1 * cos + x2 * sin
    y2 = x1 * (-sin) + x2 * cos
    return torch.cat([y1, y2], 3)
```

**Key insight:** RoPE is applied to Q and K before attention. Rotate based on position.

### MLP
```python
class MLP(nn.Module):
    def forward(self, x):
        x = self.c_fc(x)           # Expand: n_embd → 4*n_embd
        x = F.relu(x).square()     # GELU approximation
        x = self.c_proj(x)          # Contract: 4*n_embd → n_embd
```

**Key insight:** Uses `relu().square()` instead of GELU - faster approximation!

---

## Section 3: Optimizer Setup

### Learning Rate Scaling
```python
def setup_optimizer(self, ...):
    dmodel_lr_scale = (model_dim / 768) ** -0.5
    # Scale LR inversely proportional to sqrt(model_dim)
```

**Key insight:** Larger models need smaller learning rates (classical scaling law).

### Muon for Matrices
```python
# Muon for 2D parameters (weight matrices)
# AdamW for everything else (embeddings, scalars)
param_groups = [
    dict(kind='adamw', params=embedding_params, lr=embedding_lr ...),
    dict(kind='muon', params=matrix_params, lr=matrix_lr ...),
]
```

---

## Section 4: Training Loop

### Gradient Accumulation
```python
grad_accum_steps = TOTAL_BATCH_SIZE // (DEVICE_BATCH_SIZE * SEQ_LEN)

for micro_step in range(grad_accum_steps):
    loss = model(x, y)
    loss = loss / grad_accum_steps
    loss.backward()  # Accumulate gradients
```

**Key insight:** Simulate large batch size on limited GPU memory.

### Time Budget
```python
while total_training_time < TIME_BUDGET:
    # Train for exactly 5 minutes
    # Then evaluate and stop
```

### Loss Monitoring
```python
# Exponential moving average for smooth loss
smooth_train_loss = ema_beta * smooth_train_loss + (1 - ema_beta) * train_loss_f

# Abort if loss explodes
if train_loss_f > 100:
    print("FAIL")
    exit(1)
```

---

## Section 5: Hyperparameters

```python
# Model size
ASPECT_RATIO = 64       # model_dim = depth * ASPECT_RATIO
HEAD_DIM = 128
DEPTH = 8

# Batch
TOTAL_BATCH_SIZE = 2**19  # ~524K tokens
DEVICE_BATCH_SIZE = 128

# Optimization
EMBEDDING_LR = 0.6
MATRIX_LR = 0.04         # Muon LR (lower than Adam)
WEIGHT_DECAY = 0.2

# Schedule
WARMUP_RATIO = 0.0       # No warmup
WARMDOWN_RATIO = 0.5     # 50% time for cooldown
```

---

## Key Code Patterns to Remember

### 1. RMS Norm (no learnable parameters)
```python
def norm(x):
    return F.rms_norm(x, (x.size(-1),))
```

### 2. Sliding Window
```python
window_sizes = {"L": seq_len, "S": seq_len // 2}
```

### 3. Value Embeddings (ResFormer)
```python
# Optional per-layer value embeddings
if has_ve(layer_idx, n_layer):
    ve_gate = nn.Linear(ve_dim, n_kv_head)
    # Gated addition in attention
    gate = 2 * sigmoid(ve_gate(x))
    v = v + gate * ve
```

---

## Interview Code Questions

### Q: How does the forward pass work?

> "Input tokens → token embeddings → RMS norm → N transformer blocks (attention + MLP, each with residual) → RMS norm → linear projection to vocab → softmax. Each block also adds value embeddings with learned gates."

### Q: What's the difference between Muon and AdamW?

> "AdamW updates each parameter independently using gradient statistics (first and second moment). Muon for 2D matrices first orthogonalizes the gradient then applies update - keeps weight matrices diverse. Think of AdamW as per-parameter learning, Muon as structure-preserving."

### Q: How does the training stop?

> "Fixed time budget - training runs for exactly 5 minutes (configurable in prepare.py). The loop checks `total_training_time >= TIME_BUDGET` and breaks immediately after warmup steps. This ensures consistent experiment duration."

---

## Common Mistakes (Interview Gold!)

| Mistake | Why It's Wrong |
|---------|---------------|
| Using full attention everywhere | O(n²) memory - breaks for long sequences |
| Same LR for all parameters | Embeddings need higher LR than matrices |
| No loss monitoring | Exploding loss wastes experiment time |
| Variable time budgets | Can't compare experiments fairly |

---

*Next: See `mlops-notes.md` for Phase 3 project ideas!*
