---
layout: post
title: "Attention Is Not Matmul Bound"
subtitle: "Where the time really goes"
tags: [tutorials, llm, gpu, attention, performance, notes]
cover-img: /assets/img/blog/covers/attention-matmul.svg
head-extra: [mathjax.html]
---

If someone asks which part of attention is slowest, the obvious guess is the matrix multiplication. It has by far the most floating-point operations, so surely it must dominate the runtime. On a modern GPU, that intuition is **wrong**. The two matmuls in attention are simply not where the time goes.

To see why, let us actually count the bytes.

## Example: GPT-2

- sequence length $N = 1024$
- number of heads $H = 12$
- head dimension $D = 64$
- batch size $B = 1$ (to keep the arithmetic simple)
- precision FP16 (2 bytes per element)

### Step 1: size of each matrix

**$Q$, $K$, $V$** each have shape $(B, H, N, D) = (1, 12, 1024, 64)$:

$$
1 \times 12 \times 1024 \times 64 \times 2 \ \text{bytes} = 1.5 \ \text{MB}
$$

**Attention score matrix $S$** has shape $(B, H, N, N) = (1, 12, 1024, 1024)$:

$$
1 \times 12 \times 1024 \times 1024 \times 2 \ \text{bytes} = 24 \ \text{MB}
$$

This is the key number. The score matrix is **enormous**, precisely because it scales with $N^2$.

**Output matrix $O$** has shape $(B, H, N, D)$, again $1.5$ MB.

### Step 2: HBM traffic per step (reads + writes)

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

### Step 3: the conclusion

Add it up, and the combined HBM traffic of mask, softmax, and dropout (48 MB) is **almost double** that of either matmul (27 MB each). The supposedly heavy operation turns out to be the cheap one.

- Although matmul has far more FLOPs than the other operations, modern GPU Tensor Cores accelerate that compute so aggressively that the **bottleneck shifts to data movement.**
- For the three intermediate elementwise operations, the GPU cores finish the trivial arithmetic almost instantly, so the time is spent instead waiting on the **HBM read/write of that 24 MB score matrix.**

## Why FlashAttention wins

Vanilla PyTorch materializes the 24 MB $S$ matrix in HBM, reads it back, then writes it out again, and it pays that toll once per elementwise op. FlashAttention **fuses** the matmuls, masking, softmax, and dropout into a single kernel that keeps the score tiles in fast on-chip SRAM and never spills the full $S$ matrix to HBM. The FLOPs barely change, yet the HBM traffic plummets, and the runtime falls right along with it.

The lesson generalizes. When an operation is **memory-bound**, the path to speed is not "do less math." It is "move fewer bytes."

---

*Note: these notes are compiled from sources on the internet and are not my original work. I plan to rewrite them in my own words later.*
