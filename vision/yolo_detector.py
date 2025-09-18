from ultralytics import YOLO
import torch

class YOLODetector:
    def __init__(self, model_path="yolov8n.pt", conf=0.50, device=None):
        # load the model 
        self.model = YOLO(model_path)
        
        
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        self.model.to(self.device)
        
        self.conf = conf

    def detect(self, frame):
        """
        מקבל frame (numpy array BGR מ-OpenCV)
        ומחזיר רשימת detections:
        [
            {"label": "person", "conf": 0.87, "box": (x1,y1,x2,y2)},
            ...
        ]
        """
        #run the model on the frame
        results = self.model(frame, conf=self.conf, verbose=False)
        r = results[0]
        names = self.model.names
        
        # collect te detections
        detections = []
        for box in r.boxes:
            cls_id = int(box.cls)
            label = names[cls_id]
            conf = float(box.conf)
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            detections.append({
                "label": label,
                "conf": conf,
                "box": (x1, y1, x2, y2)
            })
        
        return detections
    
    #מנתח תמונה מזהה אובייקטים ומחזיר רשימת זיהויים
