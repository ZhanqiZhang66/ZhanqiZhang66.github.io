---
layout: post
title: "The 'Expert' in MoE Is Not an Expert"
subtitle: "Mixture-of-Experts is conditional computation, and its auxiliary losses are system constraints, not learning signals"
tags: [llm, moe, architecture, notes]
head-extra: [mathjax.html]
---

The first time people meet *Mixture of Experts*, they instinctively assume: since it is called "experts," surely each expert specializes in a different task? The reading is natural — but in a real MoE system it does not hold.

MoE is not doing "division of labor among specialists." It is doing something far more mechanical, even dull: **conditional computation.**

## What MoE is actually doing

In one sentence, MoE solves the problem:

> How can we use far more parameters **without** significantly increasing the amount of computation?

Its method: take one layer (usually the FFN) and split it into many *experts*, and let each token activate only a few of them. An expert is not a role — it is an **optional block of parameters**.

So why do experts end up "looking different" from each other? Because tokens are assigned to experts by a **router** (a gating network). The router produces a distribution over experts for each token and selects the top-$k$ experts to actually do the computation. Over time, different experts receive different token distributions and different gradient statistics, so their behavior starts to diverge. This is **organization that emerges naturally during training**, not something designed by hand.

## The AI will absolutely cut corners

If the router's only goal is to minimize the main-task loss, it will almost certainly learn a strategy that "looks clever but is terrible for the system": dump most tokens onto a handful of experts and leave the rest idle. That defeats the entire point of having many experts.

So we add an auxiliary **load-balancing loss**. A straightforward form is:

$$
L_{\text{expert}} = \sum_{e=1}^{E} \left( \bar{p}_e - \frac{1}{E} \right)^2
$$

There are three key quantities:

- $E$ — the total number of experts.
- $\bar{p}_e$ — the average probability (or token share) with which expert $e$ is selected over a batch.
- $1/E$ — the share each expert should receive in the ideal, uniform case.

This loss measures how far the **actual usage distribution** is from the **uniform distribution**. When $\bar{p}_e \approx 1/E$ for all experts, the loss is tiny. When some expert is chosen far too often (many tokens routed to the same expert) or far too rarely (some experts receive no tokens at all), the loss becomes large.

## Per-device balancing

In practice experts are usually bound tightly to devices: a group of experts lives on one GPU, so uneven routing means uneven device load. Even if the *per-expert* counts look balanced, severe skew can still appear at the *device* level. That is where a **per-device balancing loss** comes in. Its form is essentially identical — only the statistic changes from experts to devices:

$$
L_{\text{device}} = \sum_{d=1}^{D} \left( \bar{t}_d - \frac{1}{D} \right)^2
$$

where $\bar{t}_d$ is the fraction of tokens actually received by device $d$ and $D$ is the number of devices (GPUs). Exactly the same formula as the per-expert balancing loss — only this time it penalizes uneven GPU utilization.

## Why both losses are "mandatory"

They constrain imbalance at **different levels**:

- **per-expert** — a parameter-utilization problem;
- **per-device** — a system-load and communication problem.

If you only do the former, experts may look balanced while devices stay overloaded. If you do neither, the router collapses very quickly and MoE's advantage never materializes.

The key point: these losses are **not there to make the model "learn better."** They are there to make MoE **trainable at all**.

## A crucial shift in perspective

In a dense model, the loss is a *learning signal*. In MoE, part of the loss is a **system constraint**. These auxiliary losses do not define "what the correct output is"; they define "which behaviors are permitted."

## Summary

- MoE experts are not semantic specialists — they are **computation paths**.
- The router's freedom must be constrained, or it will certainly collapse.
- The essence of the auxiliary loss is not an optimization trick but a **hard constraint on system behavior**.

Once you adopt this lens, the designs of *expert*, *routing*, and *balancing* all stop being mysterious.

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
