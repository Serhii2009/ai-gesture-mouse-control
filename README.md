# 🖱️ AI Gesture Mouse Control (Computer Vision) ✌️

> Control your laptop with just your hands — no mouse, no touchpad required.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green.svg)](https://ai.google.dev/edge/mediapipe/solutions/guide)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A real-time computer vision system that transforms hand gestures into precise mouse control. Built with MediaPipe, OpenCV, and PyAutoGUI, this project lets you navigate your laptop naturally — move the cursor, click, double-click, and scroll using intuitive hand movements captured through your webcam.

_Control your laptop like magic or science, depending on how you look at it._

---

## ✨ Features

### 🎯 Cursor Control

Point your **right index finger** at the screen, and the cursor follows your movement with smooth, stabilized tracking. The system maps your hand position to screen coordinates with intelligent smoothing to eliminate jitter.

### 👆 Single & Double Click

Use your **left hand** to click:

- **Quick pinch** (thumb + index finger): Single click
- **Hold pinch for 2 seconds**: Double click

The system intelligently distinguishes between the two based on how long you hold the gesture.

### 📜 Directional Scrolling

Navigate documents and web pages with your **right hand**:

- **Thumb + upper middle finger** (near nail): Scroll up
- **Thumb + middle joint of middle finger**: Scroll down

Scrolling is smooth, responsive, and never jumps or stutters.

### 🧠 Smart Gesture Detection

- **Debouncing**: Prevents accidental repeated clicks
- **Smoothing**: Eliminates cursor jitter for precise control
- **Vote-based filtering**: Ensures stable scroll direction detection
- **Adaptive tracking**: Works reliably at different distances from the camera

---

## 🎬 How It Works

### The Technology Stack

This project combines three powerful libraries to create a seamless gesture control experience:

1. **MediaPipe** (Google's ML solution)

   - Detects and tracks 21 3D landmarks per hand in real-time
   - Runs efficiently on CPU without requiring GPU acceleration
   - Provides accurate hand pose estimation at 30+ FPS

2. **OpenCV** (Computer Vision)

   - Captures and processes webcam video feed
   - Handles frame flipping, color conversion, and visual overlays
   - Displays real-time feedback with landmark visualization

3. **PyAutoGUI** (System Control)
   - Translates detected gestures into actual mouse actions
   - Provides cross-platform compatibility (with Windows 11 optimization)
   - Executes movements and clicks with minimal latency

### The Processing Pipeline

```
Webcam Feed → MediaPipe Hand Tracking → Gesture Recognition → Mouse Control
     ↓              ↓                          ↓                    ↓
  1280x720     21 landmarks per hand    Pattern matching      System actions
  30 FPS       Left + Right hands        Click/Scroll logic   Move/Click/Scroll
```

**Frame-by-frame breakdown:**

1. **Capture**: OpenCV grabs a frame from your webcam and flips it horizontally for mirror-view interaction
2. **Detection**: MediaPipe processes the frame and identifies hands, extracting 21 3D coordinate points for each
3. **Classification**: The system distinguishes left hand (for clicking) from right hand (for cursor/scroll)
4. **Gesture Analysis**:
   - **Right index finger position** → cursor coordinates
   - **Left thumb-index distance** → click detection + hold timer
   - **Right thumb-middle finger contact points** → scroll direction
5. **Smoothing**: Raw coordinates pass through exponential smoothing filters to eliminate jitter
6. **Execution**: PyAutoGUI translates processed gestures into actual mouse movements and actions

### Why These Gestures?

The gesture mappings were chosen for **ergonomics and intuitiveness**:

- **Index finger pointing** is the most natural way humans indicate position
- **Thumb-index pinch** mimics the real-world action of clicking or selecting
- **Thumb-middle finger positions** create distinct, easy-to-maintain scroll gestures
- **Left/right hand separation** prevents conflicts — you can move and click simultaneously

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have:

- **Windows 11** (optimized for this OS, may work on Windows 10)
- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **Built-in webcam** (required for gesture detection)
- **Administrator privileges** (PyAutoGUI requires permission for mouse control)

> **📝 Note**: This project is designed for laptops with integrated webcams. While it can work with external USB webcams on desktop systems, performance and tracking accuracy are optimized for typical laptop camera positioning and viewing angles.

### Step 1: Clone the Repository

```bash
git clone https://github.com/Serhii2009/ai-gesture-mouse-control
cd ai-gesture-mouse-control
```

### Step 2: Create a Virtual Environment

Creating a virtual environment keeps dependencies isolated and prevents conflicts:

```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment

```bash
# Windows Command Prompt
venv\Scripts\activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# If you get a PowerShell execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

You should see `(venv)` appear at the beginning of your command prompt.

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs:

- **mediapipe 0.10.9** - Hand tracking AI
- **opencv-python 4.8.1.78** - Video processing
- **pyautogui 0.9.54** - Mouse control
- **numpy 1.24.3** - Mathematical operations

_Installation typically takes 2-3 minutes depending on your internet connection._

### Step 5: Verify Installation

```bash
python -c "import cv2, mediapipe, pyautogui; print('All dependencies installed successfully!')"
```

If you see the success message, you're ready to go!

---

## 🎮 Usage

### Starting the Application

Navigate to the source directory and run the main script:

```bash
cd src
python main.py
```

A window will open showing your webcam feed with hand tracking overlays.

### Gesture Reference Guide

#### 🖱️ **Moving the Cursor**

- **Gesture**: Point your **right index finger** toward the camera
- **Action**: The cursor follows your fingertip position
- **Tips**:
  - Keep your hand within the camera frame
  - Move smoothly for best tracking
  - Hold your hand 1-2 feet from the webcam for optimal detection

#### 🖱️ **Single Click**

- **Gesture**: Quickly pinch your **left thumb and index finger** together, then release
- **Action**: Performs a left mouse click
- **Tips**:
  - Make a clear pinching motion
  - Release immediately after touching
  - You'll see "SINGLE CLICK!" on screen

#### 🖱️ **Double Click**

- **Gesture**: Pinch your **left thumb and index finger** together and **hold for 2 seconds**, then release
- **Action**: Performs a double-click
- **Tips**:
  - Keep fingers touching while you count to two
  - Release after the hold period
  - You'll see "DOUBLE CLICK!" on screen

#### 📜 **Scroll Up**

- **Gesture**: Touch your **right thumb** to the **upper part of your right middle finger** (near the nail)
- **Action**: Scrolls up continuously while held
- **Tips**:
  - Hold the gesture steady for smooth scrolling
  - Release to stop scrolling
  - You'll see "SCROLL UP" in yellow

#### 📜 **Scroll Down**

- **Gesture**: Touch your **right thumb** to the **middle joint of your right middle finger**
- **Action**: Scrolls down continuously while held
- **Tips**:
  - Find the middle knuckle of your middle finger
  - Hold steady for best results
  - You'll see "SCROLL DOWN" in orange

#### 🛑 **Exit Application**

- **Action**: Press the **'q'** key while the video window is focused

### Visual Feedback

The application provides real-time visual feedback:

- **Green skeleton overlay**: Shows detected hand landmarks
- **FPS counter** (top-left): Displays current frame rate
- **Action indicators**: Large text confirms clicks and scrolls
- **Color coding**:
  - Green = Clicks
  - Yellow = Scroll up
  - Orange = Scroll down

---

## ⚙️ Configuration

All settings can be customized in `src/config.py`. Here are the most commonly adjusted parameters:

### Camera Settings

```python
CAMERA_INDEX = 0              # Change to 1 or 2 if default camera doesn't work
CAMERA_WIDTH = 1280           # Lower to 640 for better performance on slower machines
CAMERA_HEIGHT = 720           # Lower to 480 for better performance
CAMERA_FPS = 30               # Frame rate target
```

### Tracking Confidence

```python
MIN_DETECTION_CONFIDENCE = 0.7    # Lower = easier to detect hands (0.5-0.9)
MIN_TRACKING_CONFIDENCE = 0.7     # Lower = more stable but less accurate (0.5-0.9)
```

### Mouse Control

```python
SMOOTHING_FACTOR = 0.5            # Higher = smoother but slower (0.1-1.0)
MOUSE_SPEED_MULTIPLIER = 1.5      # Higher = faster cursor movement (0.5-3.0)
```

### Click Sensitivity

```python
PINCH_THRESHOLD = 40.0            # Lower = easier to trigger clicks (30-50)
DOUBLE_CLICK_HOLD_TIME = 2.0      # Seconds to hold for double-click (1.5-3.0)
```

### Scroll Settings

```python
SCROLL_SPEED = 15                 # Higher = faster scrolling (5-30)
SCROLL_UP_THRESHOLD = 45.0        # Distance threshold for scroll up (35-55)
SCROLL_DOWN_THRESHOLD = 45.0      # Distance threshold for scroll down (35-55)
```

---

## 🏗️ Project Structure

```
ai-cv-gesture-mouse-control/
│
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point and main loop
│   ├── camera.py                # Webcam initialization and frame capture
│   ├── hand_tracker.py          # MediaPipe hand tracking wrapper
│   ├── gesture_detector.py      # Gesture recognition algorithms
│   ├── mouse_controller.py      # PyAutoGUI mouse control interface
│   └── config.py                # Centralized configuration settings
│
├── requirements.txt             # Python package dependencies
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── LICENSE                      # MIT License
```

### Module Descriptions

- **`main.py`**: Orchestrates the application flow, manages the processing loop, and handles user interface
- **`camera.py`**: Abstracts webcam operations with optimized settings for Windows 11
- **`hand_tracker.py`**: Wraps MediaPipe's hand tracking API with helper methods for landmark extraction
- **`gesture_detector.py`**: Implements gesture recognition logic with smoothing and debouncing
- **`mouse_controller.py`**: Provides a clean interface to PyAutoGUI with coordinate mapping and smoothing
- **`config.py`**: Centralizes all tunable parameters for easy customization

---

## 🔧 Troubleshooting

### Camera Issues

**Problem**: "Failed to open camera" error

**Solutions**:

- Check if another application is using the webcam (Zoom, Teams, Skype)
- Try different camera indices in `config.py`: `CAMERA_INDEX = 1` or `2`
- Ensure camera permissions are enabled in Windows Settings → Privacy → Camera
- Restart your laptop to release camera locks

**Problem**: Camera lag or low FPS

**Solutions**:

- Lower resolution: Set `CAMERA_WIDTH = 640` and `CAMERA_HEIGHT = 480`
- Reduce frame rate: Set `CAMERA_FPS = 20`
- Close other applications using CPU/camera
- Ensure good lighting — poor lighting forces longer exposure times

### Tracking Issues

**Problem**: Hands not being detected

**Solutions**:

- Ensure adequate lighting — MediaPipe needs clear hand visibility
- Keep hands 1-2 feet from camera, fully visible
- Lower detection confidence: `MIN_DETECTION_CONFIDENCE = 0.5`
- Ensure your hands are in frame and not too far away
- Avoid wearing gloves or having objects covering your hands

**Problem**: Cursor movement is jittery or erratic

**Solutions**:

- Increase smoothing: `SMOOTHING_FACTOR = 0.7` or `0.8`
- Increase tracking confidence: `MIN_TRACKING_CONFIDENCE = 0.8`
- Stabilize your hand position
- Improve lighting conditions

### Gesture Recognition Issues

**Problem**: Clicks not registering

**Solutions**:

- Increase threshold: `PINCH_THRESHOLD = 50` or `60`
- Ensure you're using the left hand (right hand is for cursor)
- Make a clear, deliberate pinching motion
- Check that both thumb and index finger are visible

**Problem**: Too many accidental clicks

**Solutions**:

- Decrease threshold: `PINCH_THRESHOLD = 30` or `35`
- Keep your left hand relaxed when not clicking
- Increase hold frames: `PINCH_HOLD_FRAMES = 3`

**Problem**: Scrolling not working or wrong direction

**Solutions**:

- Ensure you're touching the correct part of the middle finger
- Increase thresholds: `SCROLL_UP_THRESHOLD = 55`, `SCROLL_DOWN_THRESHOLD = 55`
- Hold the gesture steady for 1-2 seconds to let the voting system stabilize
- Check that your entire right hand is visible in the frame

**Problem**: Scrolling is too fast or too slow

**Solutions**:

- Adjust speed: `SCROLL_SPEED = 20` (faster) or `10` (slower)
- For very precise scrolling: `SCROLL_SPEED = 5`
- For rapid scrolling: `SCROLL_SPEED = 30`

### Performance Issues

**Problem**: High CPU usage

**Solutions**:

- Lower camera resolution and FPS (see Camera Issues above)
- Close other CPU-intensive applications
- Disable landmark visualization: `SHOW_LANDMARKS = False`
- Disable FPS display: `SHOW_FPS = False`

**Problem**: PyAutoGUI permission errors

**Solutions**:

- Run Command Prompt or PowerShell as Administrator
- Check Windows Defender settings — some security software blocks automated mouse control
- Add Python to your antivirus exceptions

---

## 🎯 Use Cases

This project is perfect for:

- **Accessibility**: Assisting users with limited mobility or hand injuries
- **Presentation control**: Navigate slides hands-free during presentations
- **Smart home demos**: Showcasing gesture-based interaction concepts
- **Educational projects**: Learning computer vision, ML, and human-computer interaction
- **Prototyping**: Building gesture-controlled applications or testing UI concepts
- **Fun experiments**: Impressing friends and exploring the future of human-computer interaction

---

## 🧪 Technical Deep Dive

### Hand Landmark Detection

MediaPipe identifies 21 key points on each hand:

```
        8   12  16  20    (Fingertips: Index, Middle, Ring, Pinky)
        |   |   |   |
        7   11  15  19
        |   |   |   |
    4   6   10  14  18
    |   |   |   |   |
    3   5   9   13  17
    |       |       |
    2       0-------1      (0 = Wrist, 1-4 = Thumb)
```

**Key landmarks used**:

- **4**: Thumb tip (clicking, scrolling)
- **8**: Index finger tip (cursor position)
- **10**: Middle finger middle joint (scroll down trigger)
- **11**: Middle finger upper joint (scroll up trigger)
- **12**: Middle finger tip (scroll tracking)

### Coordinate Transformation

Raw MediaPipe coordinates are normalized (0.0-1.0). The system transforms them through multiple stages:

1. **Denormalization**: Multiply by frame dimensions to get pixel coordinates
2. **Screen mapping**: Map pixel coordinates to screen resolution with padding
3. **Smoothing**: Apply exponential moving average to reduce jitter
4. **Speed adjustment**: Multiply by speed factor for responsive control

### Gesture Recognition Algorithms

**Pinch Detection**:

```
distance = sqrt((thumb_x - index_x)² + (thumb_y - index_y)²)
if distance < threshold and hold_time ≥ 2s:
    return "double_click"
elif distance < threshold:
    return "single_click"
```

**Scroll Detection** (vote-based):

```
buffer = [direction₁, direction₂, direction₃, direction₄, direction₅]
if count(buffer, "up") ≥ 3:
    return "scroll_up"
elif count(buffer, "down") ≥ 3:
    return "scroll_down"
```

This voting mechanism ensures stable detection by requiring consensus across multiple frames.

---

## 🤝 Contributing

Contributions are welcome! Whether you're fixing bugs, adding features, or improving documentation, your help makes this project better.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add some AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Ideas for Contribution

- Add drag-and-drop functionality
- Create custom gesture profiles
- Improve gesture recognition accuracy
- Add gesture recording and playback
- Implement multi-monitor support
- Create a settings GUI
- Optimize for external webcams and desktop setups

---

## 📊 Performance Benchmarks

Tested on a mid-range laptop (Intel i5-10th gen, 8GB RAM, integrated graphics, built-in webcam):

| Metric                     | Value     |
| -------------------------- | --------- |
| Average FPS                | 28-32     |
| CPU Usage                  | 15-25%    |
| RAM Usage                  | ~200 MB   |
| Latency (gesture → action) | 50-100ms  |
| Cursor tracking accuracy   | ±5 pixels |

The system runs efficiently without GPU acceleration, making it accessible on most modern laptops.

---

## 📜 License

This project is licensed under the **MIT License** — you're free to use, modify, and distribute this software. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google MediaPipe Team** for their incredible hand tracking ML model
- **OpenCV Community** for robust computer vision tools
- **PyAutoGUI Developers** for making system automation accessible
- **You** for checking out this project — we hope it inspires your next creation!

---

## 📬 Contact

Want to share what you built?

- **LinkedIn**: [My LinkedIn Profile](https://www.linkedin.com/in/serhii-kravchenko-b941272a6)

If this project helped you, consider giving it a ⭐ on GitHub — it helps others discover it too!

---

<div align="center">

**Built with 🤖 MediaPipe, 👁️ OpenCV, and 🖱️ PyAutoGUI**

_Control the future with your hands._

</div>
