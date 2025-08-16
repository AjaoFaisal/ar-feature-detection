# 🕹️ AR Feature Detection

This project implements an augmented reality feature detection system using Python and OpenCV. It detects features in a reference image, tracks them in a video or webcam feed, and overlays another video onto the detected area.

---

## 🚀 Features
- Real-time ORB feature detection.
- Video overlay onto detected objects.
- Stacks multiple debug frames for visualization.
- Supports both webcam input and pre-recorded video.
- Robust to partial occlusions using homography and RANSAC.

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/AjaoFaisal/ar-feature-detection.git
cd ar-feature-detection

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

### Main AR Detection
Run:
```
python main.py
```
- Detects features from `cards.png` and overlays `video1.mp4` onto the detected area.
- Use `use_webcam = True` in `main.py` to switch to live webcam input.

---

## 📊 Output Example (Video)
[![Watch the output](https://img.youtube.com/vi/X3BaIABf8zM/hqdefault.jpg)](https://youtu.be/X3BaIABf8zM?feature=shared)

---

## 📂 Project Structure
```
ar-feature-detection/
├── cards.png              # Reference image for AR detection
├── video1.mp4             # Video to overlay
├── webcam_frame.jpg
├── main.py
├── stack.py               # Utility to stack and resize images
├── README.md
└── requirements.txt
```

---

## 🧠 Tech Stack
- Python 3.11.5
- OpenCV
- NumPy

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## Install dependencies
```bash
pip install -r requirements.txt
```
