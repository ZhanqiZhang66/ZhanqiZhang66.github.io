---
layout: post
title: "When Is SFT Done?"
subtitle: "Reading the signals"
tags: [tutorials, llm, post-training, sft, rl, notes]
cover-img: /assets/img/blog/covers/sft.svg
head-extra: [mathjax.html]
---

In LLM post-training, **SFT** (supervised fine-tuning) usually handles cold-start, behavior formatting, and task-protocol learning. But longer SFT is not always better, and lower loss is not always better. Judging whether SFT is "done" hinges not on how well it fits the training set, but on whether continued supervised imitation still produces stable **generalization** gains. It also hinges on whether that training still preserves room for a subsequent **RL** stage.

A more reasonable criterion comes from watching the marginal returns. Once adding more SFT data, running more epochs, or pushing training intensity higher makes dev-set gains plateau, once OOD and hard sets stop improving, once the output distribution begins to shrink, once pass@k diversity drops, and once the magnitude of later RL gains shrinks, SFT has basically entered a very-low-marginal-return phase.

Formally, "SFT is done" can be read as the simultaneous condition:

$$
\Delta S_{\text{dev}} \approx 0, \quad
\Delta S_{\text{OOD}} \le 0, \quad
\Delta H_{\pi} < 0, \quad
\Delta G_{\text{RL}} \le 0
$$

where $S_{\text{dev}}$ is dev-set capability, $S_{\text{OOD}}$ is out-of-distribution generalization, $H_{\pi}$ is policy entropy (sampling diversity), and $G_{\text{RL}}$ is the gain from continuing RL starting from that checkpoint. When these signals appear together, piling on more SFT tends to bring overfitting, templatization, and a shrinking exploration space.

## 1. What does SFT actually solve?

SFT is essentially **behavior cloning**, and it is best at four kinds of problems.

1. **Interaction protocol.** This covers the chat template, system/user/assistant role boundaries, JSON schema, tool-call format, stop tokens, and refusal format. These are usually best learned via SFT.
2. **Task expression.** This is about whether the model understands the input/output form of the target scenario and can organize answers, fill fields, choose tools, and handle multi-turn interaction per the business definition.
3. **Domain-knowledge expression.** SFT can make a model use domain terminology, reasoning patterns, and target style more stably, but it is *not* a good vehicle for large-scale knowledge injection. If the model genuinely lacks the knowledge, prefer continued pretraining, RAG, or high-quality domain-data augmentation.
4. **RL initialization.** For math, code, tool-use, and agentic tasks, SFT's goal is not the final optimal model. Instead it gives the policy basic task understanding, format stability, and effective sampling, so that RL has a good starting point.

## 2. The core metrics

Train loss or validation loss alone is **not enough** to judge whether SFT is finished. Watch these dimensions instead:

| Dimension | Example metrics |
|---|---|
| Fit state | train loss, valid loss, assistant-token NLL |
| Task ability | pass@1, accuracy, F1, tool success rate, JSON-valid rate |
| Generalization | OOD set, hard set, unseen benchmark, long-tail queries |
| Protocol stability | schema-valid rate, role-violation rate, stop rate, tool-argument-valid rate |
| Output distribution | entropy, distinct-$n$, self-consistency gain, average length, templatization rate |
| Room for RL | pass@k, pass@large-$k$, RL-probe gain |
| Regression risk | general-benchmark regression, safety-refusal rate, hallucination rate, over-refusal rate |

The most decisive signals are not loss but the **OOD/hard set, pass@large-$k$, and RL-probe gain**. A high post-SFT score does not guarantee a better *final* model. Recent SFT→RL studies show repeatedly that post-SFT and post-RL metrics are not always positively correlated, because over-SFT can raise short-term supervised eval scores while reducing sampling diversity and later RL gains.

## 3. Signals that SFT is *not yet* done

- The model still makes obvious protocol errors, such as unstable tool-call format, frequently illegal JSON, confused role boundaries, and inconsistent refusals. Basic behavior alignment is incomplete.
- Adding high-quality data still keeps improving the hard set, OOD set, and long-tail tasks. This matters especially for math, code, multi-hop reasoning, and complex tool calls, where a few examples fix only format and basic behavior, not the full capability distribution.
- pass@k is low overall, so the model struggles to generate correct trajectories anywhere in its sampling space. Jumping straight to RL here invites sparse rewards, training instability, and misguided exploration, so it is better to supplement high-quality SFT data first.

## 4. Signals that SFT has gone *too far*

- Train loss keeps dropping while dev/OOD/hard sets stop improving. The model is just fitting the annotation distribution better, not getting more capable.
- **Output templatization** sets in, with fixed openings, fixed endings, fixed reasoning format, fixed tool sequences, and converging answer lengths. This kills effective exploration in open-ended, multi-path, and agentic tasks.
- pass@1 rises slightly but **pass@k or self-consistency gain drops**. The model collapses toward a single mode and its sampling space narrows, which usually makes for a poor RL initialization.
- Running RL from that checkpoint yields smaller or even worse gains, because SFT has pushed the policy into too narrow a behavior distribution for RL to find useful signal by sampling.

## 5. How SFT should be done

The priority is **data quality, data structure, and training strategy**, not merely more data.

**Data.**

- Bucket by *capability*, not coarsely by source: general instruction, domain QA, math reasoning, code, tool calls, multi-turn dialogue, safety refusal, structured output, and long context. Track gains per bucket, or averages will mask local regressions.
- Control quality through clear task definitions, verifiable answers, consistent format, non-repetitive expression, and a sensible difficulty spread. Synthetic data from a strong teacher must pass dedup, rule checks, LLM-as-judge, diversity filtering, and human spot-checks. For code/math/tool-use, add execution or rule verification.
- Do not train only on short and easy samples. They inflate SFT metrics but do not necessarily help RL. Agentic data must cover varied trajectory lengths, tool combinations, error recovery, and edge cases, or the model learns too narrow a behavior pattern.

**Training.**

- Run a **checkpoint sweep**, and do not default to the last checkpoint. Learning rate, epochs, batch size, warmup, and loss-mask strategy all move the result significantly. Compute loss only on assistant tokens, and for multi-turn and tool-call data, decide explicitly whether to train intermediate assistant actions, whether to train the final reply, and whether to mask tool observations.
- Select the checkpoint by more than the post-SFT score alone. A more robust criterion is a protocol that is stable, hard/OOD sets that are not regressing, pass@k that is still high, diversity that is not collapsing, and a small-scale **RL probe** showing a clear gain.

## 6. The boundary between SFT and RL

SFT addresses *whether the model knows how to answer*. RL addresses *which of several candidate behaviors is better*.

- When the model cannot follow format, call tools, or complete the basic task, do SFT first.
- When it can sample correct answers but pass@1 is unstable, or when candidate quality varies a lot, move to preference tuning, DPO, PPO, GRPO, or RLVR.

For verifiable tasks (math, code, agentic tool-use) RL's value is usually higher, because there is a clear outcome signal and the correct trajectory may not be unique. SFT can only imitate existing trajectories, whereas RL can optimize the policy distribution against the final result.

But RL also depends on SFT initialization. With too little SFT the model cannot produce effective trajectories, and with too much the sampling distribution is too narrow for RL to explore. So the goal of SFT is **not** to push supervised metrics to the maximum. It is to obtain a stable, controllable policy that still has room for later optimization.

---

*Note: these notes are compiled from sources on the internet and are not my original work. I plan to rewrite them in my own words later.*
