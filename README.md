
# TOBB ETÜ ELE 495 - Lightning95

<center><img src="https://cdn.discordapp.com/attachments/1186721999326822433/1263371407862267966/github_logo.png?ex=6699fdcf&is=6698ac4f&hm=59bb0088ad7243b93867bf8fef9736b95205daf0b1d3d1edd56605c108f0351b&" /></center>

# Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Block Diagram](#block-diagram)
- [Images](#images)
- [Video](#video)
- [Acknowledgements](#acknowledgements)

## Introduction
This project involves developing a JetBot, powered by the Jetson Nano, to recognize numbers using the SSD MobileNet V2 neural network. The JetBot is designed to identify license plate numbers and match them with information provided by users through a mobile application interface.

## Features

-   **Jetson Nano Platform:** Utilizes the computational power of the Jetson Nano for real-time processing and number recognition.
-   **SSD MobileNet V2:** Implements the SSD MobileNet V2 model for efficient and accurate number detection.
-   **Mobile Application Interface:** Allows users to input license plate information through a user-friendly mobile application.
-   **Integration with JetBot:** Ensures seamless communication between the mobile application and the JetBot, enabling real-time updates and interactions.

## Requirements
This project needs the following python libraries:

 - firebase-admin
 - jetbot
 - jetson-inference
 - jetson-utils

## Block Diagram
<p align = 'center'><img src='https://i.hizliresim.com/f4lx1ta.png' /></p>

## Images
<p align = 'center'><img src='https://i.hizliresim.com/e0wd4k9.jpg' /></p>

## Video
[![Video](https://resmim.net/cdn/2024/07/17/WHtK7R.jpg)](https://youtu.be/mZFRf9zGdFs)

## Acknowledgements

This project was made possible by the resources and support from several key contributors and platforms. We would like to extend our gratitude to the following:

[JetBot](https://jetbot.org/master/): The open-source AI robot platform which served as the foundation for this project. JetBot provides a comprehensive framework for building and deploying AI-powered robots, and its documentation and community support were invaluable.

[Jetson Inference by dusty-nv](https://github.com/dusty-nv/jetson-inference): The incredible work by Dusty NV on the Jetson Inference library was essential for implementing the SSD MobileNet V2 model. This library offers a robust collection of resources for real-time object detection, classification, and segmentation, which significantly streamlined the development process.

Thank you to the entire open-source community and the developers behind these platforms for their contributions and dedication to advancing AI technology.
