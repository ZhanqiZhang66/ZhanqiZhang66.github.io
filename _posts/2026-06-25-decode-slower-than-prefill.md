---
layout: post
title: "Why LLM Decode Is 100× Slower Than Prefill"
subtitle: "The bottleneck is not the KV cache — it is matrix shape, and the physics shows up in arithmetic intensity"
tags: [tutorials, llm, inference, roofline, performance, notes]
head-extra: [mathjax.html]
---

## A widely misunderstood bottleneck

The slowness of LLM inference is most often blamed on the KV cache — it takes memory, it is non-contiguous, copying it is expensive. The engineering stack around it (PagedAttention, vLLM, SGLang) is mature. Yet even with KV-cache management perfected, the **decode** stage is still one to two orders of magnitude slower than **prefill**. This is not bad engineering; the physical bottleneck is simply elsewhere.

The real bottleneck is **matrix shape**. Decode generates one token at a time, so the input matrix degenerates from prefill's "flat rectangle" into "a single needle." That shape change turns a **GEMM** into a **GEMV**, and the arithmetic intensity collapses from a sizeable value that grows linearly with dimension into a fixed constant of about $0.5$. Any arithmetic intensity below the hardware ridge means **memory bandwidth is the ceiling** — no amount of extra compute or faster Tensor Cores can rescue it.

The key is to translate the two inference terms — *prefill* and *decode* — into "the geometry of the input matrix." At the terminology level the two differ only in "how many tokens are processed at once." At the shape level, this is a **phase transition from compute-bound to memory-bound.**

## From abstract terms to concrete shapes

Take LLaMA-7B (hidden $= 4096$, FFN $= 11008$, head_dim $= 128$). Suppose 100 input tokens, with 50 already generated. Every matmul, before and after, shares the same weights — the difference is entirely in the shape of the input $X$.

**Prefill** processes all 100 input tokens at once:

| Operator | Input $X$ | Weight $W$ | Output |
|---|---|---|---|
| QKV projection | $(100, 4096)$ | $(4096, 4096)$ | $(100, 4096)$ |
| FFN gate/up | $(100, 4096)$ | $(4096, 11008)$ | $(100, 11008)$ |
| FFN down | $(100, 11008)$ | $(11008, 4096)$ | $(100, 4096)$ |

**Decode** generates a single token — same weights, but $X$ degenerates:

| Operator | Input $X$ | Weight $W$ | Output |
|---|---|---|---|
| QKV projection | $(1, 4096)$ | $(4096, 4096)$ | $(1, 4096)$ |
| FFN gate/up | $(1, 4096)$ | $(4096, 11008)$ | $(1, 11008)$ |
| FFN down | $(1, 11008)$ | $(11008, 4096)$ | $(1, 4096)$ |

The multiply is still mathematically valid, but the $M$ dimension drops from 100 to 1 — $X$ is no longer a matrix, it is a vector. **GEMM degenerates into GEMV.** Attention behaves the same way: at prefill $Q$ is a small $(100, 128)$ matrix; at decode it is a single $(1, 128)$ vector.

## The arithmetic-intensity formula

Shape decides arithmetic intensity, and arithmetic intensity decides which side of the Roofline a kernel lands on. Consider one matmul $X W$ with $X$ of shape $(M, K)$ and $W$ of shape $(K, N)$.

Total compute:

$$
\text{FLOPs} = 2 \cdot M \cdot N \cdot K
$$

Theoretical minimum memory traffic (every element of the two inputs and the output read or written at least once, 4 bytes each):

$$
\text{Bytes}_{\min} = 4 \cdot (MK + KN + MN)
$$

Arithmetic intensity:

$$
\text{AI} = \frac{M N K}{2 \cdot (MK + KN + MN)}
$$

Plugging in **prefill** ($M = 100$, $N = K = 4096$):

$$
\text{AI}_{\text{prefill}} = \frac{100 \cdot 4096 \cdot 4096}{2 \cdot (100\cdot 4096 + 4096\cdot 4096 + 100\cdot 4096)} \approx 49
$$

Plugging in **decode** ($M = 1$, $N = K = 4096$):

$$
\text{AI}_{\text{decode}} = \frac{1 \cdot 4096 \cdot 4096}{2 \cdot (1\cdot 4096 + 4096\cdot 4096 + 1\cdot 4096)} \approx 0.5
$$

The two numbers differ by **100×**. This is not a gap in engineering headroom — it is a gap in physical nature.

