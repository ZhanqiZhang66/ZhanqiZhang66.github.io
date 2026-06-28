---
layout: post
title: "Vision and Language"
subtitle: "A double helix"
tags: [tutorials, vision, multimodal, deep-learning, notes]
cover-img: /assets/img/blog/covers/vision-language.svg
head-extra: [mathjax.html]
---

## Why redraw the map

Over the past decade, under the single banner of "deep learning," NLP and CV actually walked two rather different roads. NLP completed an architecture-level convergence in 2017, the year every task was eventually swallowed by the Transformer. CV took longer, because of the continuity of its input signal and the strong heterogeneity of its tasks (classification, detection, segmentation, generation, 3D reconstruction, video understanding). It converged three-to-five years later, and is still not fully finished today.

The best way to understand modern vision is not as a list of isolated SOTA models, but as **a coupled system in continuous "technological contagion" with NLP.** Every paradigm leap in NLP reappears in vision, in some deformed shape, within three to five years. Just as importantly, vision sends back insights NLP could not produce on its own: iterative-denoising generation, the effectiveness of discriminative self-supervision, and the tension between representation and generation.

This map places four parallel-evolving threads (**discriminative representation learning, generative models, multimodal alignment, and 3D / world models**) on a single timeline, marking their branch points, confluences, and the cracks still unbridged.

## 1. The skeleton: four threads and four contagions

### 1.1 The full evolution

| NLP | Understanding | Generation | Multimodal | 3D / World |
|---|---|---|---|---|
| Word2Vec | AlexNet, ResNet | GAN |  |  |
| Transformer, BERT, GPT-2 | (CNN still dominant) | VAE, VQ-VAE |  |  |
| GPT-3, Scaling Laws | ViT, MoCo, DINO | DDPM | CLIP | NeRF |
| ChatGPT, RLHF | MAE, DINOv2 | LDM (SD), DiT | BLIP, Flamingo, LLaVA | 3DGS |
| GPT-4o, o1, R1 | DINOv3 | SD3, FLUX, Sora | Qwen-VL, Chameleon, Janus | TRELLIS, V-JEPA, Cosmos, Genie |

The four threads are not parallel and unrelated. They are stitched together by four "NLP→CV contagion events," and that is the map's real structure.

### 1.2 The four contagions

**First (2020): ViT** moved the Transformer into vision verbatim. On the surface it is "swap a backbone"; the deeper meaning is a principle: *on sufficiently large data, inductive bias is a burden, not an advantage.* CNN's translation equivariance, locality, and hierarchical receptive fields are priors, and priors are regularization on small data but a ceiling on large data. The judgment still holds, yet it raises an open question. **What prior of the visual signal is truly irreplaceable: spatial locality, scale invariance, or some geometric structure we have not yet formalized?**

**Second (2021 to 2022): self-supervision** crossed from NLP into vision. NLP's BERT/GPT paradigm is "predicting the masked part is a free lunch," but the vision community branched on the first translation: MAE chose pixel reconstruction (mimicking BERT), while DINO chose teacher-student self-distillation (which has no NLP counterpart). DINOv2's later strength shows that **reconstructive and discriminative SSL do not learn the same kind of information**, because reconstruction must preserve high-frequency detail that is nearly useless for downstream understanding. This is an original vision finding: in pixel space there is a non-negligible gap between "enough to reconstruct" and "enough to understand."

**Third (2023 to 2024): the Scaling Law** fully entered vision. NLP's scaling law was set by Kaplan et al. in 2020; vision got the "data scale × model scale × data quality" flywheel running only with DINOv2, and the generation line only once DiT replaced the U-Net with a Transformer and drew FID monotonically falling with compute. DiT's real contribution is not "Transformer for diffusion" but proving that **generative models also obey scaling laws**, the key step that pulled vision into the LLM rulebook.

**Fourth (2024 to 2026): training paradigms began to unify.** Chameleon, Janus, and GPT-4o share one claim: understanding and generation are no longer two things, but should share one autoregressive backbone. If this truly works, the boundary of vision as an independent field begins to dissolve, and it becomes a submodule of multimodal foundation models.

