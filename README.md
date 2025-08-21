📖 Project Description

This project is designed to assist visually impaired users by providing real-time communication with their surroundings.
The system combines several AI components into a single pipeline:

YOLO object detection to recognize objects in the environment (trained on COCO and VizWiz VQA  datasets).

Speech-to-Text (STT) to capture user voice commands and questions.

NLP (T5) to interpret and answer user questions based on the detected objects.

Text-to-Speech (TTS) to provide natural voice feedback.

With this pipeline, a visually impaired person can ask:

"What is in front of me?"

The system will:

Capture an image from the camera.

Detect objects such as "chair", "table", or "person".

Understand the question using the NLP model.

Answer with natural speech {whisper}  user said:"what heve surrounding me?" 
systam answer:
"There is a red chair and a table in front of you."

The project uses object databases (COCO dataset, VizWiz VQA) to recognize and describe objects, enabling a smoother human–AI.



VISION MODEL/
│── app/
│   ├── config/        
│   ├── main.py          # main script
│   └── pipeline.py      
│── vision/
│   ├── opencv.py        # OpenCV utilities
│   └── yolo_detector.py # YOLO object detection
│── audio/
│   ├── stt/             # Speech-to-Text
│   └── tts/             # Text-to-Speech
│── nlp/
│   └── t5/              # T5 model for question answering
│──Dataset_vizwiz/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   └── labels/
│       ├── train/
│       └── val/
 ──  download_vizwiz
│── requirements.txt
│── README.md



🗂️ Dataset
VizWiz VQA dataset for question-answering
COCO dataset for object detection

 **Object Detection** using YOLO
-  **Question Answering (NLP)** using T5 model
-  **Speech-to-Text (STT)** using Whisper or another STT module
-  **Text-to-Speech (TTS)** with Coqui TTS / pyttsx3
-  Real-time camera support with OpenCV