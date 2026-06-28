---
layout: post
title: "AI Infra: A Map of Schedulable Resources, Tricks, and Hardware"
subtitle: "Every optimization trades one resource dimension for another — here is the full inventory and what each trick is really swapping"
tags: [llm, gpu, infra, performance, notes]
head-extra: [mathjax.html]
---

There is only one core thesis: **the essence of every optimization is to *trade* one resource dimension for another.** Only once you can see the full list of resources and their physical carriers can you judge what a trick is really swapping — and when it should not be used at all.

## I. Three mental models

### Model 1 — resources have only three dimensions

Any hardware resource has, in essence, only three consumable or contended dimensions:

| Dimension | Meaning | Bottleneck symptom |
|---|---|---|
| Capacity (byte) | how much fits at once | OOM, KV cache does not fit |
| Bandwidth (byte/s, FLOP/s) | how much is moved/computed per unit time | memory-bound, bandwidth saturated |
| Latency (s) | how long one operation waits | serial dependency, bubbles, launch stalling the CPU |

Latency usually cannot be eliminated directly — it can only be **hidden** with concurrency. That is the whole of Model 3.

### Model 2 — Roofline: where compute meets bandwidth

$$
\text{AI} = \frac{\text{FLOPs}}{\text{bytes moved}}, \qquad
\text{achievable} = \min\big(\text{Peak FLOPS}, \ \text{AI} \times \text{Peak BW}\big)
$$

The ridge point is $\text{AI}^{*} = \text{Peak FLOPS} / \text{Peak BW}$. Below it ($\text{AI} < \text{AI}^{*}$) you are memory-bound; above it, compute-bound. The H100's ridge is about $295$ FLOP/byte, the B200's about $281$ — barely moving over the years. Because compute grows faster than bandwidth, the ridge *rises* rather than falls, pushing more and more kernels into the memory-bound region. This is the quantitative statement of the **"memory wall."**

Large square matrices have high AI (compute-bound); thin-long matrices and small-batch decode have low AI (memory-bound). LLM decode is inherently memory-bound: each token requires reading all weights once, so $\text{AI} \approx \text{batch size}$, and only a large enough batch enters the compute-bound regime — exactly the physical motivation behind continuous batching and speculative decoding.

### Model 3 — hide latency with concurrency (Little's Law)

$$
\text{concurrency needed} = \text{latency} \times \text{throughput}
$$

Multi-warp hides memory latency, multi-stream hides kernel gaps, async copy hides H2D/D2H, overlap hides collective latency, double buffering hides load latency, pipelining hides cross-stage dependencies — all structurally identical, all "do B while waiting for A." The key corollary: **hiding latency only pays off when the hidden thing is actually the bottleneck.** If communication is only 5% of the time, hiding it into compute saves at most 5% — and may net-lose by contending for SMs and registers or by splitting kernels. Always profile the bottleneck's share first, then decide whether to hide it.

## II. Compute and storage units

**CUDA Core vs Tensor Core.** The former is a scalar ALU; the latter is a matrix MMA unit that computes a whole small tile per instruction, with one-to-two orders of magnitude higher throughput, born only for GEMM/convolution.

| Dimension | CUDA Core | Tensor Core |
|---|---|---|
| Primitive | scalar FMA | matrix MMA (one tile per instruction) |
| Use | LayerNorm / Softmax / RoPE / sampling | all large GEMM, attention |
| Throughput (H100) | FP32 ~67 TF | BF16 ~990 TF, FP8 ~1979 TF |
| Interface | ordinary CUDA / SIMT | wmma / wgmma, cuBLAS / CUTLASS |

An SM also contains independent units that can run in parallel with the main compute — the hardware basis for overlap:

| Unit | Function |
|---|---|
| SFU | transcendentals (exp/sin/rsqrt), without occupying CUDA Cores |
| Copy Engine / DMA | H2D/D2H copy, independent of the SM, so it can copy while computing |
| TMA (Hopper+) | async bulk global↔shared copy, with addresses computed in hardware |
| TMEM (Blackwell+) | dedicated Tensor Core accumulator memory, relieving register pressure |
| Transformer Engine | dynamically manages per-tensor scale for FP8/FP4 |

**The memory hierarchy is the optimization-space pyramid** (higher = faster and smaller). Keeping data one level higher for one more reuse is the essence of most kernel optimization.

