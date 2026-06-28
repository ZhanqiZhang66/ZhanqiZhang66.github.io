---
layout: post
title: "Mixture of Experts"
subtitle: "Experts are computation paths"
tags: [tutorials, llm, moe, architecture, notes]
cover-img: /assets/img/blog/covers/moe.svg
head-extra: [mathjax.html]
---

The first time people meet *Mixture of Experts*, they instinctively assume that since it is called "experts," surely each expert specializes in a different task. The reading is natural, but in a real MoE system it simply does not hold.

MoE is not doing "division of labor among specialists." It is doing something far more mechanical, even dull: **conditional computation.**

## What MoE is actually doing

In one sentence, MoE solves the problem:

> How can we use far more parameters **without** significantly increasing the amount of computation?

The method is to take one layer (usually the FFN), split it into many *experts*, and let each token activate only a few of them. An expert is not a role. It is an **optional block of parameters**.

So why do experts end up "looking different" from each other? Because tokens are assigned to experts by a **router** (a gating network). The router produces a distribution over experts for each token and selects the top-$k$ experts to actually do the computation. Over time, different experts receive different token distributions and different gradient statistics, so their behavior starts to diverge. This is **organization that emerges naturally during training**, not something designed by hand.

## The router will always cut corners

If the router's only objective is to minimize the main task loss, it will almost certainly settle on a strategy that looks clever but is bad for the system: it sends most tokens to a small group of experts and leaves the rest idle. That wastes the parameters we paid for and undermines the entire reason for having many experts.

To prevent this, modern MoE models add an auxiliary load-balancing loss. The version introduced by the Switch Transformer is still the standard today:

$$
L_{\text{aux}} = \alpha \cdot N \cdot \sum_{i=1}^{N} f_i \, P_i
$$

This is a dot product between two $N$-dimensional vectors, scaled by a coefficient. Each symbol has a clear meaning:

- $N$ is the number of experts in the layer.
- $f_i$ is the fraction of tokens in the batch that are actually dispatched to expert $i$. We compute it by counting how many tokens the router sends to expert $i$ and dividing by the total number of tokens.
- $P_i$ is the fraction of router probability assigned to expert $i$, averaged over every token in the batch. It comes straight from the router's softmax outputs.
- $\alpha$ is a small coefficient that controls how strongly balancing is enforced.

Both $f_i$ and $P_i$ sum to one across the experts, so the loss reaches its minimum when both are uniform, meaning every expert receives the same share of tokens and the same share of probability. The factor $N$ simply normalizes the loss so that this balanced minimum stays constant no matter how many experts there are.

One detail is easy to miss but matters a lot. The dispatch fractions $f_i$ come from a hard top-$k$ selection, which is not differentiable, whereas the probabilities $P_i$ are. Because the loss multiplies the two together, gradients still flow through $P_i$: the model lowers the loss by pulling probability mass away from experts that are already overloaded. So even though we cannot backpropagate through the routing decision itself, the auxiliary loss as a whole is differentiable and steadily nudges the router toward balanced assignments.

## Balancing at the device level

In a large deployment, experts are spread across many GPUs, with a group of experts living on each device. Balancing experts one by one is not enough, because the load can still be skewed at the device level: even if no single expert is overloaded, one GPU can end up doing far more work than another. DeepSeek addresses this by adding a balance loss that operates on groups of experts rather than single experts. It has the same shape as the expert-level loss, only the statistics are aggregated per device:

$$
L_{\text{dev}} = \alpha' \sum_{i=1}^{D} f_i' \, P_i'
$$

Here $D$ is the number of devices, $f_i'$ is the average dispatch fraction over the experts placed on device $i$, and $P_i'$ is the total router probability assigned to those experts. DeepSeek pairs this with a communication-balance loss that keeps the volume of data sent to and from each device even. The goal never changes: keep every GPU equally busy.

The newest models even question whether an auxiliary loss is the right tool at all. DeepSeek-V3 drops the balancing loss entirely and instead keeps a small per-expert bias that it nudges up or down during training. Because the bias is applied only when selecting the top-$k$ experts, and not when computing their probabilities, it steers the load without distorting the router's gradients. The lesson is the one we keep running into: balance is something the system has to be engineered for, whether through a loss or through a bias.

## Why both losses are "mandatory"

They constrain imbalance at **different levels**. The per-expert loss addresses a parameter-utilization problem, while the per-device loss addresses a system-load and communication problem.

If you only do the former, experts may look balanced while devices stay overloaded. If you do neither, the router collapses very quickly and MoE's advantage never materializes.

The key point is that these losses are **not there to make the model "learn better."** They are there to make MoE **trainable at all**.

## A crucial shift in perspective

In a dense model, the loss is a *learning signal*. In MoE, part of the loss is a **system constraint**. These auxiliary losses do not define "what the correct output is"; they define "which behaviors are permitted."

## Summary

- MoE experts are not semantic specialists. They are **computation paths**.
- The router's freedom must be constrained, or it will certainly collapse.
- The essence of the auxiliary loss is not an optimization trick but a **hard constraint on system behavior**.

Once you adopt this lens, the designs of *expert*, *routing*, and *balancing* all stop being mysterious.