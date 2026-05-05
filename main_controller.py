import cv2
import numpy as np
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

from reid import ReID
from database import Database


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class MainController:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

        
        self.tracker = DeepSort(
            max_age=15,
            n_init=3,
            max_cosine_distance=0.3
        )

        self.reid = ReID()
        self.db = Database()

        self.memory = {}
        self.next_id = self.db.get_max_id() + 1

        self.running = False  

    
    def run(self, source=0, callback=None):
        self.running = True

        cap = cv2.VideoCapture(source)
        window_name = "Tracking"

        cv2.namedWindow(window_name)

        while self.running:
            ret, frame = cap.read()
            if not ret:
                break

            results = self.model(frame)[0]
            detections = []

            
            for box in results.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if cls == 0 and conf > 0.8:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w = x2 - x1
                    h = y2 - y1

                    
                    if w < 60 or h < 120:
                        continue

                    if w * h < 8000:
                        continue

                    detections.append(([x1, y1, w, h], conf, 'person'))

            
            tracks = self.tracker.update_tracks(detections, frame=frame)

            active_ids = []

            for track in tracks:
                if not track.is_confirmed():
                    continue

                
                if track.time_since_update > 0:
                    continue

                track_id = track.track_id
                l, t, w, h = map(int, track.to_ltrb())

                
                if track_id in self.memory:
                    person_id = self.memory[track_id]
                else:
                    feature = self.reid.extract(frame, (l, t, w, h))
                    if feature is None:
                        continue

                    known_people = self.db.get_all_features()

                    best_id = None
                    best_score = 0

                    for db_id, db_feat in known_people:
                        score = cosine_similarity(feature, db_feat)

                        if score > 0.65 and score > best_score:
                            best_id = db_id
                            best_score = score

                    if best_id is not None:
                        person_id = best_id
                    else:
                        person_id = self.next_id
                        self.next_id += 1
                        self.db.save_feature(person_id, feature)

                    self.memory[track_id] = person_id

                active_ids.append(person_id)

                
                cv2.rectangle(frame, (l, t), (l + w, t + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"ID {person_id}",
                    (l, t - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                self.db.update_person(person_id)

            if callback:
                callback(list(set(active_ids)))

            
            cv2.imshow(window_name, frame)

            
            key = cv2.waitKey(1)
            if key == 27:
                break

            
            try:
                if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
            except:
                break

        
        self.running = False
        cap.release()
        cv2.destroyAllWindows()
        cv2.waitKey(1)

    
    def stop(self):
        self.running = False