| Layer | Location | Magnitude | Latency |
|---|---|---|---|
| Register file | per-thread | KB | ~0 |
| Shared Memory / L1 | per-SM | hundreds of KB | 20–30 cycles |
| L2 | whole-card shared | tens of MB | — |
| HBM / GDDR | whole card | tens–hundreds of GB | hundreds of cycles, 3–8 TB/s |
| Host DRAM | via PCIe / NVLink-C2C | — | 64 / 900 GB/s |
| Remote GPU / NVMe | NVLink / IB / storage | — | offload last resort |

## III. The full list of schedulable resources

The left column is what you schedule at the framework / training-stack level; the right is the physical carrier and its bottleneck signal.

| Abstract resource | Hardware carrier | Bottleneck signal |
|---|---|---|
| GEMM compute | Tensor Core | high Tensor-pipeline utilization |
| scalar/vector compute | CUDA Core + SFU | elementwise kernels dominate time |
| VRAM bandwidth | HBM↔L2↔L1↔registers | DRAM near peak, Tensor idle |
| VRAM capacity | HBM / GDDR | OOM, batch limited |
| on-chip memory | SMEM / registers / L2 | occupancy suppressed |
| concurrency / occupancy | warp slots, scheduler | active warps ≪ max |
| kernel launch | CPU main thread + driver | large gaps in the GPU timeline |
| host compute | CPU cores | CPU saturated, GPU waits on CPU |
| H2D / D2H | Copy Engine + PCIe / C2C | copy and compute not overlapped |
| intra-node interconnect | NVLink / NVSwitch / IF | NVLink bandwidth saturated |
| inter-node interconnect | NIC (IB/RoCE) + RDMA | cross-node collectives dominate |
| collective communication | NCCL / RCCL / HCCL | AllReduce / All2All tail latency |
| stream parallel / async | CUDA Stream + Event | single-stream serialization |
| L2 residency | L2 (settable persistence) | low L2 hit rate |
| power / thermal | TDP, clock | frequency throttled |
| card partitioning | MIG, SR-IOV | multi-tenant contention |

A few easily overlooked points: the **CPU launch thread** is a real bottleneck during decode (tens to hundreds of tiny kernels per step) — the entire reason CUDA Graph exists. The Copy Engine and the SMs are *separate* hardware, so copying does not consume compute — the physical prerequisite for "copy while computing." L2 can be actively pinned with `cudaAccessPolicyWindow` (it is not a fully automatic black box). NVLink-C2C (900 GB/s coherent memory) is far faster than PCIe (64 GB/s), so offload strategy differs accordingly. SHARP lets the switch do in-network reduction, completing half of an AllReduce's additions inside the network. Power is a whole-card shared budget, so a fully loaded GEMM triggers downclocking. The register file is a hard constraint on occupancy — using too much per thread leaves fewer warps resident.

## IV. The trick panorama: what each one trades

Arranged by acting layer, from low-level kernel to macro-level serving. The interesting columns are the last two: which bottleneck it removes, and when it is instead harmful.

| Trick | Layer | Target resource | When useless / harmful |
|---|---|---|---|
| Warp shuffle | Kernel | on-chip latency | cross-warp still needs SMEM |
| SMEM tiling | Kernel | VRAM bandwidth (↑AI) | suppresses occupancy |
| Vectorized memory access | Kernel | LD/ST issue | needs alignment, tail handling |
| cp.async / TMA | Kernel | hide memory latency | cannot hide if compute is too little |
| wgmma / tcgen05 | Kernel | Tensor utilization | needs TMA to feed it |
| Kernel fusion | Kernel | bandwidth + launch | fuse too large → register overflow |
| FlashAttention | Kernel | bandwidth + capacity | little benefit for very short sequences |
| CUDA Graph | Runtime | launch latency | dynamic shapes hard to capture |
| Persistent kernel | Runtime | launch + scheduling | load imbalance idles SMs |
| Multi-stream | Runtime | hide gaps | adds complexity without real parallelism |
| async copy + pinned | Runtime | hide H2D/D2H | no benefit off the critical path |
| Double buffering | Runtime | hide load latency | consumes extra capacity |
| Sync elimination | Framework | sync bubbles | wrongly removing breaks correctness |
| Mixed precision | Algorithm | compute + bandwidth + capacity | norm/gating must keep precision |
| FP8 / FP4 quantization | Algorithm | compute + bandwidth + capacity | useless if hardware unsupported |
| INT8 / weight-only | Algorithm | bandwidth + capacity | outliers, precision regression |
| KV-cache quantization | Serving | capacity + bandwidth | sensitive for long context |
| Tensor Parallel | Parallel | single-card compute + capacity | AllReduce per layer, needs fast interconnect |
| Pipeline Parallel | Parallel | capacity + cross-node bandwidth | pipeline bubbles |
| DP + ZeRO | Parallel | capacity (sharding) | insufficient bandwidth drags training |
| Expert Parallel | Parallel | capacity + compute (MoE) | if All2All is not the bottleneck, overlap is negative |
| Sequence / Context Parallel | Parallel | capacity (ultra-long sequence) | introduces extra communication |
| Compute–comm overlap | Parallel | hide collectives | net loss if communication is not the bottleneck |
| Continuous batching | Serving | compute utilization | no batch to assemble at very low concurrency |
| PagedAttention | Serving | capacity (defragmentation) | small indexing overhead |
| Chunked prefill | Serving | prefill/decode balance | too-fine chunks add scheduling overhead |
| Prefix / Radix cache | Serving | compute + bandwidth (reuse) | no benefit if prefix is not shared |
| PD disaggregation | Architecture | decouple compute vs bandwidth | KV transferred across nodes, interconnect must be fast |
| Speculative decoding | Algorithm | decode (memory-bound) | low acceptance / already compute-bound → small benefit |
| MTP / Medusa / EAGLE | Algorithm | same (built-in draft head) | training cost, acceptance depends on task |
| 2:4 structured sparsity | Algorithm | Tensor compute | needs sparsification training, precision may drop |

