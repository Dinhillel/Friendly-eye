import cv2
from collections import Counter
from vision.yolo_detector import YOLODetector
from vision.ocr import extract_text_from_image
from nlp.t5model import T5Responder
from audio.tts import Speaker

# STT import (Whisper) 
try:
    from audio.stt import record_to_file, transcribe
    whisper_enabled = True
except ImportError:
    whisper_enabled = False

# --- Models initialization ---
try:
    detector = YOLODetector(model_path="yolov8n.pt", conf=0.35)
except Exception as e:
    print(f"Error loading YOLO model: {e}")
    detector = None

try:
    t5 = T5Responder(model_name="google/t5-v1_1-small")
except Exception as e:
    print(f"Error loading T5 model: {e}")
    t5 = None

speaker = Speaker(rate=180, volume=1.0)

# --- Function to summarize YOLO detections ---
def summarize_detections(detections):
    if not detections:
        return "no notable objects"
    counts = Counter([d["label"] for d in detections])
    parts = []
    for label, n in counts.items():
        if n == 1:
            parts.append(label)
        else:
            parts.append(f"{n} {label}s")
    return ", ".join(parts)

#  Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = []
    context_text = "no notable objects"

    # --- YOLO detection ---
    if detector:
        try:
            detections = detector.detect(frame)
            context_text = summarize_detections(detections)
        except Exception as e:
            print(f"YOLO detection failed: {e}")

    # --- OCR detection ---
    try:
        ocr_text = extract_text_from_image(frame)
        if ocr_text.strip():
            context_text += ". Text detected: " + ocr_text
    except Exception as e:
        print(f"OCR failed: {e}")

    # --- STT input (optional) ---
    if whisper_enabled:
        try:
            record_to_file("user_input.wav")  # מקליט ממשתמש
            user_text = transcribe("user_input.wav")
            if user_text.strip():
                context_text += ". User said: " + user_text
        except Exception as e:
            print(f"STT failed: {e}")

    # --- T5 NLP ---
    sentence = context_text
    if t5:
        try:
            sentence = t5.answer("Describe the scene.", context_text)
        except Exception as e:
            print(f"T5 generation failed: {e}")

    # --- TTS ---
    try:
        speaker.say(sentence, wait=False)
    except Exception as e:
        print(f"TTS failed: {e}")

    # --- Draw YOLO detections ---
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        label = f"{det['label']} {det['conf']:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, max(0, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("YOLO + OCR + STT + NLP + TTS", frame)

    # --- Exit on 'q' ---
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
