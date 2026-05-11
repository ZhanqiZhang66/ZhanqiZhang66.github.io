---
layout: page
title: "Selected Projects"
subtitle: 
share-img: /assets/img/IMG_5259.jpg
cover-img:
  - "/assets/img/photograph/IMG_9057.jpeg" : "Black's beach, LA Jolla (2022)"
use-site-title: true
---
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Y06S3E3WTE"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Y06S3E3WTE');
</script>

### Conferences and Publications

<style>
.publication-row {
    display: flex;
    flex-direction: column;
    margin-bottom: 30px;
    padding: 22px 24px;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.publication-row:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}
.publication-content {
    display: contents;
}
.pub-title { order: 1; }
.pub-authors { order: 2; }
.pub-venue { order: 3; }
.publication-image { order: 4; }
.pub-abstract { order: 5; }
.publication-image {
    width: 100%;
    text-align: center;
    margin: 14px 0 16px 0;
}
.publication-image img {
    max-width: 100%;
    max-height: 460px;
    width: auto;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    object-fit: contain;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.publication-image img:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
}
.pub-title {
    font-size: 1.2em;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 8px;
    line-height: 1.3;
}
.pub-authors {
    font-size: 0.95em;
    color: #34495e;
    margin-bottom: 6px;
    font-weight: 500;
}
.pub-venue {
    font-style: italic;
    color: #7f8c8d;
    margin-bottom: 10px;
    font-size: 0.9em;
}
.pub-abstract {
    font-size: 0.92em;
    line-height: 1.6;
    color: #2c3e50;
    text-align: justify;
}
.pub-abstract ul {
    margin: 8px 0;
    padding-left: 20px;
}
.pub-abstract li {
    margin-bottom: 4px;
}
.pub-abstract details {
    margin-top: 4px;
}
.pub-abstract summary {
    cursor: pointer;
    font-weight: 600;
    color: #2c3e50;
    padding: 8px 10px;
    background: #eef2f5;
    border-radius: 6px;
    list-style: none;
    transition: background 0.2s ease;
    user-select: none;
}
.pub-abstract summary:hover {
    background: #e1e7ec;
}
.pub-abstract summary::-webkit-details-marker {
    display: none;
}
.pub-abstract summary::before {
    content: "▸ ";
    display: inline-block;
    transition: transform 0.2s ease;
    color: #5d7591;
}
.pub-abstract details[open] summary::before {
    content: "▾ ";
}
.pub-abstract details > *:not(summary) {
    margin-top: 10px;
}

