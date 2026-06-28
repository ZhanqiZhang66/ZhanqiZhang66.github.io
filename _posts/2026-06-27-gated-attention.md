---
layout: post
title: "Gated Attention: Rethinking Softmax Attention Through One Switch"
subtitle: "A single sigmoid gate after SDPA removes the attention sink, stabilizes training, and rescues long-context extrapolation"
tags: [llm, attention, architecture, notes]
head-extra: [mathjax.html]
---

## A simple modification ignored for eight years

Since the Transformer was finalized in 2017, the attention module's shape has barely changed structurally. The edits cluster at the two ends — at the front, positional encoding (absolute → RoPE) and KV-projection slimming (MHA → GQA → MLA); at the back, the GLU-ification of the FFN (SwiGLU became standard after 2020). But the core computation sandwiched between the Q/K/V projections and the final dense layer — the softmax-weighted sum — has been left almost untouched.

**Gated Attention** (2025) is one of the few works that deliberately touches that core. Its change is extremely simple: after the scaled dot-product attention (SDPA) output, multiply element-wise by a sigmoid gate score. One line of code; in the headwise version the added parameters are under one ten-thousandth of the model — yet it delivers three things: it eliminates the **attention sink**, it stabilizes large-scale training, and it lifts YaRN extrapolation to 128k from catastrophic collapse to usable.

This map is not a paper summary. It places the change back into the Transformer's evolutionary lineage to clarify what problem it really solves, why it was missed for so long, and how the design principle it reveals will shape the next generation of attention.

## 1. The modification: a positional game in one formula

A standard multi-head attention head writes as:

$$
o_i^{k} = \left( \sum_{j=0}^{i} S_{ij}^{k} \cdot X_j W_V^{k} \right) W_O^{k}
$$

Gated Attention modifies this single line to:

$$
o_i^{k} = \left( \sum_{j=0}^{i} S_{ij}^{k} \cdot X_j W_V^{k} \right) \odot \sigma\!\left(X_i W_\theta^{k}\right) \cdot W_O^{k}
$$

The only new term is $\sigma(X_i W_\theta^{k}) \in [0, 1]$ — a switch vector decided **solely by the current query token $X_i$** and multiplied element-wise into the aggregated context.

The paper's experimental design is itself the most instructive part. The gate has five candidate positions (after Q/K/V projection, after SDPA, after the final dense), and five variant dimensions (position, granularity, head-specific or not, multiplicative or additive, activation function). Over 30 combinations were swept on a 15B MoE model, and the single winning recipe was: **after SDPA + head-specific + sigmoid + multiplicative.** Change any one dimension and the gain either drops sharply or vanishes.

| Dimension | Best choice | Cost of the wrong choice |
|---|---|---|
| Position | after SDPA (G1) | after Key (G3) can even hurt |
| Granularity | head-specific | head-shared revives the sink |
| Form | multiplicative sigmoid | additive SiLU halves the gain |
| Source | current query | input-independent is nearly useless |

The real message of this table is not "which is best" but "**all four dimensions must be right simultaneously**" — meaning the change is not an arbitrary tweak but something bound by an internal structure.

## 2. Why it works: two separated contributions

The paper's most important methodological contribution is decomposing the gate's gain into two independent mechanisms, validated by controlled experiments.

### 2.1 The nonlinearity contribution: patching an overlooked design hole

Expand a single head's output:

$$
o_i^{k} = \sum_{j} S_{ij}^{k} \cdot X_j \left( W_V^{k} W_O^{k} \right)
$$

Because the attention-weighted sum is a linear operation, there is no nonlinearity between $W_V^{k}$ and $W_O^{k}$ — mathematically they collapse into a low-rank linear map of rank at most $d_k$. Under GQA, $W_V$ is further shared across heads, tightening the low-rank constraint.

This is a structural problem the community overlooked for eight years: in the FFN, the two linear layers always sandwich a GeLU or SwiGLU, but in attention the two linear layers have **nothing** between them. The gate's first contribution is to supply that missing nonlinearity. As a control, the paper uses GroupNorm (no learnable switch, but it introduces a normalization nonlinearity): perplexity drops from $6.026$ to $5.847$ — about 70% of the full sigmoid-gate gain ($6.026 \to 5.761$). Most of the gate's value, then, comes not from "gating" as a concept but from the general principle of **breaking the low rank.**

