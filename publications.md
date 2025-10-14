---
layout: page
title: "Selected Projects"
subtitle: 
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

<style>
.publication-row {
    display: flex;
    align-items: flex-start;
    margin-bottom: 30px;
    padding: 20px;
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
    flex: 2.5;
    padding-right: 25px;
}
.publication-image {
    flex: 1;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 200px;
}
.publication-image img {
    max-width: 100%;
    max-height: 250px;
    width: auto;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    object-fit: contain;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.publication-image img:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
}
.pub-title {
    font-size: 1.15em;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
    line-height: 1.3;
}
.pub-authors {
    font-size: 0.95em;
    color: #34495e;
    margin-bottom: 8px;
    font-weight: 500;
}
.pub-venue {
    font-style: italic;
    color: #7f8c8d;
    margin-bottom: 12px;
    font-size: 0.9em;
}
.pub-abstract {
    font-size: 0.9em;
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

/* Responsive design for mobile */
@media (max-width: 768px) {
    .publication-row {
        flex-direction: column;
        padding: 15px;
    }
    .publication-content {
        padding-right: 0;
        margin-bottom: 15px;
    }
    .publication-image {
        min-height: auto;
        max-width: 200px;
        margin: 0 auto;
    }
    .publication-image img {
        max-height: 200px;
    }
}
</style>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.science.org/doi/10.1126/sciadv.adq7342">Brain Feature Maps Reveal Progressive Animal-Feature Representations</a></div>
        <div class="pub-authors">Zhang, Z., Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2025)</div>
        <div class="pub-venue"><b>Science Advances</b></div>
        <div class="pub-abstract">What are the fundamental principles that inform representation in the primate visual brain? While objects have become an intuitive framework for studying neurons in many parts of cortex, it is possible that neurons follow a more expressive organizational principle, such as encoding generic features present across textures, places, and objects. In this study, we used multielectrode arrays to record from neurons in the early (V1/V2), middle (V4), and later [posterior inferotemporal (PIT) cortex] areas across the visual hierarchy, estimating each neuron's local operation across natural scene via "heatmaps." We found that, while populations of neurons with foveal receptive fields across V1/V2, V4, and PIT responded over the full scene, they focused on salient subregions within object outlines. Notably, neurons preferentially encoded animal features rather than general objects, with this trend strengthening along the visual hierarchy. These results show that the monkey ventral stream is partially organized to encode local animal features over objects, even as early as primary visual cortex.</div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/featuremap.png" alt="Brain Feature Maps" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.nature.com/articles/s41586-025-09544-4">Arousal as a universal embedding for spatiotemporal brain dynamics</a></div>
        <div class="pub-authors">Raut, R. V, Rosenthal Z. P, Wang X. ,Miao H. , Zhang, Z, Lee Jin-Moo, Raichle, M. E , Bauer, A. Q , Brunton, S. L , Brunton, B. W, Kutz, J N. (2023)</div>
        <div class="pub-venue"><b>Nature</b></div>
        <div class="pub-abstract">Neural activity in awake organisms shows widespread and spatiotemporally diverse correlations with behavioral and physiological measurements. We propose that this covariation reflects in part the dynamics of a unified, arousal-related process that regulates brain-wide physiology on the timescale of seconds. Taken together with theoretical foundations in dynamical systems, this interpretation leads us to a surprising prediction: that a single, scalar measurement of arousal (e.g., pupil diameter) should suffice to reconstruct the continuous evolution of multimodal, spatiotemporal measurements of large-scale brain physiology. To test this hypothesis, we perform multimodal, cortex-wide optical imaging and behavioral monitoring in awake mice. We demonstrate that spatiotemporal measurements of neuronal calcium, metabolism, and blood-oxygen can be accurately and parsimoniously modeled from a low-dimensional state-space reconstructed from the time history of pupil diameter. Extending this framework to behavioral and electrophysiological measurements from the Allen Brain Observatory, we demonstrate the ability to integrate diverse experimental data into a unified generative model via mappings from an intrinsic arousal manifold. Our results support the hypothesis that spontaneous, spatially structured fluctuations in brain-wide physiology—widely interpreted to reflect regionally-specific neural communication—are in large part reflections of an arousal-related process. This enriched view of arousal dynamics has broad implications for interpreting observations of brain, body, and behavior as measured across modalities, contexts, and scales.</div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/arousal.png" alt="Arousal Dynamics" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.medrxiv.org/content/10.1101/2024.11.14.24317348v2">Characterizing Behavioral Dynamics in Bipolar Disorder with Computational Ethology</a></div>
        <div class="pub-authors">Zhang, Z., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2024)</div>
        <div class="pub-venue"><b>preprint on medRxiv</b></div>
        <div class="pub-abstract">New technologies for the quantification of behavior have revolutionized animal studies in social, cognitive, and pharmacological neurosciences. However, comparable studies in understanding human behavior, especially in psychiatry, are lacking. In this study, we utilized data-driven machine learning to analyze natural, spontaneous open-field human behaviors from people with euthymic bipolar disorder (BD) and non-BD participants. Our computational paradigm identified representations of distinct sets of actions (motifs) that capture the physical activities of both groups of participants. We propose novel measures for quantifying dynamics, variability, and stereotypy in BD behaviors. These fine-grained behavioral features reflect patterns of cognitive functions of BD and better predict BD compared with traditional ethological and psychiatric measures and action recognition approaches. This research represents a significant computational advancement in human ethology, enabling the quantification of complex behaviors in real-world conditions and opening new avenues for characterizing neuropsychiatric conditions from behavior.</div>
    </div>
    <div class="publication-image">
        <!-- Add your publication image here -->
        <img src="/assets/img/paper_fig/bd.png" alt="Behavioral Dynamics" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Unsupervised quantification and classification of free-moving human behavior in euthymic bipolar disorder</a></div>
        <div class="pub-authors">Zhang, Z., Yang, Y., Sheehan, T., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2024)</div>
        <div class="pub-venue"><b>Accepted for Computational and Systems Neuroscience (COSYNE)</b></div>
        <div class="pub-abstract">Free-moving spontaneous behavior is the window to probe the brain and mind. Individuals with neuropsychiatric conditions such as bipolar disorder (BD) can exhibit distinctive patterns of behavior (McReynolds, 1962). Our objective was to quantify free-moving spontaneous human behavior in real-world contexts among euthymic BD individuals and differentiate them from a healthy control (HC) population based on these identified behavioral features. We analyzed videos of 25 BD patients and 25 HC participants freely moving in an unexplored room for 15 minutes (Young et al, 2007). Utilizing a key-point estimation toolbox (Mathis et al., 2018), we extracted human poses and represented them through a latent variable model (Luxem et al., 2022). Clustering the latent representations identified repeated behavioral motifs, revealing unique features of BD aligned with known clinical observations. Our approach outperformed CV models, expert human annotation, and even established clinical assessment scales in distinguishing BD from HC.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Unsupervised Behavior Analysis" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Semi-supervised quantification and interpretation of undirected human behavior</a></div>
        <div class="pub-authors">Zhang, Z., Yang, Y., Sheehan, T., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2023)</div>
        <div class="pub-venue"><b>Accepted for Computational and Systems Neuroscience (COSYNE)</b></div>
        <div class="pub-abstract">Undirected behavior reflects cognitive functions and provides insights for diagnosing psychiatric conditions such as bipolar disorder (BD) (McReynolds, 1962). Open-field animal behaviors have been well-studied for this purpose; however, a corresponding human subject paradigm is still lacking, and quantifying complex spontaneous human behaviors is challenging. Here, we demonstrate a semi-supervised model to quantify undirected human behavior, differentiate subtle hallmark behavioral features of BD, and create a natural language generative model to provide nuanced interpretations of behaviors with context information. We found the dwell time of motif "approach, inspect, move along" is significantly lower in the BD population compared with controls (two sample t-test, p-value: 0.04), while no significance was found from manually annotated categories.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Semi-supervised Behavior" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://brain.ieee.org/event/ieee-brain-discovery-and-neurotechnology-workshop/">Unsupervised quantification of undirected human behavior for bipolar disorder analysis</a></div>
        <div class="pub-authors">Zhang, Z., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2022)</div>
        <div class="pub-venue"><b>Accepted as a spotlight poster for IEEE Brain Discovery Neurotechnology Workshop – Brain Mind Body Cognitive Engineering for Health and Wellness and Society for Neuroscience (SfN)</b></div>
        <div class="pub-abstract">Research on unsupervised quantification of undirected human behavior for bipolar disorder analysis.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Unsupervised Quantification" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.sfn.org/meetings/neuroscience-2021">Animal-feature Encoding in Macaque Brain and in Artificial Networks</a></div>
        <div class="pub-authors">Zhang, Z., Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2022)</div>
        <div class="pub-venue"><b>Accepted as a poster for Society for Neuroscience (SfN)</b></div>
        <div class="pub-abstract">Macaque monkeys are foraging and social animals that spend a significant fraction of their time identifying conspecifics, classifying their actions, and avoiding threats from other animals. This suggests that in learning information from the visual world, many neurons of the monkey ventral stream might focus on encoding animal-based features. We discovered that animal masks identified regions with strong neuronal activity for IT better than they did for V4 and for V4 better than for V1 (AUC values, median ± SE; V1: 0.19 ± 0.01, V4: 0.63 ± 0.06, IT: 0.73 ± 0.08). Collectively, our results provide further evidence of an organizing principle of the monkey ventral stream — to encode information diagnostic of animals.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Animal-feature Encoding" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://www.cosyne.org/">Do you see what I see? Representations in brains and neural networks. Brain-Score and Beyond: Confronting Brain-like ANNs with Neuroscientific Data</a></div>
        <div class="pub-authors">Zhang, Z., Ponce, C. R. (2022)</div>
        <div class="pub-venue"><b>Accepted as a workshop presentation for Computational and Systems Neuroscience (COSYNE) 2022</b></div>
        <div class="pub-abstract">Workshop presentation on representations in brains and neural networks.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Brain Representations" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://abstracts.g-node.org/conference/BC21/abstracts#/uuid/bbb01455-e0b9-4521-bbe1-9c7c0ba4389c">The Macaque Ventral Stream Shows A Hierarchical Structure for Animal-feature Encoding (2021)</a></div>
        <div class="pub-authors">Zhang, Z., Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R.</div>
        <div class="pub-venue"><b>Accepted as abstract for Society for Neuroscience (SfN) and Bernstein Conference</b></div>
        <div class="pub-abstract">Are there organizing principles for information encoding along the primate ventral stream? Neurons in each visual area are often tested with different types of stimuli, ranging from simple (e.g., lines in V1) to complex (faces in inferotemporal cortex, IT); however, this strategy limits functional comparisons across areas. By comparing neuronal responses to a given stimulus set across areas, we set out to identify brain-wide organizing principles and determine if these principles are shared by learning-based models of the ventral stream (convolutional neural networks, CNNs).</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Macaque Ventral Stream" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title"><a href="https://openscholarship.wustl.edu/eng_etds/574/">Translating Convolutional Neural Networks Approach to the Ventral Pathway (2021)</a></div>
        <div class="pub-authors">Zhang, Z.<br/>Committee Members: Dr. Chien-Ju Ho, Dr. Ulugbek Kamilov, and Dr. Carlos Ponce</div>
        <div class="pub-venue"><b>Washington University in St. Louis, McKelvey School of Engineering, Department of Computer Science Master Thesis Dissertation</b></div>
        <div class="pub-abstract">Do artificial neurons in CNNs learn to represent the same visual information as the biological neurons in primate brains? Previous studies have shown that the visual recognition pathway (ventral stream) in humans and monkeys increasingly represents animate objects. We used a heatmap attribution technique borrowed from convolutional neural networks to generate biological feature maps identifying regions in scenes that elicit responses from neurons along the ventral stream (V1/V2, V4, and IT). We found that image regions containing animals elicited increasingly larger responses along the ventral stream, while such animacy features are not represented in artificial neural networks.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="CNN Ventral Pathway" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Shape Recognition in Ultrasound with Deep Learning (2020)</div>
        <div class="pub-authors">Zhang, Z., Miao, H., & Liao, X.</div>
        <div class="pub-venue"><b>Washington University in St. Louis, McKelvey School of Engineering, Department of Electrical and Systems Engineering Capstone Design Thesis</b></div>
        <div class="pub-abstract">Ultrasound is one of the most common imaging techniques in clinical settings, but its functionalities are limited by its low resolution and high dependency on the operator skills. Here, we applied a pre-trained neural network to recognize geometric shapes in ultrasound images of 3D-printed samples. We achieved 96% task accuracy and created a database available for future research in ultrasound imaging.</div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/paper_fig/" alt="Ultrasound Shape Recognition" />
    </div>