The intuition behind the formula is even clearer. $W$ is a $(4096, 4096)$, 64 MB weight matrix. In prefill, $W$ is read once but serves 100 tokens' projections — every byte of $W$ read produces about 200 FMAs. In decode, $W$ is again read once but serves only 1 token — every byte of $W$ read produces just 1 FMA. **Reuse collapses 100×, and so does AI.** This is the fundamental difference between GEMV and GEMM: GEMM's reuse grows linearly with $M$, while GEMV's reuse is locked at 1. No matter how large the weights or how deep $K$, decode's AI is a constant.

## The physical cost of a constant AI

AI is the x-axis of the Roofline model; the y-axis is achievable FLOPS. Below the ridge point, performance is set by bandwidth:

$$
\text{Performance} = \text{AI} \cdot \text{Bandwidth}
$$

An H100 SXM's FP32 ridge is around $20$ FLOP/byte, and its BF16 + Tensor Core ridge around $150$. Decode's AI of $0.5$ is far below any generation's ridge — meaning the compute ceiling is irrelevant; **only HBM bandwidth is usable.**

Concretely, one LLaMA-7B decode step must read every weight across all 32 transformer layers. In FP16 the weights are about 14 GB, and the H100's HBM bandwidth is 3.35 TB/s, so the theoretical lower bound is:

$$
T_{\text{decode}} = \frac{14\ \text{GB}}{3.35\ \text{TB/s}} \approx 4.2\ \text{ms / token}
$$

This is the physical limit. No matter how good the kernel or how strong the Tensor Core, single-batch decode can never beat 4.2 ms/token — HBM must read the whole 14 GB to produce the next token. The same hardware running prefill, with AI near the ridge, can reach over 60% of BF16 compute. By FLOPS, prefill is two orders of magnitude faster than decode. Every "why is decode so slow?" confusion traces back to the comparison of these two numbers.

## Continuous batching: a fix at the shape level

Once the AI formula is clear, continuous batching becomes transparent. Its name suggests "continuously batching requests," but the problem it actually solves is to **re-thicken the degenerate needle matrix.**

If 16 users are decoding at once and each is handled independently, that is 16 GEMVs, each reading the 14 GB of weights — HBM read 16 times. Concatenate their inputs and $X$ goes from $(1, 4096)$ to $(16, 4096)$: no longer a needle, but a flat-but-thick rectangle. The same weights, read once, now serve 16 tokens' projections.

| Config | $X$ shape | FMAs per byte of $W$ | AI |
|---|---|---|---|
| single-request decode | $(1, 4096)$ | 1 | 0.5 |
| batch-16 decode | $(16, 4096)$ | 16 | 8 |
| batch-64 decode | $(64, 4096)$ | 64 | 32 |
| prefill, seq = 100 | $(100, 4096)$ | 100 | 49 |

AI grows **linearly with batch size** — the fundamental reason continuous batching raises throughput by one to two orders of magnitude. Importantly, this improvement relies on no kernel trick at all; it comes purely from merging users' work into a thicker matrix. The "continuous" part that distinguishes it from static batching (iteration-level scheduling, PagedAttention, chunked prefill) solves the engineering issues of asynchronous requests, uneven completion, and mixing prefill with decode.

## The other tricks, through the same lens

- **Quantization (INT4/FP8)** compresses weights to 1/4 or 1/8, equivalent to making HBM bandwidth "appear" several times faster without changing AI.
- **Speculative decoding** uses a small model to propose multiple candidates that the big model verifies in one pass — the $M$ dimension goes from 1 to $k$.
- **MoE** at decode merges activated experts across the batch (grouped GEMM) to avoid each expert degenerating into an ultra-thin GEMV.
- **FlashAttention** keeps the intermediate score matrix in on-chip memory and never spills it — the AI gain comes from reducing HBM access rather than changing shape, but the Roofline analysis is identical.

## Shape is the meta-variable

How exquisitely a kernel is written decides whether you hit 80% or 95% of the Roofline ceiling — but *which side of the Roofline you are on, and what the ceiling is*, is decided entirely by matrix shape. Kernel optimization explains the last mile; **shape optimization decides the racetrack itself.**

So when you face a new LLM-inference performance problem, the first step is not to profile kernel time, nor to check KV-cache hit rate — it is to **write out the shapes of every matmul in the workload, plug them into the AI formula, and see which side of the Roofline each operator falls on.** After that, where the bottleneck is, how far it can be optimized, and which class of technique you need are all immediately clear. That is the threshold from "being able to use an inference framework" to "being able to design an inference system."

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