## 2. The discriminative-representation thread: from CNN to DINOv3

### 2.1 The skeleton and each step's delta

The question never changes: **given an image, how do we learn a feature useful for every downstream task?**

| Node | Core delta vs the previous step |
|---|---|
| ViT | removes CNN's inductive bias |
| MoCo / DINO | learns usable features with no labels |
| MAE | pixel reconstruction as SSL |
| DINOv2 | data scale + distillation + stable training |
| DINOv3 | further extrapolates scale and multi-resolution |

ResNet solved the optimization of deep networks via residual connections, but still assumed vision is local, hierarchical, and translation-equivariant. ViT tore those assumptions out, cut the image into patches, fed them as a token sequence, and handed "what is a reasonable visual prior" back to the data. MoCo and DINO brought contrastive learning and self-distillation, enabling label-free ViT training. MAE masked 75% of patches and reconstructed them, importing BERT-style SSL. DINOv2 truly completed the "backbone + self-supervision + large-scale data" trinity, with features that for the first time matched or beat supervised features without fine-tuning. DINOv3 then pushed scale and training stability further.

### 2.2 An often-ignored tension

Discriminative and reconstructive SSL give *non-equivalent* features in vision, something that barely holds in NLP, where BERT's MLM and contrastive SimCSE differ far less downstream than MAE and DINOv2 do in vision. This raises an open question. **Is the difference a direct consequence of the visual signal being "low density" in the information-theoretic sense?** Most pixel bits encode high-frequency texture unrelated to semantics; reconstruction must keep those bits, while contrastive and distillation objectives can discard them. If so, the design principle for visual SSL should be "specify what to throw away," not "preserve everything in full," which is almost the opposite of NLP's philosophy.

## 3. The generative thread: from GAN to Flow Matching

### 3.1 The skeleton and each step's delta

The question: **how do we model and sample from a high-dimensional continuous distribution $p(x)$?**

| Node | Core delta vs the previous step |
|---|---|
| VAE | explicit probabilistic framework |
| VQ-VAE | discrete latent, recast as sequence modeling |
| DDPM | iterative denoising, decomposing a hard problem |
| LDM | diffusion in latent space, controllable generation |
| DiT | Transformer-ized, scaling law established |
| SD3 / FLUX | Flow Matching, releasing constrained degrees of freedom |

GAN learns a sampler directly via an adversarial game, skipping explicit probability modeling, but it is unstable and mode-collapses. VAE gives a probabilistic frame but blurry samples. VQ-VAE introduces a discrete latent, turning generation into token-sequence modeling and making the autoregressive path viable on images for the first time. DDPM redefines generation as iterative denoising: it splits "one step from noise to image" into thousands of small steps, each learning only a simple denoiser. LDM (Stable Diffusion) moves diffusion into the VAE's latent space, slashing cost and making conditional control (text, depth, pose) natural. DiT swaps LDM's U-Net for a Transformer and establishes diffusion's scaling law. SD3 and FLUX bring Flow Matching, recasting diffusion from "learn to denoise" into "learn the optimal-transport vector field," which is more elegant in theory and faster-converging in practice. Sora and Veo3 extend into video, and TRELLIS into 3D.

### 3.2 Why three generation routes still do not converge

NLP has only one generation route: autoregression. Vision keeps three alive at once, namely autoregression (Parti, Chameleon), diffusion (SD, DiT), and Flow Matching (FLUX, SD3). A direct explanation is that on continuous high-dimensional signals, iterative denoising suits the problem better than a single autoregressive pass, because each denoising step only solves the local problem of "fine-tuning on top of an already-rough structure." A deeper explanation is that **autoregression implies an ordering assumption** (what to generate first, then next), but a 2D image has no natural causal order, and forcing one (raster scan) injects significant bias. Diffusion and Flow Matching have no such order, since they apply tiny corrections to the whole image at once. That leaves an open question: if tokenizers improve to find a "natural order" for images (by saliency or frequency decomposition), could autoregression catch up to diffusion again? Chameleon's existence shows the path is not dead.

### 3.3 The duality of representation and generation