Mapping back to the three models: **bandwidth-savers** (fusion / Flash / tiling / quantization) raise AI, pushing memory-bound kernels toward compute-bound; **latency-hiders** (stream / async / overlap / PP) are Little's Law, valid only if the hidden thing is the bottleneck; **launch/sync reducers** (CUDA Graph, persistent kernels, sync elimination) remove CPU-side and synchronization serialization; **compute-changers** (quantization / Tensor Core / sparsity) raise peak FLOPS or lower the byte cost per FLOP; and **distributed tricks** (TP/PP/DP/EP/SP) trade communication for single-card capacity and compute.

## V. Real vendor hardware (mid-2026)

A note on reading specs: compute figures here default to **dense** values. Vendor spec sheets often default to 2:4 sparsity, roughly double the dense number (NVIDIA's "FP4 20 PFLOPS" for B200 is the sparse value; dense is ~9–10). Always align conventions when comparing across vendors.

**NVIDIA data center**

| Model | Arch | BF16 | FP8 | Memory | Bandwidth |
|---|---|---|---|---|---|
| H100 SXM | Hopper | 989 TF | 1,979 TF | 80 GB HBM3 | 3.35 TB/s (NVLink4 900) |
| H200 | Hopper | 989 | 1,979 | 141 GB HBM3e | ~4 TB/s |
| H20 (China SKU) | Hopper | ~148 | ~296 | 96 GB HBM3 | ~4 TB/s |
| B200 | Blackwell | 2,250 | 4,500 | 192 GB HBM3e | ~8 TB/s |
| B300 | Blackwell | — | ~7,000 | 288 GB HBM3e | ~8 TB/s |
| GB200 | Blackwell | 2×B200 | — | 384 GB + Grace | ~16 TB/s class |

The H20 is counterintuitive: its compute is cut to ~15% of the H100, but its 4 TB/s bandwidth is actually *higher* — so for memory-bound decode its value is not bad at all, a direct projection of the Roofline. Blackwell's 5th-gen Tensor Core adds FP4/FP6 microscaling, and the 2nd-gen Transformer Engine manages low-precision scales automatically. Roadmap: Vera Rubin NVL144 (2026) at 3.6 EFLOPS FP4 inference and HBM4 at 13 TB/s; Rubin Ultra NVL576 (2027) at 15 EFLOPS FP4.

**NVIDIA workstation / consumer**

| Model | CUDA Cores | Memory | Bandwidth | NVLink | TDP |
|---|---|---|---|---|---|
| RTX PRO 6000 Blackwell | 24,064 | 96 GB GDDR7 ECC | 1.79 TB/s | none | 600 W |
| RTX 5090 | 21,760 | 32 GB GDDR7 | 1.79 TB/s | none | 575 W |

Neither supports NVLink, so multi-card setups fall back to PCIe 5.0 (~64 GB/s one-way). For local TP/EP experiments, communication easily becomes the bottleneck — which is exactly what the resource map predicts.

---

*This post is part of a collected series of curated notes and has no formal references of its own.*
