import tkinter as tk
from tkinter import filedialog
import subprocess
import sys
import threading
import os

def run_app(source):
    subprocess.run([sys.executable, "main.py", source])

def run_thread(source):
    thread = threading.Thread(target=run_app, args=(source,))
    thread.start()

def open_camera():
    run_thread("0")

def open_file():
    file_path = filedialog.askopenfilename(
        title="Select Video",
        filetypes=[("Video Files", "*.mp4 *.avi *.mov")]
    )
    if file_path:
        run_thread(file_path)

def open_sample():
    path = os.path.join("data", "sample.mp4")
    if os.path.exists(path):
        run_thread(path)
    else:
        status_label.config(text="Sample video not found!", fg="red")


root = tk.Tk()
root.title("Anonymous Tracking System")
root.geometry("500x400")
root.configure(bg="#1e1e2f") 


title = tk.Label(root,
                 text="Anonymous Tracking",
                 font=("Helvetica", 20, "bold"),
                 bg="#1e1e2f",
                 fg="white")
title.pack(pady=30)


btn_style = {
    "width": 20,
    "height": 2,
    "font": ("Helvetica", 12),
    "bg": "#4CAF50",
    "fg": "white",
    "bd": 0,
    "activebackground": "#45a049"
}


btn_camera = tk.Button(root, text="Open Camera", command=open_camera, **btn_style)
btn_camera.pack(pady=10)

btn_file = tk.Button(root, text="Select Video", command=open_file, **btn_style)
btn_file.pack(pady=10)

btn_sample = tk.Button(root, text="Sample Video", command=open_sample, **btn_style)
btn_sample.pack(pady=10)


status_label = tk.Label(root,
                        text="",
                        font=("Helvetica", 10),
                        bg="#1e1e2f",
                        fg="white")
status_label.pack(pady=20)


root.mainloop()