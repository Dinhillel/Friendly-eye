import cv2
from yolo_detector import YOLODetector  

def open_camera(index=0, width=1280, height=720):
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width) #רוחב הפריים
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)# גובה הפריים
    return cap         

def draw_detections(frame, detections):
    for det in detections: 
        x1, y1, x2, y2 = det["box"]
        label = f"{det['label']} {det['conf']:.2f}"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, max(0, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame

if __name__ == "__main__":
    # Create an instance of YOLO
    detector = YOLODetector(model_path="yolov8n.pt", conf=0.35)

    
    cap = open_camera()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # זיהוי אובייקטים
        detections = detector.detect(frame)

        # ציור התיבות על המסך
        frame = draw_detections(frame, detections)

        # הצגת המסך
        cv2.imshow("YOLO Detection", frame)

        # יציאה בלחיצה על 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    #פותח מצלמה ומבצע זיהוי אובייקטים בזמן אמת
