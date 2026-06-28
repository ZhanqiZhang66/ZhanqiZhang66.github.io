---
layout: post
title: "The Temperature Knob: Sampling, Penalties, and Hallucination"
subtitle: "A decoding-side tour from softmax temperature to repetition loops and made-up facts"
tags: [tutorials, llm, decoding, notes]
cover-img: /assets/img/blog/tutorial-cover.svg
thumbnail-img: /assets/img/blog/llm_notes/temp-feedback-loop.png
head-extra: [mathjax.html]
---

The last layer of a language model does not emit a probability — it emits **logits**, a vector of real numbers. A probability distribution only appears after we push those logits through a softmax. The entire secret of *temperature* lives in the step just before the softmax: we divide every logit by a single scalar $T$.

## 1. Temperature: making the distribution sharper or flatter

A useful mental picture is a pot of porridge. The grains, beans, and squash are already in there in fixed proportions; turning the heat up or down does not change what is in the pot, only how sharply the ingredients stand out from one another. Temperature does the same thing to a token distribution — it never changes the **ranking** of tokens, only the **gaps** between neighboring probabilities.

Formally, we scale each logit by $1/T$ and then take the softmax:

$$
P(x_i) = \frac{\exp(z_i/T)}{\sum_j \exp(z_j/T)}
$$

Three limiting values make the behavior obvious:

- **$T \to 0$.** The largest logit is exponentially amplified until it dominates everything. The distribution collapses to a single spike — this is exactly `argmax`, i.e. greedy decoding. Greedy is not "temperature-free"; it is the limit of temperature going to zero.
- **$T = 1$.** Nothing is changed. This is the natural distribution the model saw during training.
- **$T \to \infty$.** Every logit is squeezed toward $0$, the distribution approaches uniform, and the model is effectively drawing tokens at random from the vocabulary. The text falls apart immediately.

In practice $T$ usually lives somewhere around $0.2$–$1.2$: lower for factual question answering, higher for creative writing. There is no universally "correct" value. A higher temperature raises the chance of sampling low-probability tokens and increases drift, but it does not *necessarily* produce gibberish — whether the text survives depends on how flat the underlying distribution already is.

One frequent source of confusion: **temperature scaling only matters when you sample.** If you take a pure greedy / `argmax` path, dividing all logits by a positive constant never changes the ordering, so the chosen token is identical. Where there is no randomness, the temperature knob spins in the void.

### Temperature does not work in isolation

Real systems apply temperature *before* candidate truncation. The semantic order is almost always:

1. temperature scaling,
2. candidate truncation (top-$k$ / top-$p$),
3. renormalize over the survivors and sample.

This order matters. If you truncated first and scaled second, temperature would lose its influence over *which tokens make it into the candidate set*. Because scaling comes first, even adjusting temperature alone indirectly resizes the top-$p$ nucleus: a sharper distribution yields a smaller, more focused nucleus; a flatter one yields a larger, more divergent nucleus.

> Temperature changes the gaps, not the ranking; its relationship to top-$k$/top-$p$ is "reshape the distribution first, then decide which few tokens to draw from."

## 2. Why models get stuck in loops: the feedback loop

Tuning temperature well does not guarantee good output. A classic failure is the model getting trapped in a repetition it cannot escape — *"this movie is very very very very …"* — or, more subtly, circling the same sentence over and over. This is called **pattern collapse** (colloquially, "the stuck record"). It is worst under greedy decoding, but it still happens with temperature sampling. Why?

The cause is the self-reinforcing feedback loop of autoregressive generation:

1. At step $t$ the model samples a token $x_t$.
2. $x_t$ is appended to the context and becomes part of the input at step $t+1$.
3. A local pattern that has already formed (e.g. "very very very") enters the context, and the model readily reads it as a pattern that is *still continuing* — especially under greedy, beam, or low-diversity sampling.
4. Once the same token has been sampled into the context several times, "one more of the same" becomes an even stronger candidate. The pattern pulls itself into being the next most-likely token.

Formally, given the already-generated sequence $x_{<t}$, the next-step distribution is simply

$$
P(x_t \mid x_{<t}) = \mathrm{softmax}\big(f_\theta(x_{<t})\big).
$$

The model does not "know" it is repeating. It only sees that "very" has appeared three times and, by the regularities it learned, judges a fourth "very" to be a reasonable continuation. This is structural, not a sign the model got dumber: unless the sampling strategy actively breaks up the local pattern, the loop reinforces itself.

![The autoregressive feedback loop that drives repetition: generated tokens re-enter the context, raise their own probability, and get sampled again.](/assets/img/blog/llm_notes/temp-feedback-loop.png)

## 3. Three penalties: operating directly on the distribution

If the loop comes from "already-generated tokens raising their own probability," the cure is direct — actively push down the probability of tokens that have already appeared, *before* each sampling step. That is what penalties do. They all act on the logits before softmax, but their mechanisms differ.

An important detail that is easy to miss: penalties count **tokens**, not words and certainly not sentences. A word may be split into two tokens, and two semantically unrelated pieces of text may happen to share a high-frequency token — both change what the penalty actually touches.

Let $z_i$ be the current-step logit of token $i$ and $c_i$ its count in the already-generated sequence.

**Repetition penalty** (HuggingFace style) discounts a token's logit multiplicatively if it has appeared:

