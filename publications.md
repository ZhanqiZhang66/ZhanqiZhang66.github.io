---
layout: page
title: "Selected Projects"
subtitle: 
css: "/assets/css/index.css"
share-img: /assets/img/victoria.jpg
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

**Characterizing Behavioral Dynamics in Bipolar Disorder with Computational Ethology**
**Zhang, Z.**, Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2024).  
*preprint on [medRxiv ](https://www.medrxiv.org/content/10.1101/2024.11.14.24317348v1)*

New technologies for the quantification of behavior have revolutionized animal studies in social, cognitive, and pharmacological neurosciences. However, comparable studies in understanding human behavior, especially in psychiatry, are lacking. In this study, we utilized data-driven machine learning to analyze natural, spontaneous open-field human behaviors from people with euthymic bipolar disorder (BD) and non-BD participants. Our computational paradigm identified representations of distinct sets of actions (motifs) that capture the physical activities of both groups of participants. We propose novel measures for quantifying dynamics, variability, and stereotypy in BD behaviors. These fine-grained behavioral features reflect patterns of cognitive functions of BD and better predict BD compared with traditional ethological and psychiatric measures and action recognition approaches. This research represents a significant computational advancement in human ethology, enabling the quantification of complex behaviors in real-world conditions and opening new avenues for characterizing neuropsychiatric conditions from behavior.

**Arousal as a universal embedding for spatiotemporal brain dynamics**

Raut, R. V, Rosenthal Z. P, Wang X. ,Miao  H. , **Zhang, Z**, Lee Jin-Moo, Raichle, M. E , Bauer, A. Q , Brunton, S. L , Brunton, B. W, Kutz, J N. (2023)

*Preprint on [bioRxiv ](https://pmc.ncbi.nlm.nih.gov/articles/PMC10769245/)*

Neural activity in awake organisms shows widespread and spatiotemporally diverse correlations with behavioral and physiological measurements. We propose that this covariation reflects in part the dynamics of a unified, arousal-related process that regulates brain-wide physiology on the timescale of seconds. Taken together with theoretical foundations in dynamical systems, this interpretation leads us to a surprising prediction: that a single, scalar measurement of arousal (e.g., pupil diameter) should suffice to reconstruct the continuous evolution of multimodal, spatiotemporal measurements of large-scale brain physiology. To test this hypothesis, we perform multimodal, cortex-wide optical imaging and behavioral monitoring in awake mice. We demonstrate that spatiotemporal measurements of neuronal calcium, metabolism, and blood-oxygen can be accurately and parsimoniously modeled from a low-dimensional state-space reconstructed from the time history of pupil diameter. Extending this framework to behavioral and electrophysiological measurements from the Allen Brain Observatory, we demonstrate the ability to integrate diverse experimental data into a unified generative model via mappings from an intrinsic arousal manifold. Our results support the hypothesis that spontaneous, spatially structured fluctuations in brain-wide physiology—widely interpreted to reflect regionally-specific neural communication—are in large part reflections of an arousal-related process. This enriched view of arousal dynamics has broad implications for interpreting observations of brain, body, and behavior as measured across modalities, contexts, and scales.

**Unsupervised quantification and classification of free-moving human behavior in euthymic bipolar disorder.**

**Zhang, Z.**, Yang, Y., Sheehan, T., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2024).  
_Accepted for [Computational and Systems Neuroscience (COSYNE)](https://www.cosyne.org/)_

Free-moving spontaneous behavior is the window to probe the brain and mind. Individuals with
neuropsychiatric conditions such as bipolar disorder (BD) can exhibit distinctive patterns of behavior
(McReynolds, 1962). Our objective was to quantify free-moving spontaneous human behavior in real-world
contexts among euthymic BD individuals and differentiate them from a healthy control (HC) population based
on these identified behavioral features.

We analyzed videos of 25 BD patients and 25 HC participants freely moving in an unexplored room for
15 minutes (Young et al, 2007). Utilizing a key-point estimation toolbox (Mathis et al., 2018), we extracted
human poses and represented them through a latent variable model (Luxem et al., 2022). Clustering the latent
representations identified repeated behavioral motifs, revealing unique features of BD aligned with known
clinical observations. For comparison, we employed action detection from computer vision (CV) models (e.g.,
MMAction and S3D) and from expert human annotation to extract motifs.

Notably, our unsupervised framework revealed differences between BD and HC populations. We
detected differences in dwell time for identified motifs (two sample t-test, p-value: 0.04), in contrast to
manually labeled or CV identified actions. We found a smaller behavioral repertoire in BD, as measured by
transition probabilities, but with higher latent volume, indicating a higher-variance yet more stereotyped
behavior in BD. Our approach outperformed CV models, expert human annotation, and even established
clinical assessment scales (Hamilton Depression Scale and Young Mania Rating Scale) in distinguishing BD from
HC (accuracy mean std; ours: 0.72 0.11, CV actions: 0.62 0.13: assessment scales: 0.60 0.13, human
annotation: 0.50 0.14).

Our results underscore the potential of data-driven identified behavioral motifs to effectively
differentiate BD from HC. This insight promises the development of novel diagnostics and treatment
approaches for understanding neuropsychiatric conditions from behavior.

**Semi-supervised quantification and interpretation of undirected human behavior.**  
**Zhang, Z.**, Yang, Y., Sheehan, T., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2023).  
_Accepted for [Computational and Systems Neuroscience (COSYNE)](https://www.cosyne.org/)_

Undirected behavior reflects cognitive functions and provides insights for diagnosing psychiatric conditions such as bipolar disorder (BD) (McReynolds, 1962). Open-field animal behaviors have been well-studied for this purpose; however, a corresponding human subject paradigm is still lacking, and quantifying complex spontaneous human behaviors is challenging. Here, we demonstrate a semi-supervised model to quantify undirected human behavior, differentiate subtle hallmark behavioral features of BD, and create a natural language generative model to provide nuanced interpretations of behaviors with context information. We collected videos of BD (n=12) and control (n=12) human participants freely interacting in an unexplored room with each video manually annotated into 6 categories (e.g., walk). We used DeepLabCut (Mathis et al, 2018) to track the spatiotemporal postures of the participants coupled with the VAME latent variable model (Luxem et al, 2021) to encode pose sequences into latent representations. We then clustered the latent representations into 10 behavioral motifs. To interpret these motifs, we independently described example clips using natural language. Using these descriptions, we created a novel transformer-based model that generated interpretable descriptions for each cluster. We found the dwell time of motif “approach, inspect, move along” is significantly lower in the BD population compared with controls (two sample t-test, p-value: 0.04), while no significance was found from manually annotated categories. We then used transition matrices to characterize how participants transitioned between motifs. We found BD to have sparser transition matrices in the second half of the video which reflected more stereotyped behavior and a smaller behavioral repertoire. We quantified this using the entropy of the transition matrix and found BD patients to have significantly different entropy between the first and the second half of the video (F test for equal variances, p-value: 0.01). Our analysis identifies fine-resolution behavioral motifs that can distinguish BD using undirected human behavior.

**Unsupervised quantification of undirected human behavior for bipolar disorder analysis.**  
**Zhang, Z.**, Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2022).  
_Accepted as a spotlight poster for [IEEE Brain Discovery Neurotechnology Workshop – Brain Mind Body Cognitive Engineering for Health and Wellness](https://brain.ieee.org/event/ieee-brain-discovery-and-neurotechnology-workshop/) and [Society for Neuroscience (SfN)](https://www.sfn.org/meetings/neuroscience-2021)_

**Animal-feature Encoding in Macaque Brain and in Artificial Networks.**  
**Zhang, Z.**, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2022).  
_Accepted as a poster for [Society for Neuroscience (SfN)](https://www.sfn.org/meetings/neuroscience-2021)_

Macaque monkeys are foraging and social animals that spend a significant fraction of their time identifying conspecifics, classifying their actions, and avoiding threats from other animals (Post and Baulu, 1978; Cheney and Seyfarth, 1990; Son, 2004). This suggests that in learning information from the visual world, many neurons of the monkey ventral stream might focus on encoding animal-based features. To test this, we designed experiments to show how neurons respond over entire natural scenes containing animals and other types of objects. Inspired by feature-mapping operations in artificial neural networks (ANNs), we developed heatmaps describing the spiking activity of V1, V4, and IT neurons over full natural scenes (Arcaro et al., 2020). Heatmaps can be compared across cortical areas and also to feature channels in ANNs. We selected dozens of scenes, and each was segmented using independently obtained annotations from neural networks (Chen et al, 2017) and human participants. These segmentations served as masks quantifying the concentration of neuronal and ANN activity within labeled regions. Consistent with the observed behavior of macaques in the wild, we discovered that animal masks identified regions with strong neuronal activity for IT better than they did for V4 and for V4 better than for V1 (AUC values, median ± SE;  V1: 0.19 ± 0.01, V4: 0.63 ± 0.06, IT: 0.73 ± 0.08). No such linear trend was found for non-animal masks (e.g., food, books). To determine if this trend could emerge from any system with a hierarchical architecture, we replicated these analyses using ANNs. Most ANNs did not show this animal-focused trend. We studied the few ANNs that did express this pattern, such as CORNet-S (Kubilius et al, 2019), and measured their ability to overcome nuisance changes (distortion robustness), e.g., bias for shapes vs. textures, using previous tools (Geirhos et al, 2021). We found these ANNs could converge to the same result as the brain by showing a bias towards animal-related textures, even if they lacked object-centric representations. Finally, we also compared neuronal heatmaps with those derived from monkeys’ free-viewing data, against three saliency maps (GBVS, Itti-Koch, and FASA). We found saliency maps and free-viewing maps correlated best with IT heatmaps (Pearson correlation; eye-viewing: 0.13, Itto-Koch: 0.31, GBVS: 0.38, FASA: 0.16). Collectively, our results provide further evidence of an organizing principle of the monkey ventral stream  — to encode information diagnostic of animals.

**Do you see what I see? Representations in brains and neural networks. Brain-Score and Beyond: Confronting Brain-like ANNs with Neuroscientific Data.**  
**Zhang, Z.**, Ponce, C. R. (2022).  
_Accepted as a workshop presentation for [Computational and Systems Neuroscience (COSYNE) 2022](https://www.cosyne.org/)_

**The Macaque Ventral Stream Shows A Hierarchical Structure for Animal-feature Encoding (2021)**  
**Zhang, Z.**, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R.  
_Accepted as abstract for [Society for Neuroscience (SfN)](https://www.sfn.org/meetings/neuroscience-2021) and [Bernstein Conference](https://abstracts.g-node.org/conference/BC21/abstracts#/uuid/bbb01455-e0b9-4521-bbe1-9c7c0ba4389c)_  

Are there organizing principles for information encoding along the primate ventral stream? Neurons in each visual area are often tested with different types of stimuli, ranging from simple (e.g., lines in V1) to complex (faces in inferotemporal cortex, IT); however, this strategy limits functional comparisons across areas. By comparing neuronal responses to a given stimulus set across areas, we set out to identify brain-wide organizing principles and determine if these principles are shared by learning-based models of the ventral stream (convolutional neural networks, CNNs)

**Translating Convolutional Neural Networks Approach to the Ventral Pathway (2021) [\[PDF\]](https://openscholarship.wustl.edu/eng_etds/574/)**  
**Zhang, Z.**  
Committee Members: Dr. Chien-Ju Ho, Dr. Ulugbek Kamilov, and Dr. Carlos Ponce  
_Washington University in St. Louis, McKelvey School of Engineering, Department of Computer Science Master Thesis Dissertation_  

Do artificial neurons in CNNs learn to represent the same visual information as the biological neurons in primate brains? Previous studies have shown that the visual recognition pathway (ventral stream) in humans and monkeys increasingly represents animate objects. We used a heatmap attribution technique borrowed from convolutional neural networks to generate biological feature maps identifying regions in scenes that elicit responses from neurons along the ventral stream (V1/V2, V4, and IT). Biological feature maps were then compared to activation maps produced by units in convolutional neural networks. We found that image regions containing animals elicited increasingly larger responses along the ventral stream, while such animacy features are not represented in artificial neural networks.  


**Shape Recognition in Ultrasound with Deep Learning (2020)**  
**Zhang, Z.**, Miao, H., & Liao, X.  
_Washington University in St. Louis, McKelvey School of Engineering, Department of Electrical and Systems Engineering Capstone Design Thesis_  

Ultrasound is one of the most common imaging techniques in clinical settings, but its functionalities are limited by its low resolution and high dependency on the operator skills. Here, we applied a pre-trained neural network to recognize geometric shapes in ultrasound images of 3D-printed samples. We achieved 96% task accuracy and created a database available for future research in ultrasound imaging.

Undergrad Projects
------------------

### 2019

**Internet of Things: incubator**  
Victoria Zhang, Xingjue Liao  

*   Plastic bottles: recycle and reuse
*   Hardware: wires, resistors, fan, Adafruit SI7021, Photon, Arduino...
*   Embedded system: Sensors and Actuators + Feedback Control
*   UI: graphical sliders and other information of the incubator.
*   Networking infrastructure: monitor and control the incubator remotely

[\[CODE\]](https://github.com/ZhanqiZhang66/Incubator)  

**Internet of Things: Mini Garage Controller in C++, JavaScript and HTML**  
Victoria Zhang, Xingjue Liao  

*   Hardware: wires, resistors, buttons, LEDS, Two Photons
*   Embedded system: Sensors and Actuators + Remote Control
*   UI: responsive website and app
*   Networking infrastructure: monitor and control the garage light and door remotely
*   Functionality: Close the door and turn of the light automatically with the time setted

[\[CODE\]](https://github.com/ZhanqiZhang66/GarageController)  

**Computer Vision Projects in Python**  
**Victoria Zhang**  

*   Edge detection + Line detection
*   Image Restoration & Optimization
*   Photometric Stereo
*   Camera Projection and Transformations
*   Estimation, Sampling, Robust Fitting
*   Epipolar Geometry, Binocular Stereo
*   Optical flow
*   Neural Networks
*   Semantic Vision Tasks
*   GAN and VAEs. Unsupervised Learning.
This work currently can't be viewed publicly due to the course policy  


**Web development: To-do List**  
**Victoria Zhang**  
<!-- [\[CODE\]](https://wustlcse204.github.io/09-todo-react-ZhanqiZhang66/)   -->

### 2018

**3D Rotational Robotics in Simulink and Matlab**  
**Victoria Zhang** 
[\[CODE\]](https://github.com/ZhanqiZhang66/3R-Robotics)  

**AI tic-tac-toe and Gomoku Game in C++**  
**Victoria Zhang**  
[\[CODE\]](https://github.com/ZhanqiZhang66/AI-Gomuku)
