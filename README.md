Assistive Vision System for Visually Impaired Users

 Project Overview
This project is an intelligent assistive technology solution designed to help visually impaired users interact with their environment through real-time computer vision and natural language processing. The system combines multiple AI components to provide seamless voice-based interaction with the visual world.
Core Functionality
The system enables users to ask natural language questions about their surroundings and receive spoken responses. For example:

User: "What is in front of me?"
System: "There is a red chair and a table in front of you."

✨ Features

🔍 Computer Vision
Real-time Object Detection: Uses YOLOv8 for accurate object recognition
Multi-dataset Training: Trained on COCO and VizWiz VQA datasets
Live Camera Feed: Processes video stream in real-time
Confidence Scoring: Provides detection confidence levels

🎙️ Audio Processing
Speech-to-Text: Whisper-based voice command recognition
Text-to-Speech: Natural voice feedback with pyttsx3
Multi-language Support: Configurable language settings
Voice Commands: Interactive voice-controlled interface

🧠 Natural Language Processing
Question Answering: T5-based contextual understanding
Scene Description: Intelligent interpretation of visual context
Conversational Interface: Natural language interaction

⚡ Performance

Real-time Processing: 30 FPS camera processing
GPU Acceleration: CUDA support for faster inference
Optimized Models: Lightweight models for efficient processing

 System Architecture
 ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Camera Input  │───▶│ YOLO Detector   │───▶│ Object Context  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             ▼
│  Voice Output   │◀───│   T5 Responder  │◀───┌─────────────────┐
└─────────────────┘    └─────────────────┘    │ Scene Analysis  │
        ▲                                     └─────────────────┘
        │                                              ▲
┌─────────────────┐    ┌─────────────────┐             │
│   TTS Engine    │◀───│ Voice Question  │─────────────┘
└─────────────────┘    └─────────────────┘
        ▲                        ▲
        │                        │
┌─────────────────┐    ┌─────────────────┐
│    Speaker      │    │ STT (Whisper)   │
└─────────────────┘    └─────────────────┘
                                ▲
                       ┌─────────────────┐
                       │ Microphone      │
                       └─────────────────┘

VISION_MODEL/
├── app/

├── config.py        # Configuration settings

├── main.py          # Main application entry point
│ 
└── pipeline.py      # Main processing pipeline
├── vision/
│   ├── opencv.py        # OpenCV camera utilities
│   └── yolo_detector.py # YOLO object detection module
├── audio/
│   ├── stt.py          # Speech-to-Text processing
│   └── tts.py          # Text-to-Speech synthesis
├── nlp/
│   └── t5model.py      # T5 question-answering model
├── Dataset_vizwiz/     # VizWiz dataset (excluded from git)
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
├── download_vizwiz.py  # Dataset download script
├── requirements.txt    # Python dependencies
└── README.md          # This file

 Clone the Repository:
git clone https://github.com/DinHillel/Eye-Frindly.git
cd Frindly-Eye
                       