/* Responsive design for mobile */
@media (max-width: 768px) {
    .publication-row {
        padding: 16px;
    }
    .publication-image img {
        max-height: 280px;
    }
}
</style>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://arxiv.org/abs/2605.07127">The Position Curse: LLMs Struggle to Locate the Last Few Items in a List</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>*, Xiong, H.-D.*, Wilson, R. C., Aoi, M., Mattar, M. G., & Ji-An, L.† <br/><em>*Co-first authors. †Senior author.</em></div>
        <div class="pub-venue"><b>preprint</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: LLMs can find a needle in a haystack but fail to retrieve the last few items in a short list — we name this the <em>Position Curse</em>, characterize it across open- and closed-source models, and show LoRA fine-tuning on PosBench helps but doesn't saturate.</summary>
                Modern large language models (LLMs) can find a needle in a haystack (locating a single relevant fact buried among hundreds of thousands of irrelevant tokens) with near-saturated accuracy, yet fail to retrieve the last few items in a short list. We call this failure the <em>Position Curse</em>. For instance, even in a two-line code snippet, Claude Opus 4.6 misidentifies the second-to-last line most of the time. To characterize this failure, we evaluated two complementary queries: given a position in a sequence (of letters or words), retrieve the corresponding item; and given an item, return its position. Each position is specified as a forward or backward offset from an anchor, either an endpoint of the list (its start or end) or another item in the list. Across both open-source and frontier closed-source models, backward retrieval substantially lags forward retrieval. To test whether this capability can be rescued by post-training, we constructed <b>PosBench</b>, a position-focused training dataset. LoRA fine-tuning improves both forward and backward retrieval and generalizes to a held-out code-understanding benchmark (<b>PyIndex</b>), yet absolute performance remains far from saturated. As LLM coding agents increasingly operate over large codebases where precise indexing becomes essential for code understanding and editing, position-based retrieval emerges as a key capability for future pretraining objectives and model design.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/pos_retrieval.png" alt="Position Curse" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://arxiv.org/abs/2603.18299">ALIGN: Adversarial Learning for Generalizable Speech Neuroprosthesis</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>*, Li, S.*, Sabatini, B. L., Aoi, M., & Mishne, G. <br/><em>*Co-first authors.</em></div>
        <div class="pub-venue"><b>preprint</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: ALIGN is an adversarial domain-alignment framework for intracortical speech BCIs that generalizes to unseen sessions, lowering phoneme and word error rates relative to baselines.</summary>
                Intracortical brain-computer interfaces (BCIs) can decode speech from neural activity with high accuracy when trained on data pooled across recording sessions. In realistic deployment, however, models must generalize to new sessions without labeled data, and performance often degrades due to cross-session nonstationarities (e.g., electrode shifts, neural turnover, and changes in user strategy). In this paper, we propose ALIGN, a session-invariant learning framework based on multi-domain adversarial neural networks for semi-supervised cross-session adaptation. ALIGN trains a feature encoder jointly with a phoneme classifier and a domain classifier operating on the latent representation. Through adversarial optimization, the encoder is encouraged to preserve task-relevant information while suppressing session-specific cues. We evaluate ALIGN on intracortical speech decoding and find that it generalizes consistently better to previously unseen sessions, improving both phoneme error rate and word error rate relative to baselines. These results indicate that adversarial domain alignment is an effective approach for mitigating session-level distribution shift and enabling robust longitudinal BCI decoding.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/align.png" alt="ALIGN BCI" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.science.org/doi/10.1126/sciadv.adq7342">Brain Feature Maps Reveal Progressive Animal-Feature Representations</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2025)</div>
        <div class="pub-venue"><b>Science Advances</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Heatmap recordings across V1/V2, V4, and PIT show monkey ventral-stream neurons preferentially encode local animal features over generic objects, with this trend strengthening up the visual hierarchy.</summary>
                What are the fundamental principles that inform representation in the primate visual brain? While objects have become an intuitive framework for studying neurons in many parts of cortex, it is possible that neurons follow a more expressive organizational principle, such as encoding generic features present across textures, places, and objects. In this study, we used multielectrode arrays to record from neurons in the early (V1/V2), middle (V4), and later [posterior inferotemporal (PIT) cortex] areas across the visual hierarchy, estimating each neuron's local operation across natural scene via "heatmaps." We found that, while populations of neurons with foveal receptive fields across V1/V2, V4, and PIT responded over the full scene, they focused on salient subregions within object outlines. Notably, neurons preferentially encoded animal features rather than general objects, with this trend strengthening along the visual hierarchy. These results show that the monkey ventral stream is partially organized to encode local animal features over objects, even as early as primary visual cortex.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/featuremap.png" alt="Brain Feature Maps" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.nature.com/articles/s41586-025-09544-4">Arousal as a universal embedding for spatiotemporal brain dynamics</a></div>
        <div class="pub-authors">Raut, R. V., ..., <b>Zhang, Z.</b>, et al. (2023)</div>
        <div class="pub-venue"><b>Nature</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: A single scalar measure of arousal (e.g., pupil diameter) suffices to reconstruct multimodal, brain-wide spatiotemporal physiology — reframing many "spontaneous" fluctuations as reflections of a unified arousal-related process.</summary>
                Neural activity in awake organisms shows widespread and spatiotemporally diverse correlations with behavioral and physiological measurements. We propose that this covariation reflects in part the dynamics of a unified, arousal-related process that regulates brain-wide physiology on the timescale of seconds. Taken together with theoretical foundations in dynamical systems, this interpretation leads us to a surprising prediction: that a single, scalar measurement of arousal (e.g., pupil diameter) should suffice to reconstruct the continuous evolution of multimodal, spatiotemporal measurements of large-scale brain physiology. To test this hypothesis, we perform multimodal, cortex-wide optical imaging and behavioral monitoring in awake mice. We demonstrate that spatiotemporal measurements of neuronal calcium, metabolism, and blood-oxygen can be accurately and parsimoniously modeled from a low-dimensional state-space reconstructed from the time history of pupil diameter. Extending this framework to behavioral and electrophysiological measurements from the Allen Brain Observatory, we demonstrate the ability to integrate diverse experimental data into a unified generative model via mappings from an intrinsic arousal manifold. Our results support the hypothesis that spontaneous, spatially structured fluctuations in brain-wide physiology—widely interpreted to reflect regionally-specific neural communication—are in large part reflections of an arousal-related process. This enriched view of arousal dynamics has broad implications for interpreting observations of brain, body, and behavior as measured across modalities, contexts, and scales.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/arousal.png" alt="Arousal Dynamics" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.medrxiv.org/content/10.1101/2024.11.14.24317348v2">Characterizing Behavioral Dynamics in Bipolar Disorder with Computational Ethology</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b> et al. (2024)</div>
        <div class="pub-venue"><b>preprint on medRxiv</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Computational ethology applied to free-moving open-field human behavior identifies fine-grained motifs that distinguish bipolar disorder from controls better than traditional ethological and psychiatric measures.</summary>
                New technologies for the quantification of behavior have revolutionized animal studies in social, cognitive, and pharmacological neurosciences. However, comparable studies in understanding human behavior, especially in psychiatry, are lacking. In this study, we utilized data-driven machine learning to analyze natural, spontaneous open-field human behaviors from people with euthymic bipolar disorder (BD) and non-BD participants. Our computational paradigm identified representations of distinct sets of actions (motifs) that capture the physical activities of both groups of participants. We propose novel measures for quantifying dynamics, variability, and stereotypy in BD behaviors. These fine-grained behavioral features reflect patterns of cognitive functions of BD and better predict BD compared with traditional ethological and psychiatric measures and action recognition approaches. This research represents a significant computational advancement in human ethology, enabling the quantification of complex behaviors in real-world conditions and opening new avenues for characterizing neuropsychiatric conditions from behavior.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/bd.png" alt="Behavioral Dynamics" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Unsupervised quantification and classification of free-moving human behavior in euthymic bipolar disorder</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b> et al. (2024)</div>
        <div class="pub-venue"><b>Accepted for Computational and Systems Neuroscience (COSYNE)</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Unsupervised pose-based modeling of free-moving humans identifies behavioral motifs that classify bipolar disorder vs. healthy controls, outperforming CV models, expert annotation, and clinical scales.</summary>
                Free-moving spontaneous behavior is the window to probe the brain and mind. Individuals with neuropsychiatric conditions such as bipolar disorder (BD) can exhibit distinctive patterns of behavior (McReynolds, 1962). Our objective was to quantify free-moving spontaneous human behavior in real-world contexts among euthymic BD individuals and differentiate them from a healthy control (HC) population based on these identified behavioral features. We analyzed videos of 25 BD patients and 25 HC participants freely moving in an unexplored room for 15 minutes (Young et al, 2007). Utilizing a key-point estimation toolbox (Mathis et al., 2018), we extracted human poses and represented them through a latent variable model (Luxem et al., 2022). Clustering the latent representations identified repeated behavioral motifs, revealing unique features of BD aligned with known clinical observations. Our approach outperformed CV models, expert human annotation, and even established clinical assessment scales in distinguishing BD from HC.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/bd_cosyne.png" alt="Unsupervised Behavior Analysis" />
    </div>
