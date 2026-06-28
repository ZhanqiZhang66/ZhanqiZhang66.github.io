---
layout: post
title: "How to Tell When SFT Is Done"
subtitle: "Why lower loss is the wrong target, and which signals say supervised fine-tuning has hit diminishing returns"
tags: [tutorials, llm, post-training, sft, rl, notes]
head-extra: [mathjax.html]
---

In LLM post-training, **SFT** (supervised fine-tuning) usually handles cold-start, behavior formatting, and task-protocol learning. But longer SFT is not always better, and lower loss is not always better. Judging whether SFT is "done" hinges not on how well it fits the training set, but on whether continued supervised imitation still produces stable **generalization** gains — and whether it still preserves room for a subsequent **RL** stage.

A more reasonable criterion: when adding more SFT data, more epochs, or higher training intensity makes dev-set gains plateau, when OOD and hard sets stop improving, when the output distribution begins to shrink, when pass@k diversity drops, and when the magnitude of later RL gains shrinks — then SFT has basically entered a very-low-marginal-return phase.

Formally, "SFT is done" can be read as the simultaneous condition:

$$
\Delta S_{\text{dev}} \approx 0, \quad
\Delta S_{\text{OOD}} \le 0, \quad
\Delta H_{\pi} < 0, \quad
\Delta G_{\text{RL}} \le 0
$$

where $S_{\text{dev}}$ is dev-set capability, $S_{\text{OOD}}$ is out-of-distribution generalization, $H_{\pi}$ is policy entropy (sampling diversity), and $G_{\text{RL}}$ is the gain from continuing RL starting from that checkpoint. When these signals appear together, piling on more SFT tends to bring overfitting, templatization, and shrinking exploration space.

## 1. What does SFT actually solve?

SFT is essentially **behavior cloning**, and it is best at four kinds of problems.

1. **Interaction protocol** — chat template, system/user/assistant role boundaries, JSON schema, tool-call format, stop tokens, refusal format. These are usually best learned via SFT.
2. **Task expression** — whether the model understands the input/output form of the target scenario and can organize answers, fill fields, choose tools, and handle multi-turn interaction per the business definition.
3. **Domain-knowledge expression** — SFT can make a model use domain terminology, reasoning patterns, and target style more stably, but it is *not* a good vehicle for large-scale knowledge injection. If the model genuinely lacks the knowledge, prefer continued pretraining, RAG, or high-quality domain-data augmentation.
4. **RL initialization** — for math, code, tool-use, and agentic tasks, SFT's goal is not the final optimal model but giving the policy basic task understanding, format stability, and effective sampling, so RL has a good starting point.

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

The most decisive are not loss but **OOD/hard set, pass@large-$k$, and RL-probe gain**. A high post-SFT score does not guarantee a better *final* model. Recent SFT→RL studies show repeatedly that post-SFT and post-RL metrics are not always positively correlated: over-SFT can raise short-term supervised eval scores while reducing sampling diversity and later RL gains.

## 3. Signals that SFT is *not yet* done

- The model still makes obvious protocol errors — unstable tool-call format, frequently illegal JSON, confused role boundaries, inconsistent refusals. Basic behavior alignment is incomplete.
- Adding high-quality data still keeps improving the hard set, OOD set, and long-tail tasks. Especially for math, code, multi-hop reasoning, and complex tool calls, a few examples fix only format and basic behavior, not the full capability distribution.
- pass@k is low overall — the model struggles to generate correct trajectories anywhere in its sampling space. Jumping straight to RL here invites sparse rewards, training instability, and misguided exploration; supplement high-quality SFT data first.

## 4. Signals that SFT has gone *too far*

- Train loss keeps dropping while dev/OOD/hard sets stop improving — the model is just fitting the annotation distribution better, not getting more capable.
- **Output templatization** — fixed openings, fixed endings, fixed reasoning format, fixed tool sequences, converging answer lengths. This kills effective exploration in open-ended, multi-path, and agentic tasks.
- pass@1 rises slightly but **pass@k or self-consistency gain drops** — the model collapses toward a single mode and its sampling space narrows. Usually a poor RL initialization.
- Running RL from that checkpoint yields smaller or even worse gains — SFT has pushed the policy into too narrow a behavior distribution for RL to find useful signal by sampling.

## 5. How SFT should be done

Priority is **data quality, data structure, and training strategy** — not merely more data.

**Data.**

- Bucket by *capability*, not coarsely by source: general instruction, domain QA, math reasoning, code, tool calls, multi-turn dialogue, safety refusal, structured output, long context. Track gains per bucket, or averages will mask local regressions.
- Control quality: clear task definitions, verifiable answers, consistent format, non-repetitive expression, sensible difficulty spread. Synthetic data from a strong teacher must pass dedup, rule checks, LLM-as-judge, diversity filtering, and human spot-checks. For code/math/tool-use, add execution or rule verification.
- Do not train only short and easy samples. They inflate SFT metrics but do not necessarily help RL. Agentic data must cover varied trajectory lengths, tool combinations, error recovery, and edge cases, or the model learns too narrow a behavior pattern.

**Training.**

- Run a **checkpoint sweep**; do not default to the last checkpoint. Learning rate, epochs, batch size, warmup, and loss-mask strategy all move the result significantly. Compute loss only on assistant tokens; for multi-turn and tool-call data, decide explicitly whether to train intermediate assistant actions, the final reply, and whether to mask tool observations.
- Select the checkpoint not by post-SFT score alone. A more robust criterion: protocol stable, hard/OOD not regressing, pass@k still high, diversity not collapsing, and a small-scale **RL probe** showing a clear gain.

## 6. The boundary between SFT and RL

SFT addresses *whether the model knows how to answer*. RL addresses *which of several candidate behaviors is better*.

- When the model cannot follow format, call tools, or complete the basic task — do SFT first.
- When it can sample correct answers but pass@1 is unstable, or candidate quality varies a lot — move to preference tuning, DPO, PPO, GRPO, or RLVR.

For verifiable tasks (math, code, agentic tool-use) RL's value is usually higher: there is a clear outcome signal and the correct trajectory may not be unique. SFT can only imitate existing trajectories; RL can optimize the policy distribution against the final result.

But RL also depends on SFT initialization. Too little SFT and the model cannot produce effective trajectories; too much and the sampling distribution is too narrow for RL to explore. So the goal of SFT is **not** to push supervised metrics to the maximum — it is to obtain a stable, controllable policy that still has room for later optimization.

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