There is a rarely stated connection here: **discriminative representation learning and generative modeling are two directions of the same problem.** DINOv2 learns $p(z \mid x)$ (image → semantics); DiT learns $p(x \mid z)$ (semantics → image). Yet no model has truly unified the two directions in one backbone, and vision backbones and generation backbones are still trained and deployed separately. This contrasts sharply with NLP, where GPT both understands and generates with one model. Why can vision not? One likely reason is the non-unified tokenizer: DINOv2 uses patch tokens but does not require invertibility, while DiT and SD3 use VAE latents that must be invertible. Once representation space and generation space cannot be inter-translated, unification is off the table.

## 4. The multimodal-alignment thread: from CLIP to native multimodality

| Node | Core delta vs the previous step |
|---|---|
| CLIP | rewrites classification as matching |
| BLIP / Flamingo | plugs into LLMs, unifies many tasks |
| LLaVA | minimal alignment, proves architecture is not the bottleneck |
| Qwen-VL / GPT-4V | data scale and alignment precision |
| Chameleon / Janus | native multimodality, one backbone for understanding and generation |

CLIP trained dual-tower contrastive learning on 400M image-text pairs, rewriting classification from closed-set matching (image → class id) to open-set matching (image → text description). The power of that rewrite is badly underrated, because it is not a new model but a **redefinition of "classification"**: anything describable in text becomes classifiable, and zero-shot ability emerges. BLIP and Flamingo wired visual encoders into language models, opening up VQA and captioning. LLaVA proved with a minimal recipe (one projection layer + instruction tuning) that vision-language alignment needs no complex architecture. Qwen-VL, InternVL, and GPT-4V then pushed scale and alignment precision. The newest stage is native multimodality: Chameleon, Janus, and GPT-4o no longer train the visual encoder and language model separately, but use one Transformer over discrete text and discrete visual tokens, sharing parameters for understanding and generation.

### 4.1 A seldom-discussed asymmetry

After CLIP, nearly all multimodal work defaults to "text is the anchor, vision aligns to text." The reverse direction, letting text align to vision, is almost unexplored. Behind it sits an implicit assumption: **language space is a good approximation of semantic space.** Is that true? Visual concepts with no linguistic counterpart (a specific material's sheen, a particular usage) suggest otherwise.

## 5. The 3D / world-model thread, and a methodology

V-JEPA, Cosmos, and Genie bring video and physical interaction into view, beginning to attempt **world models**: not merely generating pixels, but generating dynamic environments an agent can interact with.

TRELLIS offers an overlooked methodological lesson: **when a field's downstream tasks are highly heterogeneous, unify the representation first and model design simplifies on its own.** Once SLAT closed the representation gap, the generation stage simply reused mature 2D Rectified Flow with almost no architectural novelty. This parallels NLP exactly, since Word2Vec and the Transformer both first solved "how is language represented," and only then did architectures explode. Which other fields are bottlenecked by representation rather than model strength? Robotic control, chemical molecules, and protein dynamics all seem to fit.

## 6. Confluence and cracks

### 6.1 Confluence: Transformer and Scaling Law

By 2026 the four threads have converged on two levels: architecture (all Transformer-ized) and training objective (all guided by scaling laws). From the outside, vision models and language models look more and more like different instances of the same thing.

### 6.2 The unbridged cracks

| Crack | Current state |
|---|---|
| Tokenizer not unified | patch, VQ, continuous latent: a three-way standoff |
| Generation route not unified | autoregression, diffusion, Flow Matching coexist |
| Representation vs generation not unified | DINOv2 and DiT remain separate |
| Data scale not matched | visual data far scarcer than language; SSL still key |
| Multimodal directionality unequal | text is the anchor; vision aligns one-way |

Each crack is a latent chance for a paradigm leap. If a new tokenizer could inter-translate discriminative features and generative latents, DINOv2 and DiT might merge into one model. If a new training objective could balance discriminative SSL's efficiency with generative SSL's coverage, the very concept of a "backbone" could be rewritten.

The map's purpose is not to give answers but to show that vision is best read as one half of a double helix, winding around language, trading paradigms in both directions, and still carrying the seams where the two strands have not yet fused.