---
layout: post
title: "Speculative Decoding"
subtitle: "Same output, much faster"
tags: [tutorials, llm, inference, decoding, notes]
cover-img: /assets/img/blog/covers/speculative-decoding.svg
head-extra: [mathjax.html]
---

Speculative decoding (also called speculative sampling) is one of the most elegant tricks in the LLM inference-acceleration toolbox. In one line, it lets a large model run at speeds that were previously unimaginable, all **without sacrificing any accuracy**.

## 1. The core pain point: why is large-model inference so slow?

Before we can fix the slowness, we have to understand where it comes from. LLMs generate text **autoregressively**, which means they must finish the first token before they can produce the second, and so on. It is a lot like writing an essay one word at a time, never drafting the first and third paragraph in parallel.

The bottleneck is **moving data, not computing it.** Modern GPUs have enormous, in fact surplus, compute. The real ceiling is **memory bandwidth**. To generate *one* token, the GPU must haul the model's gigantic parameters (hundreds of GB) out of memory into the compute cores once.

> Here is an analogy. You need to move bricks (compute), but the bricks sit in a warehouse kilometers away (memory). The traditional approach goes like this: drive the truck to the warehouse, grab **one brick**, drive back, lay it, then drive to the warehouse again, grab one more brick, and repeat. No matter how fast your truck (GPU compute) is, all the time is spent on the road.

## 2. The intuition: a literary master and an intern

The core idea of speculative decoding is simple: let a fast junior scribble ahead, and let the expert merely check the work.

- **The large model (target model)** is a literary master. It is brilliant and writes flawless prose, but it writes *very slowly*, since every token requires deep deliberation and a full parameter haul.
- **The small model (draft model)** is an intern. It is mediocre, but it writes *blazingly fast* thanks to its few parameters, which are cheap to move.

The workflow:

1. **The intern guesses (Draft).** The intern glances at the prompt and quickly drafts the next, say, 5 tokens ("today the weather is really nice").
2. **The master verifies (Verify).** The master reads those 5 tokens at once. Crucially, the time it takes the master to *read and verify* 5 tokens is about the same as the time to *write* a single token himself, because hauling the truck to the warehouse costs roughly the same whether you bring back 1 brick or 5.
3. **Decision.**
   - If the master agrees that all 5 tokens match what he would have written, he **accepts them all**, generating 5 tokens in one round for a 5× speedup.
   - If the master agrees with the first 3 but the 4th is wrong, he keeps the first 3, discards the rest, and writes the correct 4th token himself.

That is speculative decoding: **"guess + parallel verify"** replacing **"serial generation."**

## 3. How it actually works inside the GPU

**Step 1, drafting.** Load a small model (think `GPT-nano` scale) and have it quickly generate $K$ tokens (say $K = 4$). Because the draft model has so few parameters, this is fast. We obtain a draft $[x_1, x_2, x_3, x_4]$.

**Step 2, parallel verification.** This is the magic step. The $K$ draft tokens are packed and fed to the large model **in a single forward pass**. Generation is serial, but *verification is parallel*:

- while looking at $x_1$, the big model computes the probability of $x_2$;
- while looking at $x_2$, it computes the probability of $x_3$; and so on.

Because GPUs excel at matrix math, **processing 1 token and processing 5 tokens take almost the same wall-clock time** (as long as you stay under the memory-bandwidth ceiling).

**Step 3, acceptance and rejection.** Compare the big model's distribution with the draft:

- **Greedy decoding:** if the draft token equals the big model's highest-probability token, keep it.
- **Sampling:** even if they differ, the draft token can be kept as long as it falls within the big model's allowed probability range, via a *rejection sampling* scheme that preserves diversity.

At the first rejected token, everything after it is discarded, the big model supplies the correct token, and the next round begins.

## 4. Why it is "lossless"

Many acceleration methods (quantization, pruning) make the model dumber. Speculative decoding is called **lossless** because every output token is either verified and accepted by the big model or written by the big model itself.

The mathematical guarantee is this: with a properly designed acceptance and rejection rule, the distribution of text produced by speculative decoding is **identical** to the distribution of the big model running on its own. The user gets exactly the result they would have gotten without the trick, just 2 to 3× faster.

## 5. Trade-offs

**Pros**

1. **Significant speedup.** You typically see 2× to 3×, and even more on structured tasks like code generation.
2. **No loss of quality.** No retraining of the big model is required.
3. **Hardware-friendly.** It cashes in the GPU compute that would otherwise sit idle, turning a memory-bound problem into a more compute-bound one.

**Cons**

1. **Two models in memory.** You must fit both a big and a small model in VRAM. The small one is small, but it is not free.
2. **Alignment requirement.** The "intern" and the "master" should write in similar styles. If the intern is too weak and is wrong every time, the master rejects everything and rewrites, which ends up *slower* than the original, because you also wasted time letting the intern guess.
3. **Batch-size limit.** When concurrency is very high (large batch size), the GPU's compute may already be saturated, and adding speculative decoding helps little.

## 6. Modern variants

- **Medusa.** No separate draft model. Instead, attach a few lightweight prediction *heads* on top of the big model; each head predicts the 1st, 2nd, 3rd next token in parallel, removing the need to load a second model.
- **Lookahead decoding.** No draft model at all. It uses the big model's own n-grams as drafts, so having produced "San," it guesses "Francisco" is likely next.
- **Prompt lookup decoding.** Copy-paste similar spans from the already-generated context to serve as the draft for the big model to check.

## 7. Summary

Speculative decoding is like the "predictive input" system in a video game:

1. **Problem:** the big model is slow because reading and writing memory is slow.
2. **Solution:** a small model guesses fast, the big model verifies in batch.
3. **Essence:** trade *cheap compute* for *expensive bandwidth*.
4. **Result:** quality unchanged, speed roughly doubled.

It is a textbook **systems-engineering optimization**. It does not change the AI's intelligence, but it dramatically changes the experience of interacting with it.

---

*Note: these notes are compiled from sources on the internet and are not my original work. I plan to rewrite them in my own words later.*