</div>

<!--
<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Semi-supervised quantification and interpretation of undirected human behavior</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b> et al. (2023)</div>
        <div class="pub-venue"><b>Accepted for Computational and Systems Neuroscience (COSYNE)</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: A semi-supervised model finds the motif "approach, inspect, move along" has significantly reduced dwell time in BD vs. controls (p = 0.04), while manually annotated categories show no significance.</summary>
                Undirected behavior reflects cognitive functions and provides insights for diagnosing psychiatric conditions such as bipolar disorder (BD) (McReynolds, 1962). Open-field animal behaviors have been well-studied for this purpose; however, a corresponding human subject paradigm is still lacking, and quantifying complex spontaneous human behaviors is challenging. Here, we demonstrate a semi-supervised model to quantify undirected human behavior, differentiate subtle hallmark behavioral features of BD, and create a natural language generative model to provide nuanced interpretations of behaviors with context information. We found the dwell time of motif "approach, inspect, move along" is significantly lower in the BD population compared with controls (two sample t-test, p-value: 0.04), while no significance was found from manually annotated categories.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Semi-supervised Behavior" />
    </div>
</div>
-->

<!--
<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://brain.ieee.org/event/ieee-brain-discovery-and-neurotechnology-workshop/">Unsupervised quantification of undirected human behavior for bipolar disorder analysis</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b> et al. (2022)</div>
        <div class="pub-venue"><b>Accepted as a spotlight poster for IEEE Brain Discovery Neurotechnology Workshop – Brain Mind Body Cognitive Engineering for Health and Wellness and Society for Neuroscience (SfN)</b></div>
        <div class="pub-abstract">Research on unsupervised quantification of undirected human behavior for bipolar disorder analysis.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Unsupervised Quantification" />
    </div>
