import sqlite3
import threading
import numpy as np


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("tracking.db", check_same_thread=False)
        self.lock = threading.Lock()
        self.create_table()

    def create_table(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY,
                    feature BLOB,
                    first_seen REAL,
                    last_seen REAL
                )
            """)
            self.conn.commit()

    def save_feature(self, person_id, feature):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO people VALUES (?, ?, ?, ?)",
                (person_id, feature.tobytes(), 0, 0)
            )
            self.conn.commit()

    def update_person(self, person_id):
        import time
        with self.lock:
            cursor = self.conn.cursor()
            now = time.time()

            cursor.execute("SELECT id FROM people WHERE id=?", (person_id,))
            exists = cursor.fetchone()

            if exists:
                cursor.execute(
                    "UPDATE people SET last_seen=? WHERE id=?",
                    (now, person_id)
                )
            else:
                cursor.execute(
                    "INSERT INTO people (id, first_seen, last_seen) VALUES (?, ?, ?)",
                    (person_id, now, now)
                )

            self.conn.commit()

    def get_all_features(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, feature FROM people")

            data = []
            for row in cursor.fetchall():
                feature = np.frombuffer(row[1], dtype=np.float32)
                data.append((row[0], feature))

            return data

    def get_max_id(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(id) FROM people")
            result = cursor.fetchone()[0]
            return result if result else 0