### 2.2 The sparse-switch contribution: an escape hatch for softmax

The remaining ~30% comes from another property of the sigmoid — it can output a strict $0$.

Softmax forces the attention weights to sum to $1$. When the model encounters a situation where it needs to attend to *nothing*, that is a hard constraint — the weight must be allocated somewhere. The model's workaround is to dump the weight onto the first token, forming an **attention sink**: in trained LLMs the first token absorbs, on average, $46.7\%$ of attention, independent of position and content.

With a sigmoid gate the model gains a second path: softmax still allocates however it wants, but when the gate closes the entire head output goes to zero. Formally, the attention block's output goes from forced-nonzero to learnably-arbitrarily-small, bypassing softmax's "must allocate" constraint. The evidence is clean: a control using NS-sigmoid (output restricted to $[0.5, 1.0]$) keeps input-dependence and keeps the nonlinearity, but cannot reach zero — and the sink survives.

## 3. The four conditions, and why the query side matters

The sweep also shows why the recipe is so specific:

| Condition | Wrong choice | Symptom |
|---|---|---|
| Head-specific | head-shared | first-token attention rises from 0.048 to 0.301 |
| Query-side (G1) | value-side (G2) | the sink still exists |

The query-side requirement deserves its own discussion. Placing the gate after the value projection (position G2) versus after SDPA (position G1) is mathematically very similar, but the G2 gate's signal comes from the attended history token $X_j$, while the G1 gate's comes from the current query token $X_i$. G2's viewpoint is "each key/value decides whether it wants to be heard"; G1's is "the current query decides whether to listen to anything at all."

Attention is fundamentally a **query-driven** process, so filtering must also be query-driven. G2 can suppress massive activations (cleaning up the residual stream) but cannot remove the attention sink — because it cannot let the query as a whole say "I do not want to attend." This is a deep asymmetry: *signal pollution* and *signal must exist* are two different problems; G2 treats only the former, G1 treats the latter.

## 4. A duality with the GLU-ification of the FFN

Gated Attention and SwiGLU are formally isomorphic — both are "main path ⊙ gating branch · output projection" — but they cure different diseases at different points in the Transformer block.

| Dimension | SwiGLU (FFN) | Gated Attention (G1) |
|---|---|---|
| Dimensional change | up then down | unchanged then projected |
| Gated object | the up-projected feature | the already-mixed context |
| Gate source | same source as the feature | different source (the query side) |
| Activation | SiLU, unbounded | sigmoid, filtering only |
| Problem solved | insufficient per-token compute capacity | the side effects of the softmax constraint |

This duality hints at a larger trend. Modern Transformers are converging, in several places, on a "two paths multiplied + output projection" structure — SwiGLU, Gated Attention, Mamba's SSM output gate, the GLU family. Mamba's authors argue outright that multiplication is the source of expressivity, and Gated Attention's experiments lend that further empirical support.

## 5. The underrated downstream effect: long-context extrapolation

If you only look at the $0.27$ drop in perplexity, this is an ordinary paper. What truly changes the verdict is long-context extrapolation:

| Setting | Baseline | Gated | Δ |
|---|---|---|---|
| 32k native | 79.50 | 79.77 | +0.3 |
| 32k YaRN | 37.94 | 72.88 | +34.9 |
| 128k YaRN | 31.65 | 58.82 | +27.2 |

Within the training length (32k) the two are nearly identical, but extending the context to 128k with YaRN sends the baseline into catastrophic collapse while the gated model degrades gently.

The explanation points to the deep nature of the attention sink. What the baseline forms during training is not a neutral statistical artifact but a precise internal mechanism that depends on specific RoPE distances — the sink is **deeply coupled with positional encoding.** When YaRN changes the RoPE base, that mechanism cannot transfer training-free, and the whole attention distribution collapses. The gated model never forms a sink; its filtering comes entirely from the input-dependent gate signal, decoupled from positional encoding, so it is naturally robust to RoPE changes.

