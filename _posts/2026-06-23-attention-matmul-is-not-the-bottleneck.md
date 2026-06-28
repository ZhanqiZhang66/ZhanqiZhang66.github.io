---
layout: post
title: "Attention: Why Matmul Is Not the Bottleneck"
subtitle: "Counting HBM traffic on GPT-2 shows that masking, softmax, and dropout move twice the bytes of the two matmuls"
tags: [tutorials, llm, gpu, attention, performance, notes]
thumbnail-img: /assets/img/blog/llm_notes/attention-flashattention-bars.jpg
head-extra: [mathjax.html]
---

> **Q:** In attention, what is the slowest part?
> **Me:** ...Matmul? *(Instantly busted.)*

It feels obvious — matrix multiplication has by far the most floating-point operations, so it must dominate the runtime. On a modern GPU this intuition is **wrong**. The two matmuls in attention are not where the time goes.

![Attention timing on GPT-2: in vanilla PyTorch, masking, softmax, and dropout dominate, while a fused FlashAttention kernel collapses the whole thing.](/assets/img/blog/llm_notes/attention-flashattention-bars.jpg)

To see why, let us actually count the bytes.

## A concrete configuration: GPT-2

- sequence length $N = 1024$
- number of heads $H = 12$
- head dimension $D = 64$
- batch size $B = 1$ (to keep the arithmetic simple)
- precision FP16 (2 bytes per element)

### Step 1 — size of each matrix

**$Q$, $K$, $V$** each have shape $(B, H, N, D) = (1, 12, 1024, 64)$:

$$
1 \times 12 \times 1024 \times 64 \times 2 \ \text{bytes} = 1.5 \ \text{MB}
$$

**Attention score matrix $S$** has shape $(B, H, N, N) = (1, 12, 1024, 1024)$:

$$
1 \times 12 \times 1024 \times 1024 \times 2 \ \text{bytes} = 24 \ \text{MB}
$$

This is the key number — the score matrix is **enormous**, because it scales with $N^2$.

**Output matrix $O$** has shape $(B, H, N, D)$, again $1.5$ MB.

### Step 2 — HBM traffic per step (reads + writes)

**1. First matmul, $Q K^{\top}$:**

- read $Q$: 1.5 MB
- read $K$: 1.5 MB
- write $S$: 24 MB
- **total: 27 MB**

**2. Mask / softmax / dropout:**

- read $S$: 24 MB
- write $S_{\text{masked}}$: 24 MB
- **total: 48 MB**

**3. Second matmul, $S_{\text{dropout}} V$:**

- read $S_{\text{dropout}}$: 24 MB
- read $V$: 1.5 MB
- write $O$: 1.5 MB
- **total: 27 MB**

### Step 3 — the conclusion

The combined HBM traffic of mask + softmax + dropout (48 MB) is **almost double** that of either matmul (27 MB each).

- Although matmul has far more FLOPs than the other operations, modern GPU Tensor Cores accelerate that compute so aggressively that the **bottleneck shifts to data movement.**
- For the three intermediate elementwise operations, the GPU cores finish the trivial arithmetic almost instantly; the time is spent waiting on the **HBM read/write of that 24 MB score matrix.**

## Why FlashAttention wins

The chart tells the whole story. Vanilla PyTorch materializes the 24 MB $S$ matrix in HBM, reads it back, writes it again — once per elementwise op. FlashAttention **fuses** the matmuls, masking, softmax, and dropout into a single kernel that keeps the score tiles in fast on-chip SRAM and never spills the full $S$ matrix to HBM. The FLOPs barely change; the HBM traffic plummets, and so does the runtime.

The lesson generalizes: when an operation is **memory-bound**, the path to speed is not "do less math" — it is "move fewer bytes."

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
