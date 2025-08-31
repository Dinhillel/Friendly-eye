<img width="1024" height="1024" alt="image" src="https://github.com/user-attachments/assets/31e441c4-a7f5-43f4-8228-af222c4c6169" />

Assistive Vision System for Visually Impaired people

Project Overview:
This project is an intelligent assistive technology solution designed to help visually impaired people interact with their environment through real-time computer vision and natural language processing. The system combines multiple AI components to provide seamless voice-based interaction with the visual world. Core Functionality The system enables users to ask natural language questions about their surroundings and receive spoken responses. 

For example:
User: "What is in front of me?" System: "There is a red chair and a table in front of you."

✨ Features

🔍 Computer Vision Real-time Object Detection: Uses YOLOv8 for accurate object recognition Multi-dataset Training: Trained on COCO and Data-image-captioning datasets Live Camera Feed: Processes video stream in real-time Confidence Scoring: Provides detection confidence levels.

🎙️ Audio Processing Speech-to-Text: Whisper-based voice command recognition Text-to-Speech: Natural voice feedback with pyttsx3 Multi-language Support: Configurable language settings Voice Commands: Interactive voice-controlled interface

🧠 Natural Language Processing Question Answering: T5-based contextual understanding Scene Description: Intelligent interpretation of visual context Conversational Interface: Natural language interaction

⚡ Performance
Real-time Processing: 30 FPS camera processing GPU Acceleration: CUDA support for faster inference Optimized Models: Lightweight models for efficient processing

🗂️ Dataset
https://www.kaggle.com/datasets/aishrules25/automatic-image-captioning-for-visually-impaired
-  **Question Answering (NLP)** using T5 model
-  **Speech-to-Text (STT)** using Whisper or another STT module
-  **Text-to-Speech (TTS)** with Coqui TTS / pyttsx3
-  Real-time camera support with OpenCV

git clone https://github.com/Dinhillel/Friendly-eye.git

