
# TOBB ETÜ ELE 495 - Lightning95

<center><img src="https://i.hizliresim.com/pj5m2ox.png" /></center>

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

**firebase-admin:** The firebase-admin library is part of Firebase, a platform developed by Google for creating mobile and web applications. The firebase-admin SDK is used for server-side interactions with Firebase services, providing functionalities like authentication, real-time database, cloud storage, cloud messaging, and more. It allows backend services to access Firebase features securely and manage Firebase projects programmatically.

**jetbot:** The jetbot is an open-source AI robot platform based on NVIDIA Jetson Nano. It is designed for robotics and AI education. The library includes tools and examples to build and program your own robot using the Jetson Nano, enabling projects involving computer vision, machine learning, and robotics. JetBot simplifies working with hardware components and sensors, making it easier to prototype and test robotics applications.

**jetson-inference:** The jetson-inference is a library for deploying deep learning models on NVIDIA Jetson platforms. It provides a collection of pre-trained models for image classification, object detection, segmentation, and other tasks, along with tools for model training and inference. The library is optimized for Jetson devices, enabling high-performance AI applications in areas like autonomous machines, robotics, and IoT.

**jetson-utils:** The jetson-utils is a utility library for NVIDIA Jetson platforms that provides functions for video streaming, image processing, and multimedia. It includes tools for handling camera inputs, video encoding/decoding, image manipulation, and more. The library is designed to work seamlessly with other Jetson libraries like jetson-inference, providing a robust framework for developing AI and multimedia applications on Jetson devices.

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
