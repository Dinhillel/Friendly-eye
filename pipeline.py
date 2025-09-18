import cv2
from vision.yolo_detector import YOLODetector
from vision.opencv import open_camera, draw_detections
from nlp.t5model import T5Responder
from audio.tts import Speaker
from audio.stt import record_to_file, transcribe
from app.config import config

def summarize_detections(detections):
    """
    Summarize detections into a context string.
    """
    if not detections:
        return "No objects detected."
    labels = [det['label'] if isinstance(det, dict) and 'label' in det else str(det) for det in detections]
    return "Detected: " + ", ".join(labels)


def run_loop():
    # Initialize systems
    detector = YOLODetector(config.YOLO_MODEL, conf=config.YOLO_CONF)
    responder = T5Responder(model_name=config.T5_MODEL, max_new_tokens=config.MAX_NEW_TOKENS)
    speaker = Speaker(rate=config.TTS_RATE, volume=config.TTS_VOLUME, voice=config.TTS_VOICE)

    cap = open_camera(config.CAM_INDEX)
    print("Controls: press 'S' to speak a question (3s), 'Q' to quit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        # Detect objects
        detections = detector.detect(frame)
        context = summarize_detections(detections)

        # Draw for developer preview
        if config.SHOW_WINDOW:
            draw_detections(frame, detections)
            cv2.putText(frame, f"Context: {context}", (10, 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow("Assistive Vision", frame)

        key = cv2.waitKey(1) & 0xFF
        if key in (ord('q'), ord('Q')):
            break
        elif key in (ord('s'), ord('S')):
            # Record a short voice query and transcribe
            wav_path = config.AUDIO_TMP
            record_to_file(wav_path, seconds=3.0)
            try:
                question = transcribe(wav_path, model_size=config.WHISPER_SIZE, language=config.WHISPER_LANGUAGE)
            except Exception as e:
                print("STT error:", e)
                question = ""  # fallback

            if question:
                print("User:", question)
                try:
                    answer = responder.answer(question, context)
                except Exception as e:
                    print("NLP error:", e)
                    answer = "Sorry, I couldn't process your question."
                print("Assistant:", answer)
                speaker.say(answer)
 
    cap.release()
    if config.SHOW_WINDOW:
        cv2.destroyAllWindows()