</div>
-->

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.sfn.org/meetings/neuroscience-2021">Animal-feature Encoding in Macaque Brain and in Artificial Networks</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2022)</div>
        <div class="pub-venue"><b>Accepted as a poster for Society for Neuroscience (SfN)</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Animal-mask AUC values rise from V1 (0.19) to V4 (0.63) to IT (0.73), supporting animal-feature encoding as an organizing principle of the macaque ventral stream.</summary>
                Macaque monkeys are foraging and social animals that spend a significant fraction of their time identifying conspecifics, classifying their actions, and avoiding threats from other animals. This suggests that in learning information from the visual world, many neurons of the monkey ventral stream might focus on encoding animal-based features. We discovered that animal masks identified regions with strong neuronal activity for IT better than they did for V4 and for V4 better than for V1 (AUC values, median ± SE; V1: 0.19 ± 0.01, V4: 0.63 ± 0.06, IT: 0.73 ± 0.08). Collectively, our results provide further evidence of an organizing principle of the monkey ventral stream — to encode information diagnostic of animals.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/heatmao_sfn.png" alt="Animal-feature Encoding" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Do you see what I see? Representations in brains and neural networks. Brain-Score and Beyond: Confronting Brain-like ANNs with Neuroscientific Data</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Ponce, C. R. (2022)</div>
        <div class="pub-venue"><b>Accepted as a workshop presentation for Computational and Systems Neuroscience (COSYNE) 2022</b></div>
        <div class="pub-abstract">Workshop presentation on representations in brains and neural networks.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/heatmap_cosyne.png" alt="Brain Representations" />
    </div>
</div>

<!--
<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://abstracts.g-node.org/conference/BC21/abstracts#/uuid/bbb01455-e0b9-4521-bbe1-9c7c0ba4389c">The Macaque Ventral Stream Shows A Hierarchical Structure for Animal-feature Encoding (2021)</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R.</div>
        <div class="pub-venue"><b>Accepted as abstract for Society for Neuroscience (SfN) and Bernstein Conference</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Comparing neuronal responses across V1, V4, and IT to identify brain-wide organizing principles and test whether learning-based CNNs share them.</summary>
                Are there organizing principles for information encoding along the primate ventral stream? Neurons in each visual area are often tested with different types of stimuli, ranging from simple (e.g., lines in V1) to complex (faces in inferotemporal cortex, IT); however, this strategy limits functional comparisons across areas. By comparing neuronal responses to a given stimulus set across areas, we set out to identify brain-wide organizing principles and determine if these principles are shared by learning-based models of the ventral stream (convolutional neural networks, CNNs).
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Macaque Ventral Stream" />
    </div>
</div>
-->