This leads to a broader principle: **any "position-sensitive internal mechanism" learned during training is a fragility at inference time.** The success of training-free long-context methods (YaRN, PI, NTK-aware) conversely *requires* that training-stage models hold position-independent internal representations. The core value of Gated Attention is converting attention allocation from position-coupled to content-coupled — a principle deeper than "removing the attention sink."

## 6. Adoption and non-adoption in production

By mid-2026, Gated Attention has been validated in production but is far from standard.

| Vendor | Model | Attention choice |
|---|---|---|
| Qwen | Qwen3-Next, Qwen3.5, Qwen3.6 | Gated Attention + Gated DeltaNet hybrid |
| DeepSeek | V3.2, V4 | MLA |
| Moonshot | Kimi K2.5 | MLA |
| Zhipu | GLM-5 | MLA + DSA |
| MiniMax | M2.5 | standard MHA |

Qwen adopts it across the board, inside a hybrid architecture: most layers use Gated DeltaNet (cheap linear attention), and every third layer inserts one Gated Attention layer for precise retrieval. This posture is more refined than the paper's envisioned full-stack replacement, and closer to production needs. Other vendors took entirely different routes (MLA, DSA, pure MHA), so attention architecture in 2026 is in a multi-route competition. SwiGLU took about two years to replace the standard FFN; whether Gated Attention follows the same trajectory depends on not-yet-available evidence: whether its long-context robustness advantage keeps widening at larger scale.

## 7. Open questions

1. The gain split of "70% nonlinearity + 30% sparse switch" is a one-off measurement on a 15B MoE. How the two shift across scales, data mixes, and task types is unknown. If the sparse-switch contribution dominates at scale, Gated Attention is worth far more than current estimates.
2. The coupling between the attention sink and RoPE mismatch is only observed phenomenologically, with no theoretical characterization. A rigorous framework would have to answer: what does the sink encode into the weights during training, what is lost when YaRN modifies RoPE, and is there a "sink-aware YaRN variant" that could repair baseline models?
3. The relationship between Gated Attention and MLA has not been seriously compared. They rework different levels — MLA changes the KV representation (shrinking the cache), Gated Attention changes output filtering (removing the sink). In theory they are orthogonal and stackable, but no model uses both. If stacking works, the Qwen and DeepSeek routes are complements, not substitutes.
4. The gate's input-dependent sparsity naturally introduces dynamic computation sparsity — some heads on some tokens have a gate near $0$, so in principle that head's entire computation could be skipped. FlashAttention's current implementation does not exploit this. A kernel that is gate-aware, fuses the sigmoid multiply in the epilogue, and conditionally skips head computation may be the key to truly unlocking Gated Attention's performance — an obvious gap in algorithm–hardware co-design.

## 8. Judgments left for the next step

Gated Attention's true contribution is not the score bump but the design principle it reveals: **forcing the attention weights to sum to $1$ via softmax is an underestimated constraint, and the price the model pays to bypass it (attention sink, massive activations, training instability, long-context fragility) far exceeds prior understanding.**

This raises questions worth pursuing. Should softmax still be the default normalization for attention? Sigmoid attention, selective attention, and softpick already show comparable performance at small scale; once "eliminating forced normalization" becomes the objective, the form of attention may change further. Does the gate's placement principle (sandwiched between $W_V$ and $W_O$ to supply nonlinearity) apply elsewhere — cross-attention, prefix tuning, adapters all share the same low-rank bottleneck of two linear layers around a weighted sum.

And the deepest question: should attention's **weight allocation** and **information aggregation** be decoupled into two independently learnable processes? Softmax binds them — while allocating weights it forces aggregation into a nonzero output. The gate decouples them after the fact, reintroducing an independent "whether to aggregate" switch. If that decoupling is right, future attention may evolve from "one-step allocation" into a three-step, independently learnable structure of **allocation + aggregation + filtering.** The real use of this map is not to give answers but to place "multiply a sigmoid after SDPA" into a large enough context — both a patch for an eight-year-old design flaw of softmax, and a starting point for the next generation of attention to reorganize around decoupling weight and aggregation.

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
