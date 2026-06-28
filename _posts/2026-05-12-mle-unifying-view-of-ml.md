---
layout: post
title: "Maximum Likelihood Estimation as a Unifying View of ML"
subtitle: "From linear regression to GPT, most training losses are just negative log-likelihood under a probabilistic model"
tags: [machine-learning, statistics, notes]
head-extra: [mathjax.html]
---

A large fraction of machine learning can be viewed as:

```text
Choose a probabilistic model
        ↓
Write likelihood
        ↓
Take log likelihood
        ↓
Maximize likelihood
        ↓
Equivalent to minimizing negative log likelihood
        ↓
Obtain the training loss
```

---

# General Framework

Assume data is generated from a probabilistic model:

$$
p(y \mid x; \theta)
$$

where:

- $$x$$ = input
- $$y$$ = target
- $$\theta$$ = model parameters

Given dataset:

$$
\{(x_i, y_i)\}_{i=1}^{N}
$$

Assuming samples are independent, the likelihood is:

$$
L(\theta)
=
\prod_{i=1}^{N}
p(y_i \mid x_i; \theta)
$$

Take the logarithm:

$$
\log L(\theta)
=
\sum_{i=1}^{N}
\log p(y_i \mid x_i; \theta)
$$

Training objective:

$$
\max_{\theta} \log L(\theta)
$$

Equivalent to:

$$
\min_{\theta} -\log L(\theta)
$$

So the loss is often:

$$
\boxed{
\text{Loss} = -\log \text{Likelihood}
}
$$

---

# 1. Linear Regression → Mean Squared Error (MSE)

## Probabilistic Assumption

Assume Gaussian noise:

$$
y \mid x
\sim
\mathcal{N}(f_\theta(x), \sigma^2)
$$

Meaning:

$$
p(y \mid x; \theta)
=
\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\left(
-\frac{(y - f_\theta(x))^2}{2\sigma^2}
\right)
$$

For all samples:

$$
L(\theta)
=
\prod_{i=1}^{N}
p(y_i \mid x_i; \theta)
$$

Take log:

$$
\log L(\theta)
=
\sum_{i=1}^{N}
\log p(y_i \mid x_i; \theta)
$$

Substitute Gaussian density:

$$
=
\sum_{i=1}^{N}
\left[
-\frac{(y_i - f_\theta(x_i))^2}{2\sigma^2}
-\log \sqrt{2\pi\sigma^2}
\right]
$$

Constants do not affect optimization, so:

$$
\max_\theta \log L(\theta)
$$

is equivalent to:

$$
\min_\theta
\sum_{i=1}^{N}
(y_i - f_\theta(x_i))^2
$$

Final loss:

$$
\boxed{
\text{MSE Loss}
=
\sum_i (y_i - \hat y_i)^2
}
$$

---

# 2. Logistic Regression → Binary Cross Entropy

## Probabilistic Assumption

Assume Bernoulli outputs:

$$
y \mid x
\sim
\text{Bernoulli}(p_\theta(x))
$$

where:

$$
p_\theta(x)
=
\sigma(f_\theta(x))
=
\frac{1}{1+e^{-f_\theta(x)}}
$$

Bernoulli probability mass function:

$$
p(y \mid x; \theta)
=
p_\theta(x)^y
(1-p_\theta(x))^{1-y}
$$

Likelihood:

$$
L(\theta)
=
\prod_{i=1}^{N}
p_\theta(x_i)^{y_i}
(1-p_\theta(x_i))^{1-y_i}
$$

Take log:

$$
\log L(\theta)
=
\sum_{i=1}^{N}
\left[
y_i \log p_\theta(x_i)
+
(1-y_i)\log(1-p_\theta(x_i))
\right]
$$

Training objective:

$$
\max_\theta \log L(\theta)
$$

Equivalent to minimizing negative log likelihood:

$$
\min_\theta
-\sum_{i=1}^{N}
\left[
y_i \log p_\theta(x_i)
+
(1-y_i)\log(1-p_\theta(x_i))
\right]
$$

Final loss:

$$
\boxed{
\text{Binary Cross Entropy}
=
-\sum_i
\left[
y_i \log p_i
+
(1-y_i)\log(1-p_i)
\right]
}
$$

---

# 3. Softmax Classification → Multiclass Cross Entropy

## Probabilistic Assumption

Assume categorical outputs:

$$
y \mid x
\sim
\text{Categorical}(p_1, p_2, \dots, p_K)
$$

where:

$$
p_k
=
\frac{e^{z_k}}
{\sum_j e^{z_j}}
$$

(softmax)

Probability of true class:

$$
p(y=k \mid x)=\text{softmax}(z_k)
$$

Likelihood for dataset:

$$
L(\theta)
=
\prod_{i=1}^{N}
p(y_i \mid x_i)
$$

Take log:

$$
\log L(\theta)
=
\sum_{i=1}^{N}
\log p(y_i \mid x_i)
$$

Maximize likelihood:

$$
\max_\theta
\sum_i \log p(y_i \mid x_i)
$$

Equivalent to minimizing:

$$
\min_\theta
-\sum_i \log p(y_i \mid x_i)
$$

Final loss:

$$
\boxed{
\text{Cross Entropy Loss}
=
-\sum_i \log p(y_i)
}
$$

---

# 4. Language Models (GPT) → Token Cross Entropy

## Probabilistic Assumption

Language modeling assumes:

$$
p(x_1, x_2, \dots, x_T)
=
\prod_{t=1}^{T}
p(x_t \mid x_{<t})
$$

Each token depends on previous tokens.

Likelihood:

$$
L(\theta)
=
\prod_{t=1}^{T}
p(x_t \mid x_{<t}; \theta)
$$

Take log:

$$
\log L(\theta)
=
\sum_{t=1}^{T}
\log p(x_t \mid x_{<t}; \theta)
$$

Training objective:

$$
\max_\theta
\sum_{t=1}^{T}
\log p(x_t \mid x_{<t}; \theta)
$$

Equivalent to minimizing:

$$
\min_\theta
-\sum_{t=1}^{T}
\log p(x_t \mid x_{<t}; \theta)
$$

Final loss:

$$
\boxed{
\text{Token Cross Entropy}
=
-\sum_t \log p(x_t \mid x_{<t})
}
$$

GPT training is literally maximum likelihood estimation over next-token probabilities.

---

# Summary Table

| Model | Probabilistic Assumption | Final Loss |
|---|---|---|
| Linear Regression | $$y \mid x \sim \mathcal{N}(f_\theta(x), \sigma^2)$$ | MSE |
| Logistic Regression | $$y \mid x \sim \text{Bernoulli}(p_\theta(x))$$ | Binary Cross Entropy |
| Softmax Classifier | $$y \mid x \sim \text{Categorical}(p)$$ | Multiclass Cross Entropy |
| GPT / Language Model | $$p(x_t \mid x_{<t})$$ | Token Cross Entropy |

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