<!--
<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://openscholarship.wustl.edu/eng_etds/574/">Translating Convolutional Neural Networks Approach to the Ventral Pathway (2021)</a></div>
        <div class="pub-authors"><b>Zhang, Z.</b><br/>Committee Members: Dr. Chien-Ju Ho, Dr. Ulugbek Kamilov, and Dr. Carlos Ponce</div>
        <div class="pub-venue"><b>Washington University in St. Louis, McKelvey School of Engineering, Department of Computer Science Master Thesis Dissertation</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Using CNN heatmap attribution to build biological feature maps; animal regions elicit increasingly larger responses along the monkey ventral stream — a signature not captured by artificial networks.</summary>
                Do artificial neurons in CNNs learn to represent the same visual information as the biological neurons in primate brains? Previous studies have shown that the visual recognition pathway (ventral stream) in humans and monkeys increasingly represents animate objects. We used a heatmap attribution technique borrowed from convolutional neural networks to generate biological feature maps identifying regions in scenes that elicit responses from neurons along the ventral stream (V1/V2, V4, and IT). We found that image regions containing animals elicited increasingly larger responses along the ventral stream, while such animacy features are not represented in artificial neural networks.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="CNN Ventral Pathway" />
    </div>
</div>
-->

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Shape Recognition in Ultrasound with Deep Learning (2020)</div>
        <div class="pub-authors"><b>Zhang, Z.</b></div>
        <div class="pub-venue"><b>Washington University in St. Louis, McKelvey School of Engineering, Department of Electrical and Systems Engineering Capstone Design Thesis</b></div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Pre-trained neural network recognizes geometric shapes in ultrasound images of 3D-printed samples with 96% accuracy; released a database for future ultrasound imaging research.</summary>
                Ultrasound is one of the most common imaging techniques in clinical settings, but its functionalities are limited by its low resolution and high dependency on the operator skills. Here, we applied a pre-trained neural network to recognize geometric shapes in ultrasound images of 3D-printed samples. We achieved 96% task accuracy and created a database available for future research in ultrasound imaging.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/sonification.png" alt="Ultrasound Shape Recognition" />
    </div>
</div>

## Industry Research

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.meta.com/ai-glasses/meta-ray-ban-display/?srsltid=AfmBOoqJgguuzbd2lgoz1FicSW5Bnj5K1sXeNkIHcpDYIU3ILs_aoC2d">Meta Neural Band real-time and multi-modality model</a></div>
        <div class="pub-authors">Work done during research scientist internship at Meta (2025)</div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Built models that improved the robustness of a handwriting recognition system productionized in the Meta Neural Band; live demoed at Meta Connect 2025 and named one of <em>TIME</em>'s Best Inventions of 2025.</summary>
                Developed models to improve the robustness of a handwriting recognition system productionized in the <a href="https://www.meta.com/ai-glasses/meta-ray-ban-display/?srsltid=AfmBOoqJgguuzbd2lgoz1FicSW5Bnj5K1sXeNkIHcpDYIU3ILs_aoC2d">Meta Neural Band</a>, which captures electrical activity from subtle forearm muscle movements for intuitive, gesture-based input. This work was <a href="https://www.youtube.com/live/D97ILdUbYww?si=krptKIikEhFvF9O9&t=2975">live demoed at Meta Connect 2025</a> and later recognized as one of <a href="https://time.com/collections/best-inventions-2025/7318319/meta-ray-ban-display/"><em>TIME</em>'s Best Inventions of 2025</a>.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/meta.png" alt="Meta Neural Band Handwriting" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://research.facebook.com/">EMG–Vision Multimodal Foundation Models for Neural Wristbands</a></div>
        <div class="pub-authors">Work done during research scientist internship at Meta (2024)</div>
        <div class="pub-abstract">
            <details>
                <summary>TL;DR: Developed EMG–vision multimodal foundation models for Meta's neural wristbands, improving performance across multiple downstream tasks including pose estimation.</summary>
                Developed EMG–vision multimodal foundation models for neural wristbands at <a href="https://research.facebook.com/">Meta</a>, improving performance across multiple downstream tasks such as pose estimation. The work explored joint representation learning between surface electromyography signals and synchronized vision streams to support generalization across users and tasks.
            </details>
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/neural_band.avif" alt="EMG-Vision Multimodal Model" />
    </div>
</div>

