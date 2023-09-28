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

You can also view all my repositories from <a href="https://github.com/ZhanqiZhang66?tab=repositories">here<a/>
<br />
    
<h2>
    <a name='Conferences and Publications'></a> Conferences and Publications
</h2>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Semi-supervised quantification and interpretation of undirected human behavior. </strong><br/>
           <strong>Zhang, Z.</strong>, Yang, Y., Sheehan, T., Chou, C., Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2023). <br />
                    <i>Accepted as poster for <a href="https://www.cosyne.org/">Computational and Systems Neuroscience (COSYNE) 2023</a> </i>
        </p>
         <p class="media-heading" style="font-size:15px">Undirected behavior reflects cognitive functions and provides insights for diagnosing psychiatric conditions such as bipolar disorder (BD) (McReynolds, 1962). Open-field animal behaviors have been well-studied for this purpose; however, a corresponding human subject paradigm is still lacking, and quantifying complex spontaneous human behaviors is challenging. Here, we demonstrate a semi-supervised model to quantify undirected human behavior, differentiate subtle hallmark behavioral features of BD, and create a natural language generative model to provide nuanced interpretations of behaviors with context information. We collected videos of BD (n=12) and control (n=12) human participants freely interacting in an unexplored room with each video manually annotated into 6 categories (e.g., walk). We used DeepLabCut (Mathis et al, 2018) to track the spatiotemporal postures of the participants coupled with the VAME latent variable model (Luxem et al, 2021) to encode pose sequences into latent representations. We then clustered the latent representations into 10 behavioral motifs. To interpret these motifs, we independently described example clips using natural language. Using these descriptions, we created a novel transformer-based model that generated interpretable descriptions for each cluster. We found the dwell time of motif “approach, inspect, move along” is significantly lower in the BD population compared with controls (two sample t-test, p-value: 0.04), while no significance was found from manually annotated categories. We then used transition matrices to characterize how participants transitioned between motifs. We found BD to have sparser transition matrices in the second half of the video which reflected more stereotyped behavior and a smaller behavioral repertoire. We quantified this using the entropy of the transition matrix and found BD patients to have significantly different entropy between the first and the second half of the video (F test for equal variances, p-value: 0.01). Our analysis identifies fine-resolution behavioral motifs that can distinguish BD using undirected human behavior.
        </p>
    </div>
</div>

<div class="media">
    <div class="media-body">
       <p class="media-heading">
         <strong>Unsupervised quantification of undirected human behavior for bipolar disorder analysis. </strong><br/>
           <strong>Zhang, Z.</strong>, Rosberg, H., Perry, W., Young, J., Minassian, A., Mishne, G., & Aoi, M. (2022). <br />
                    <i>Accepted as a spotlight poster for <a href="https://brain.ieee.org/event/ieee-brain-discovery-and-neurotechnology-workshop/">IEEE Brain Discovery Neurotechnology Workshop – Brain Mind Body Cognitive Engineering for Health and Wellness 2022</a> and <a href="https://www.sfn.org/meetings/neuroscience-2021">Society for Neuroscience (SfN) 2022</a> </i>
        </p>   
    </div>
</div>

<div class="media">
    <div class="media-body">
       <p class="media-heading">
                   <strong>Animal-feature Encoding in Macaque Brain and in Artificial Networks. </strong><br/>
           <strong>Zhang, Z.</strong>, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R. (2022). <br />
                    <i>Accepted as a spotlight poster for <a href="https://www.sfn.org/meetings/neuroscience-2021">Society for Neuroscience (SfN) 2022</a> </i>
        </p>
    </div>
</div>

<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Do you see what I see? Representations in brains and neural networks. Brain-Score and Beyond: Confronting Brain-like ANNs with Neuroscientific Data. </strong><br/>
           <strong>Zhang, Z.</strong>, Ponce, C. R. (2022). <br /> 
                   <i>Accepted as a workshop presentation for <a href="https://www.cosyne.org/">Computational and Systems Neuroscience (COSYNE) 2022</a> </i>
        </p>
    </div>
</div>


<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>The Macaque Ventral Stream Shows A Hierarchical Structure for Animal-feature Encoding (2021)</strong><br />
          <strong>Zhang, Z.</strong>, Hartmann, T. S., Livingstone, M. S., Born, R. T., & Ponce, C. R.<br />
           <i>Accepted as abstract for <a href="https://www.sfn.org/meetings/neuroscience-2021">Society for Neuroscience (SfN) 2021</a> and <a href="https://abstracts.g-node.org/conference/BC21/abstracts#/uuid/bbb01455-e0b9-4521-bbe1-9c7c0ba4389c">Bernstein Conference 2021</a> </i>
               <br/>
       </p>
       <p class="media-heading" style="font-size:15px"> Are there organizing principles for information encoding along the primate ventral stream? Neurons in each visual area are often tested with different types of stimuli, ranging from simple (e.g., lines in V1) to complex (faces in inferotemporal cortex, IT); however, this strategy limits functional comparisons across areas. By comparing neuronal responses to a given stimulus set across areas, we set out to identify brain-wide organizing principles and determine if these principles are shared by learning-based models of the ventral stream (convolutional neural networks, CNNs)
        </p>
    </div>
