import tkinter as tk
from tkinter import ttk
import threading
import sqlite3
import time
import os


class AppGUI:
    def __init__(self, controller):
        self.controller = controller

        self.root = tk.Tk()
        self.root.title("Anonymous Tracking System")
        self.root.geometry("520x420")
        self.root.configure(bg="#2c3e50")

        self.container = tk.Frame(self.root, bg="#2c3e50")
        self.container.pack(fill="both", expand=True)

        self.show_main_menu()

        self.root.mainloop()

    
    def show_main_menu(self):
        self.clear_screen()

        tk.Label(
            self.container,
            text="Anonymous Tracking",
            font=("Arial", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=20)

        tk.Button(
            self.container,
            text="Start Camera",
            command=self.start_camera,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.container,
            text="Run Sample Video",
            command=self.run_sample,
            bg="#2980b9",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.container,
            text="View Database",
            command=self.show_database,
            bg="#8e44ad",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(pady=10)

        tk.Button(
            self.container,
            text="Exit",
            command=self.root.destroy,
            bg="#c0392b",
            fg="white",
            font=("Arial", 12),
            width=20,
            height=2
        ).pack(pady=10)

    
    def start_camera(self):
        threading.Thread(
            target=self.controller.run,
            args=(0,),
            daemon=True
        ).start()

    def run_sample(self):
        video_path = "sample.mp4"
        if not os.path.exists(video_path):
            print("❌ sample.mp4 not found")
            return

        threading.Thread(
            target=self.controller.run,
            args=(video_path,),
            daemon=True
        ).start()

    
    def show_database(self):
        self.clear_screen()

        tk.Label(
            self.container,
            text="Database Records",
            font=("Arial", 16, "bold"),
            fg="white",
            bg="#2c3e50"
        ).pack(pady=10)

        tree = ttk.Treeview(self.container)
        tree["columns"] = ("ID", "First Seen", "Last Seen")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("ID", anchor=tk.CENTER, width=80)
        tree.column("First Seen", anchor=tk.CENTER, width=150)
        tree.column("Last Seen", anchor=tk.CENTER, width=150)

        tree.heading("#0", text="")
        tree.heading("ID", text="ID")
        tree.heading("First Seen", text="First Seen")
        tree.heading("Last Seen", text="Last Seen")

        tree.pack(fill="both", expand=True, pady=10)

        conn = sqlite3.connect("tracking.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, first_seen, last_seen FROM people")

        for row in cursor.fetchall():
            first_seen = time.strftime('%H:%M:%S', time.localtime(row[1]))
            last_seen = time.strftime('%H:%M:%S', time.localtime(row[2]))

            tree.insert("", "end", values=(row[0], first_seen, last_seen))

        conn.close()

        tk.Button(
            self.container,
            text="Back",
            command=self.show_main_menu,
            bg="#f39c12",
            fg="white",
            width=15
        ).pack(pady=10)

    
    def clear_screen(self):
        for widget in self.container.winfo_children():
            widget.destroy()