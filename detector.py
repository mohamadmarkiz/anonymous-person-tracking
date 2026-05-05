from ultralytics import YOLO

class Detector:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        results = self.model(frame)[0]
        detections = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])

            
            if cls == 0 and conf > 0.6:   

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                w = x2 - x1
                h = y2 - y1

                
                if w > 50 and h > 100:
                    detections.append(([x1, y1, w, h], conf, "person"))

        return detections