</div>


<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Translating Convolutional Neural Networks Approach to the Ventral Pathway (2021)</strong><br />
          <strong>Zhang, Z. </strong><br />
           Committee Members: Dr. Chien-Ju Ho, Dr. Ulugbek Kamilov, and Dr. Carlos Ponce<br />
           <i>Washington University in St. Louis, McKelvey School of Engineering, Department of Computer Science Master Thesis Dissertation</i><br/>
       </p>
       <p class="media-heading" style="font-size:15px">Do artificial neurons in CNNs learn to represent the same visual information as the biological neurons in primate brains? Previous studies have shown that the visual recognition pathway (ventral stream) in humans and monkeys increasingly represents animate objects. We used a heatmap attribution technique borrowed from convolutional neural networks to generate biological feature maps identifying regions in scenes that elicit responses from neurons along the ventral stream (V1/V2, V4, and IT). Biological feature maps were then compared to activation maps produced by units in convolutional neural networks. We found that image regions containing animals elicited increasingly larger responses along the ventral stream, while such animacy features are not represented in artificial neural networks.
           <br/>
        <a href="https://openscholarship.wustl.edu/eng_etds/574/">[PDF]</a><br />
        </p>
    </div>
</div>

<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Shape Recognition in Ultrasound with Deep Learning (2020)</strong><br />
           <strong>Zhang, Z.</strong>, Miao, H., & Liao, X. <br />
          <i>Washington University in St. Louis, McKelvey School of Engineering, Department of Electrical and Systems Engineering Capstone Design Thesis</i><br/>
        </p>
         <p class="media-heading" style="font-size:15px">Ultrasound is one of the most common imaging techniques in clinical settings, but its functionalities are limited by its low resolution and high dependency on the operator skills. Here, we applied a pre-trained neural network to recognize geometric shapes in ultrasound images of 3D-printed samples. We achieved 96% task accuracy and created a database available for future research in ultrasound imaging.
        </p>
    </div>
</div>


<h2>
     <a name='Projects'></a> Undergrad Projects
</h2>
<h3>
    <a name='2019'></a> 2019
</h3>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Internet of Things: incubator</strong><br />
          Victoria Zhang, Xingjue Liao<br />
          <ul>
            <li>Plastic bottles: recycle and reuse </li>
            <li>Hardware: wires, resistors, fan, Adafruit SI7021, Photon, Arduino...
</li>
            <li>Embedded system: Sensors and Actuators + Feedback Control 
</li>
            <li>UI: graphical sliders and other information of the incubator. 
</li>  
              <li>Networking infrastructure: monitor and control the incubator remotely
</li>             
</ul>
          <a href="https://github.com/ZhanqiZhang66/Incubator">[CODE]</a><br />
       </p>
    </div>
</div>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Internet of Things: Mini Garage Controller</strong><br />
         Victoria Zhang, Xingjue Liao<br />
               <ul>
            <li>Hardware: wires, resistors, buttons, LEDS, Two Photons
</li>
            <li>Embedded system: Sensors and Actuators + Remote Control 
</li>
            <li>UI: responsive website and app
</li>      
        <li>Networking infrastructure: monitor and control the garage light and door remotely
</li>   
           <li>Functionality: Close the door and turn of the light automatically with the time setted
</li>
</ul>
        <a href="https://github.com/ZhanqiZhang66/GarageController">[CODE]</a><br />
       </p>
    </div>
</div>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Computer Vision Projects</strong><br />
          <b>Victoria Zhang</b><br />
           <li>Edge detection + Line detection
</li>
            <li>Image Restoration & Optimization
</li>
            <li>Photometric Stereo
</li>      
        <li>Camera Projection and Transformations
</li>   
           <li>Estimation, Sampling, Robust Fitting
</li>
                      <li>Epipolar Geometry, Binocular Stereo
</li>
                      <li>Optical flow
</li>
                      <li>Neural Networks
</li>
           <li>Semantic Vision Tasks
</li>
                      <li>GAN and VAEs. Unsupervised Learning.
</li>
          This work currently can't be viewed publicly due to the course policy<br />
          Please Email me for more information.
       </p>
    </div>
</div>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>Web development: To-do List</strong><br />
          <b>Victoria Zhang</b><br />
          <a href="https://wustlcse204.github.io/09-todo-react-ZhanqiZhang66/">[CODE]</a><br />
       </p>
    </div>
</div>
<h3>
    <a name='2018'></a> 2018
</h3>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>3D Rotational ROBOTICS</strong><br />
          Victoria Zhang, Ben Miao<br />
            <a href="https://github.com/ZhanqiZhang66/3R-Robotics">[CODE]</a><br />
       </p>
    </div>
</div>
<div class="media">
    <div class="media-body">
       <p class="media-heading">
          <strong>AI tic-tac-toe and Gomoku</strong><br />
          <b>Victoria Zhang</b><br />
          <a href="https://github.com/ZhanqiZhang66/AI-Gomuku">[CODE]</a><br />
       </p>
    </div>
</div>
