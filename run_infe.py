from ultralytics import YOLO
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import torch
import subprocess
import cv2
import threading
import time

# Load YOLO model
model = YOLO('best.pt')

# Initialize Tkinter
root = tk.Tk()
root.title("YOLOv10 Inference Prototype")
root.geometry("420x300")
root.resizable(False, False)

# Colors & styles
BUTTON_COLOR = "#4CAF50"
BUTTON_TEXT_COLOR = "#FFFFFF"
EXIT_COLOR = "#F44336"
STATUS_COLOR = "green"
FONT = ("Segoe UI", 11, "bold")

# Status label
status_label = tk.Label(root, text="Ready", fg=STATUS_COLOR, font=("Segoe UI", 10))
status_label.grid(row=0, column=0, columnspan=2, pady=(10, 5))

def update_status(msg, color="green"):
    status_label.config(text=msg, fg=color)

def check_cuda():
    if torch.cuda.is_available():
        device_name = torch.cuda.get_device_name(0)
        update_status(f"✅ Running on GPU: {device_name}")
    else:
        update_status("⚠️ Running on CPU.", "orange")

check_cuda()

def open_folder(path):
    if os.name == 'nt':
        subprocess.run(['explorer', os.path.realpath(path)])
    elif os.name == 'posix':
        subprocess.run(['open', os.path.realpath(path)])
    else:
        messagebox.showinfo("Results Folder", path)

def infer_image():
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if file_path:
        update_status("🖼 Running inference on image...")
        threading.Thread(target=run_infer_image, args=(file_path,)).start()

def run_infer_image(file_path):
    try:
        results = model(file_path, save=True, project='runs', name='detect', device=0)
        result_folder = results[0].save_dir
        update_status(f"✅ Image saved to: {result_folder}")
        open_folder(result_folder)
    except Exception as e:
        update_status(f"❌ Error: {e}", "red")

def infer_video():
    file_path = filedialog.askopenfilename(
        title="Select a Video",
        filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")]
    )
    if file_path:
        update_status("🎥 Running inference on video...")
        threading.Thread(target=run_infer_video, args=(file_path,)).start()

def run_infer_video(file_path):
    try:
        results = model(file_path, save=True, project='runs', name='detect', device=0)
        result_folder = results[0].save_dir
        update_status(f"✅ Video saved to: {result_folder}")
        open_folder(result_folder)
    except Exception as e:
        update_status(f"❌ Error: {e}", "red")

def infer_live_feed():
    update_status("📹 Starting live feed...")
    threading.Thread(target=run_live_feed).start()

def run_live_feed():
    cam_index = -1
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cam_index = i
            cap.release()
            break
        cap.release()

    if cam_index == -1:
        update_status("❌ No camera found.", "red")
        return

    save_dir = os.path.join('runs', 'detect', 'live')
    os.makedirs(save_dir, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    video_path = os.path.join(save_dir, f'live_{timestamp}.mp4')

    cap = cv2.VideoCapture(cam_index)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ))

    prev_time = time.time()
    window_name = "YOLOv10 Live Feed (Press Q to quit)"

    try:
        for result in model.predict(source=cam_index, stream=True, device=0):
            current_time = time.time()
            time_diff = current_time - prev_time
            prev_time = current_time
            fps = 1.0 / time_diff if time_diff > 0 else 0.0
            inference_time = result.speed['inference']

            frame = result.plot()
            text = f"FPS: {fps:.2f} | Inference: {inference_time:.1f} ms"
            cv2.putText(frame, text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow(window_name, frame)
            out.write(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        update_status(f"❌ Live feed error: {e}", "red")
    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()
        update_status(f"✅ Live saved to: {video_path}")
        open_folder(save_dir)

# Buttons
btn_image = tk.Button(root, text="🖼 Image Inference", width=20, height=2,
                      bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT,
                      command=infer_image)
btn_image.grid(row=1, column=0, padx=10, pady=10)

btn_video = tk.Button(root, text="🎥 Video Inference", width=20, height=2,
                      bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT,
                      command=infer_video)
btn_video.grid(row=1, column=1, padx=10, pady=10)

btn_live = tk.Button(root, text="📹 Live Feed", width=20, height=2,
                     bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT,
                     command=infer_live_feed)
btn_live.grid(row=2, column=0, padx=10, pady=10)

btn_results = tk.Button(root, text="📁 Open Results", width=20, height=2,
                        bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT,
                        command=lambda: open_folder('runs'))
btn_results.grid(row=2, column=1, padx=10, pady=10)

btn_exit = tk.Button(root, text="❌ Exit", width=20, height=1,
                     bg=EXIT_COLOR, fg=BUTTON_TEXT_COLOR, font=FONT,
                     command=root.quit)
btn_exit.grid(row=3, column=0, columnspan=2, pady=(10, 10))

root.mainloop()