## Undergraduate Projects

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Embedded Systems: Closed-Loop Incubator with Remote Monitoring</div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Liao, X. (2019)</div>
        <div class="pub-venue"><b>Embedded Systems & IoT Project</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> Arduino, Photon, Adafruit SI7021, Embedded Systems<br/>
            <strong>Features:</strong>
            <ul>
                <li>Plastic bottles: recycle and reuse</li>
                <li>Hardware: wires, resistors, fan, Adafruit SI7021, Photon, Arduino</li>
                <li>Embedded system: Sensors and Actuators + Feedback Control</li>
                <li>UI: graphical sliders and other information of the incubator</li>
                <li>Networking infrastructure: monitor and control the incubator remotely</li>
            </ul>
[\[CODE\]](https://github.com/ZhanqiZhang66/Incubator)  
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-microchip" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Embedded Systems: Networked Garage Controller with Web UI</div>
        <div class="pub-authors"><b>Zhang, Z.</b>, Liao, X. (2019)</div>
        <div class="pub-venue"><b>C++, JavaScript, HTML, Embedded Systems</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> C++, JavaScript, HTML, Photon, Arduino<br/>
            <strong>Features:</strong>
            <ul>
                <li>Hardware: wires, resistors, buttons, LEDs, Two Photons</li>
                <li>Embedded system: Sensors and Actuators + Remote Control</li>
                <li>UI: responsive website and app</li>
                <li>Networking infrastructure: monitor and control the garage light and door remotely</li>
                <li>Functionality: Close the door and turn off the light automatically with the time set</li>
            </ul>
[\[CODE\]](https://github.com/ZhanqiZhang66/GarageController)  
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-warehouse" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Computer Vision Projects in Python</div>
        <div class="pub-authors"><b>Zhang, Z.</b> (2019)</div>
        <div class="pub-venue"><b>Computer Vision & Machine Learning</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> Python, OpenCV, TensorFlow, PyTorch<br/>
            <strong>Projects Include:</strong>
            <ul>
                <li>Edge detection + Line detection</li>
                <li>Image Restoration & Optimization</li>
                <li>Photometric Stereo</li>
                <li>Camera Projection and Transformations</li>
                <li>Estimation, Sampling, Robust Fitting</li>
                <li>Epipolar Geometry, Binocular Stereo</li>
                <li>Optical flow</li>
                <li>Neural Networks</li>
                <li>Semantic Vision Tasks</li>
                <li>GAN and VAEs. Unsupervised Learning</li>
            </ul>
            <em>This work currently can't be viewed publicly due to the course policy</em>
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-eye" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Object-Oriented Web App: Task Manager in React</div>
        <div class="pub-authors"><b>Zhang, Z.</b> (2019)</div>
        <div class="pub-venue"><b>React.js, Web Development</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> React.js, JavaScript, HTML, CSS<br/>
            Interactive web application for task management with modern React.js framework.
            <!-- [\[CODE\]](https://wustlcse204.github.io/09-todo-react-ZhanqiZhang66/) -->
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-list-alt" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Control Systems: 3R Manipulator Kinematics and Dynamics in MATLAB/Simulink</div>
        <div class="pub-authors"><b>Zhang, Z.</b> (2018)</div>
        <div class="pub-venue"><b>Matlab, Simulink, Robotics</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> MATLAB, Simulink, Robotics Control Systems<br/>
            Development of 3D rotational robotics control systems using MATLAB and Simulink for kinematic and dynamic analysis.
[\[CODE\]](https://github.com/ZhanqiZhang66/3R-Robotics)  
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-robot" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Object-Oriented AI: Game-Playing Engine for Tic-Tac-Toe and Gomoku in C++</div>
        <div class="pub-authors"><b>Zhang, Z.</b> (2018)</div>
        <div class="pub-venue"><b>C++, Artificial Intelligence</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> C++, AI Algorithms, Game Theory<br/>
            Implementation of artificial intelligence algorithms for classic board games including tic-tac-toe and Gomoku with intelligent move prediction and strategy optimization.
[\[CODE\]](https://github.com/ZhanqiZhang66/AI-Gomuku)
        </div>
    </div>
    <div class="publication-image">
        <i class="fas fa-gamepad" style="font-size: 6em; color: #7f8c8d;"></i>
    </div>
</div>
