---
layout: post
title: But, what is Attention in transformers?
subtitle: Q,K,V, with code snippets
gh-repo: zhanqizhang66/zhanqizhang66.github.io
gh-badge: [star, fork, follow]
cover-img: /assets/img/photograph/19AF8CFD-3763-4B3F-8735-AA01887F3315.jpg
thumbnail-img:
share-img: /assets/img/photograph/19AF8CFD-3763-4B3F-8735-AA01887F3315.jpg
tags: [learning notes]
---


<h2>‘All’ you need to know about transformer</h2>

Attention is well used in modern transformer learning models. Okay, but what is attention exactly? I often find myself going back to the great work "Attention is all you need" over and over again when I need to explain the concept to others and to myself.

As an engineer, I found it useful to understand math through code, so inspired by [Jacob Gildenblat's post on explainability of vision transformers](https://jacobgil.github.io/deeplearning/vision-transformer-explainability), I made this attention learning note with code snippets in PyTorch.

For Q, K, V, attention, and transformer model, there is visual illustration along with detailed code snippets for each concept/math equation.



<iframe width="100%" height="800" src="/files/Exploring Explainability for Vision Transformers.pdf">

* Update
Pytorch released a blog on the [visulization inside the matrix](https://pytorch.org/blog/inside-the-matrix/)
For example, a matmul computation can be visualized 
```
L @ R
```
![Matmul](https://pytorch.org/assets/images/inside-the-matrix/initial.jpg)
More matrices multiplication
```
A @ B @ C
```
![nlayerbottleneck](https://pytorch.org/assets/images/inside-the-matrix/nlayerbottleneck.jpg)
```
Inside the attention head
Q = input @ wQ        // 1
K_t = wK_t @ input_t  // 2
V = input @ wV        // 3
attn = sdpa(Q @ K_t)  // 4
head_out = attn @ V   // 5
out = head_out @ wO   // 6
```
![nlayerbottleneck](https://pytorch.org/assets/images/inside-the-matrix/mha1.jpg)



Reference other the papers cited in the pdf:
+ [Vision Transformer Tutorial Google Colab](https://colab.research.google.com/github/hirotomusiker/schwert_colab_data_storage/blob/master/notebook/Vision_Transformer_Tutorial.ipynb)
+ [Illustrated self attention](https://towardsdatascience.com/illustrated-self-attention-2d627e33b20a)
+ [Jacob Gildenblat's post on explainability of vision transformers](https://jacobgil.github.io/deeplearning/vision-transformer-explainability)
+ [PyTorch visulization inside the matrix](https://pytorch.org/blog/inside-the-matrix/)


	