$$
z_i' =
\begin{cases}
z_i / \alpha, & z_i \ge 0 \\
z_i \cdot \alpha, & z_i < 0
\end{cases}
\qquad (\text{if } i \text{ has appeared})
$$

With $\alpha > 1$, positive logits shrink and negative logits grow more negative, pushing the probability of seen tokens down across the board. $\alpha = 1.0$ means no penalty; $1.1$–$1.3$ is common. It does not distinguish one occurrence from ten — appearing even once triggers the cut.

**Frequency penalty** (OpenAI style) subtracts a score linearly in the number of occurrences:

$$
z_i' = z_i - \beta \, c_i
$$

With $\beta > 0$, a token seen five times loses $5\beta$ and one seen once loses $\beta$. This is finer-grained than the repetition penalty — the more something repeats, the harder it is pushed down — which suits the "high-frequency filler word keeps reappearing" failure mode.

**Presence penalty** (also OpenAI style) only checks whether a token has appeared at all:

$$
z_i' = z_i - \gamma \, \mathbb{1}[c_i > 0]
$$

Any token that has appeared once is reduced by $\gamma$, and no more. Its purpose is not to cure repetition but to **encourage new vocabulary** — useful when you want topical breadth, e.g. covering more subjects in a summary.

How to choose: for open-ended generation and continuation, frequency penalty is usually most effective, because the stuck-record disease is fundamentally driven by counts; if you only want to avoid topical poverty, presence penalty suffices; repetition penalty is an older but simple, robust fallback. The three do not replace one another, but using all three at once is rare — they fight each other.

> The cure for the stuck record is not lowering the temperature, it is automatically down-weighting repeated tokens at the next step — and *how* you down-weight depends on whether you care "has it appeared" or "how many times."

## 4. The three layers behind "talking nonsense"

Finally, *hallucination* — when a model confidently invents a nonexistent fact, cites a paper that was never written, or hands you a wrong API name. The full topic is far larger than decoding, but the part visible from the decoding side makes a good closing, because it connects the "temperature → sampling → penalty" thread to "why the model is wrong." There are at least three stacked layers.

**Layer 1 — sampling drift.** As long as $T > 0$, every step has some probability of drawing a non-optimal token. A single suboptimal draw is harmless, but over a long sequence these small drifts **accumulate along the autoregressive loop**: a slight wobble early on grows into a large deviation by token 200. Setting $T = 0$ removes this layer — at the cost of pinning generation quality to the greedy ceiling (repetition included).

**Layer 2 — long-tail amplification.** Top-$p$ was designed to cut off the unreliable tail: when the distribution is sharp the nucleus tightens; only when it is flat does the nucleus widen. The problem is that it cannot tell "flat because the model is genuinely weighing several reasonable options" from "flat because the model cannot tell the boundary." Exactly where the model is unsure (say, what follows a rare proper noun), the distribution naturally flattens, the nucleus expands, and more low-probability tokens are admitted — and a slightly high temperature flattens it further, admitting yet more. Once one of these tokens is drawn, it becomes the seed of fabricated content: it was never high-probability; sampling promoted it to the page.

**Layer 3 — model overconfidence (out-of-distribution).** The first two layers assume the model is at least honest about its own uncertainty — but it often is not. When the input falls outside the training distribution (OOD), the model frequently still produces a *sharp* distribution: it has not seen this question, yet it overlays patterns learned from similar ones and outputs a confident-looking answer. This layer has nothing to do with sampling or penalties — set $T = 0$, turn every penalty off, and the model will still make things up.

![The three stacked layers of hallucination, from the decoding view: sampling randomness, long-tail amplification, and model overconfidence.](/assets/img/blog/llm_notes/temp-hallucination-layers.png)

> Talking nonsense is not one phenomenon but the superposition of three: sampling randomness, the long tail being admitted into the candidate pool, and the model's overconfidence about the unknown.

The key boundary: the first two layers can be *mitigated* by tuning sampling; the third cannot. Blaming every hallucination on "temperature too high" is a misdiagnosis — and conversely, crushing temperature to $0$ will not make the model start telling the truth. Factual correctness relies far more on structural safeguards — external retrieval, citation checking, tool calls, refusal mechanisms — than on the decoder. Sampling is only one very thin filter in that stack.

## Wrap-up

By now the picture of generation should have sharpened from "the model emits tokens" to: at every step the model emits a *distribution*; everything we do to that distribution — temperature scaling, top-$k$/top-$p$ truncation, the various penalties — jointly decides the next token; and the failure modes of generation (repetition, drift, hallucination) are not the model getting dumber, but structural consequences of the distribution, the sampler, and the model's own limits stacked together.

**References**

- Holtzman et al., *The Curious Case of Neural Text Degeneration*, ICLR 2020. [arXiv:1904.09751](https://arxiv.org/abs/1904.09751) — the original top-$p$ / nucleus sampling paper.
- OpenAI Platform Docs — *Frequency and presence penalties* — official definitions and suggested ranges.
- Welleck et al., *Neural Text Generation with Unlikelihood Training*, ICLR 2020. [arXiv:1908.04319](https://arxiv.org/abs/1908.04319) — curing repetition from the training-objective side.
- Ji et al., *Survey of Hallucination in Natural Language Generation*, ACM Computing Surveys 2023. [arXiv:2202.03629](https://arxiv.org/abs/2202.03629).
