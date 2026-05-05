from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self):
        self.tracker = DeepSort(
            max_age=60,              
            n_init=3,
            max_cosine_distance=0.3
        )

    def update(self, detections, frame):
        tracks = self.tracker.update_tracks(detections, frame=frame)

        results = []

        for t in tracks:
            if not t.is_confirmed():
                continue

            track_id = t.track_id
            l, t_, w, h = map(int, t.to_ltrb())

            results.append({
                "id": track_id,
                "bbox": (l, t_, w, h)
            })

        return results