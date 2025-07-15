
# 🚀 Prototype Features

This prototype is a **desktop application** built on YOLOv10 for object detection. It supports **image, video, and live webcam inference** with GPU acceleration (if available).

---

## 🌟 Key Features

### 📷 1. **Image Inference**

* Select an image file through a file explorer dialog (supports `.jpg`, `.png`, `.bmp`, etc.)
* Automatically runs detection and saves annotated results.
* Opens the results folder after inference.

---

### 🎥 2. **Video Inference**

* Select a video file (supports `.mp4`, `.avi`, `.mov`, `.mkv`).
* Processes the video frame-by-frame with YOLOv10.
* Annotated video is saved and the folder is auto-opened.

---

### 📡 3. **Live Webcam Inference**

* Detect objects in real time using your webcam.
* Annotates live feed with detection boxes and labels.
* **Additional Features:**

  * 📝 Records the live session as an `.mp4` video.
  * ⚡ Shows FPS (frames per second) and inference time overlay on the live feed.
  * 🔴 Exit anytime by pressing `Q`.

---

### 💻 4. **GPU Acceleration**

* Automatically detects NVIDIA GPU and runs with CUDA if available.
* Falls back to CPU if no GPU is detected.

---

### 🎨 5. **Graphical User Interface (GUI)**

* Simple and clean GUI using **Tkinter**:

  * Two rows of large buttons for Image, Video, and Live inference.
  * Red “Exit” button for closing the app.
* Avoids console use—ideal for non-technical users.

---

## 📦 Technical Stack

* **Python 3.10**
* **Ultralytics YOLOv10**
* **PyTorch** (CUDA-enabled)
* **OpenCV** (Live feed + video processing)
* **Tkinter** (GUI)

---

## 📁 Output

* Annotated images/videos saved in:

  ```
  runs/detect
  ```
* Each inference creates a timestamped folder.

---

# 📦 YOLOv10 Prototype Setup Guide

## ✅ Before Installation

Make sure you have:

* **Python 3.10 installed**
* Python added to your system’s **environment variables**

---

### 🔥 Verify Python Installation

Open Command Prompt and run:

```bash
py --version
```

or

```bash
python --version
```

You should see:

```
Python 3.10.x
```

---

### ⚡ Check CUDA (Optional for GPU)

If you have an NVIDIA GPU, check your CUDA version:

```bash
nvidia-smi
```

This tells you which CUDA version your GPU supports.

---

## 📥 Installation Instructions

---

### 1️⃣ Clone YOLOv10 Repository

In your project folder, clone Allan’s YOLOv10 fork:

```bash
git clone https://github.com/allansdefreitas/yolov10.git
```

---

### 2️⃣ Create Virtual Environment

Navigate into the `yolov10` folder and create a virtual environment:

```bash
cd yolov10
py -3.10 -m venv venv
```

This creates:

```
yolov10\venv
```

---

### 3️⃣ Activate Virtual Environment

Activate the venv:

```bash
venv\Scripts\activate
```

You should now see:

```
(venv) yolov10>
```

---

### 4️⃣ Install Required Tools

While inside the venv, upgrade pip and install dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install ultralytics
pip install -r requirements.txt
```

---

### 5️⃣ Install PyTorch with GPU Support

Install PyTorch (CUDA 11.8) for GPU acceleration:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

🖤 **If no GPU**, just run:

```bash
pip install torch torchvision torchaudio
```