</div>

## Undergraduate Projects

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Internet of Things: Incubator</div>
        <div class="pub-authors">Victoria Zhang, Xingjue Liao (2019)</div>
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
        <img src="/assets/img/projects/" alt="IoT Incubator Project" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Internet of Things: Mini Garage Controller</div>
        <div class="pub-authors">Victoria Zhang, Xingjue Liao (2019)</div>
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
        <img src="/assets/img/projects/" alt="Garage Controller Project" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Computer Vision Projects in Python</div>
        <div class="pub-authors">Victoria Zhang (2019)</div>
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
        <img src="/assets/img/projects/" alt="Computer Vision Projects" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">Web Development: To-do List</div>
        <div class="pub-authors">Victoria Zhang (2019)</div>
        <div class="pub-venue"><b>React.js, Web Development</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> React.js, JavaScript, HTML, CSS<br/>
            Interactive web application for task management with modern React.js framework.
            <!-- [\[CODE\]](https://wustlcse204.github.io/09-todo-react-ZhanqiZhang66/) -->
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/projects/" alt="Todo List Web App" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">3D Rotational Robotics in Simulink and Matlab</div>
        <div class="pub-authors">Victoria Zhang (2018)</div>
        <div class="pub-venue"><b>Matlab, Simulink, Robotics</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> MATLAB, Simulink, Robotics Control Systems<br/>
            Development of 3D rotational robotics control systems using MATLAB and Simulink for kinematic and dynamic analysis.
[\[CODE\]](https://github.com/ZhanqiZhang66/3R-Robotics)  
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/projects/" alt="3D Robotics Project" />
    </div>
</div>

<div class="publication-row">
    <div class="publication-content">
        <div class="pub-title">AI Tic-tac-toe and Gomoku Game</div>
        <div class="pub-authors">Victoria Zhang (2018)</div>
        <div class="pub-venue"><b>C++, Artificial Intelligence</b></div>
        <div class="pub-abstract">
            <strong>Technologies:</strong> C++, AI Algorithms, Game Theory<br/>
            Implementation of artificial intelligence algorithms for classic board games including tic-tac-toe and Gomoku with intelligent move prediction and strategy optimization.
[\[CODE\]](https://github.com/ZhanqiZhang66/AI-Gomuku)
        </div>
    </div>
    <div class="publication-image">
        <img src="/assets/img/projects/" alt="AI Game Project" />
    </div>
</div>
