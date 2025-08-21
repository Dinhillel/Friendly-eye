import cv2
from collections import Counter
from yolo_detector import YOLODetector
from t5model import T5Responder
from speaker import Speaker
try:
    from audio.stt import record_to_file, transcribe
    whisper_enabled = True
except ImportError:
    whisper_enabled = False

# --- אתחול המודלים ---
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

# --- פונקציה לסיכום detections ---
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

#  מצלמה 
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    detections = []
    context_text = "no notable objects"

    #  YOLO detection 
    if detector:
        try:
            detections = detector.detect(frame)
            context_text = summarize_detections(detections)
        except Exception as e:
            print(f"YOLO detection failed: {e}")

    #  T5 NLP 
    sentence = context_text
    if t5:
        try:
            sentence = t5.answer("Describe the scene.", context_text)
        except Exception as e:
            print(f"T5 generation failed: {e}")

    # TTS 
    try:
        speaker.say(sentence, wait=False) #for to whit the user finish to talk
    except Exception as e:
        print(f"TTS failed: {e}")

    #  ציור התיבות והטקסט על המסך 
    for det in detections:
        x1, y1, x2, y2 = det["box"]
        label = f"{det['label']} {det['conf']:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, max(0, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow("YOLO + NLP + TTS", frame)

    #  יציאה בלחיצה על 'q' -
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


