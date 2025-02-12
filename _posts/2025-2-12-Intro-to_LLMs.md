---
layout: post
title: Intro to LLMs
subtitle: 
gh-repo: zhanqizhang66/zhanqizhang66.github.io/
gh-badge: [star, fork, follow]
cover-img: /assets/img/photograph/281AB3B5-547A-4CE3-BDAF-E0C43AEC29DE.jpg
thumbnail-img:
share-img: /assets/img/photograph/281AB3B5-547A-4CE3-BDAF-E0C43AEC29DE.jpg
tags: [tutorials]
---


# Introduction to Large Language Models (LLMs)

## Overview  
This journal-club presentation provides a comprehensive introduction to Large Language Models (LLMs), covering their background, modeling techniques, adaptation methods, and future directions.

## Outline  
- **LM Background**: Evolution from traditional Language Models (LMs) to LLMs  
- **LLM Modeling and Pre-training**: Transformer architectures and training approaches  
- **Adaptation to Downstream Tasks**: Fine-tuning, prompting, and task-specific adaptations  
- **Scaling and Modern LLMs**: GPT-4, DeepSeek, and efficiency optimizations  
- **Future Perspectives**: Multi-modal models, scaling laws, and ethical concerns  

---

## Language Models (LMs)  
- **LM Definition**: Probability distribution over a sequence of tokens  
- **Autoregressive LMs**: Token generation based on prior context  
- **Evolution to LLMs**: N-gram models → RNNs → Transformers  

## Transformer-Based LLMs  
- **Key Components**: Self-attention, positional encoding, masked training  
- **Architectures**:  
  - **Encoder-only** (e.g., BERT, RoBERTa) – best for classification tasks  
  - **Decoder-only** (e.g., GPT-3, ChatGPT) – ideal for generative tasks  
  - **Encoder-decoder** (e.g., T5, BART) – used for translation and structured tasks  

---

## Adapting LLMs to Tasks  
- **Supervised Fine-Tuning**: Optimizing models for specific applications  
- **Lightweight Fine-Tuning**: Efficient tuning with minimal parameter updates (e.g., LoRA, BitFit)  
- **Prompting Strategies**: Zero-shot, one-shot, few-shot learning  

---

## Scaling Laws & Model Comparisons  
- **GPT-4o**: Multimodal expansion with 1.8T parameters and 128k token context window  
- **DeepSeek-R1**: Efficient MoE-based training with reduced GPU requirements  
- **Comparison of LLMs**: Trade-offs in efficiency, inference speed, and adaptability  

---

## Future of LLMs  
- **Data Considerations**: Privacy, fairness, contamination risks  
- **Multi-Modality**: Integration of text, images, and audio (e.g., CLIP, GPT-4V)  
- **Beyond Transformers?**: Exploring alternative architectures for next-gen AI  

---

## Resources  
- **Courses**:  
  - [Stanford CS324 (Winter 2022)](https://stanford-cs324.github.io/winter2022/)  
  - [Stanford CS324 (Winter 2023)](https://stanford-cs324.github.io/winter2023/)  
- **Review Papers**:  
  - [Survey on LLMs (2023)](https://arxiv.org/pdf/2303.18223)  
  - [Recent Advances in LLMs (2023)](https://arxiv.org/pdf/2307.06435)  
- **Paper Lists & Blog Posts**:  
  - [Awesome LLM GitHub Repository](https://github.com/Hannibal046/Awesome-LLM)  
  - [Why Most LLMs are Decoder-Only](https://medium.com/@yumo-bai/why-are-most-llms-decoder-only-590c903e4789)  
*Note: Many slides in this presentation were adapted from Changhao Shi.*

---
<iframe width="100%" height="800" src="/files/intro_to_llms.pdf">


