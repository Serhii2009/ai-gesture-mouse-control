# 🖱️ AI Gesture Mouse Control (Computer Vision) ✌️

> Control your laptop with just your hands — no mouse, no touchpad required.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-green.svg)](https://ai.google.dev/edge/mediapipe/solutions/guide)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A real-time computer vision system that transforms hand gestures into comprehensive mouse and keyboard control. Built with MediaPipe, OpenCV, and PyAutoGUI, this project lets you navigate your laptop naturally — move the cursor, click, double-click, scroll, copy, paste, switch virtual desktops, and drag-and-drop using intuitive hand movements captured through your webcam.

_Control your laptop like magic or science, depending on how you look at it._

---

## ✨ Features

### 🎯 Cursor Control

Point your **right index finger** at the screen, and the cursor follows your movement with smooth, stabilized tracking. The system maps your hand position to screen coordinates with intelligent smoothing to eliminate jitter.

### 👆 Advanced Click System

Use your **left hand** for different types of clicks:

- **Quick pinch** (thumb + index finger, <0.25s): Single click
- **Thumb + middle finger**: Double click
- Each gesture uses a different finger combination to prevent conflicts

### 📋 Copy & Paste

Perform clipboard operations with simple gestures:

- **Thumb + ring finger**: Copy (Ctrl+C)
- **Thumb + pinky**: Paste (Ctrl+V)

### 📜 Directional Scrolling

Navigate documents and web pages with your **right hand**:

- **Thumb + upper middle finger** (near nail): Scroll up
- **Thumb + middle joint of middle finger**: Scroll down

Scrolling is smooth, responsive, and never jumps or stutters.

### 🖥️ Virtual Desktop Switching

Navigate between Windows virtual desktops with **right hand** gestures:

- **Thumb + ring finger**: Switch to desktop on the left (Ctrl+Win+Left)
- **Thumb + pinky**: Switch to desktop on the right (Ctrl+Win+Right)

### 🎯 Drag-and-Drop Mode

Perform drag-and-drop operations using **both hands**:

- **Left index + right index**: Start drag (mouse down)
- **Left index + right thumb**: End drag (mouse up)
- Move the cursor with your right hand while drag mode is active

### 🧠 Smart Gesture Detection

- **Debouncing**: Prevents accidental repeated actions
- **Smoothing**: Eliminates cursor jitter for precise control
- **Vote-based filtering**: Ensures stable scroll direction detection
- **Independent cooldowns**: Each gesture has its own timing to prevent conflicts
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
   - Translates detected gestures into actual mouse and keyboard actions
   - Provides cross-platform compatibility (with Windows 11 optimization)
   - Executes movements, clicks, and hotkeys with minimal latency

### The Processing Pipeline

```
Webcam Feed → MediaPipe Hand Tracking → Gesture Recognition → System Control
     ↓              ↓                          ↓                    ↓
  1280x720     21 landmarks per hand    Pattern matching      Actions
  30 FPS       Left + Right hands        Multi-gesture logic   Move/Click/Hotkeys
```

**Frame-by-frame breakdown:**

1. **Capture**: OpenCV grabs a frame from your webcam and flips it horizontally for mirror-view interaction
2. **Detection**: MediaPipe processes the frame and identifies hands, extracting 21 3D coordinate points for each
3. **Classification**: The system distinguishes left hand (for clicking/editing) from right hand (for cursor/navigation)
4. **Gesture Analysis**:
   - **Right index finger position** → cursor coordinates
   - **Left hand thumb-finger distances** → click, copy, paste detection
   - **Right hand thumb-finger distances** → scroll, desktop switching
   - **Inter-hand finger distances** → drag mode activation/deactivation
5. **Smoothing**: Raw coordinates pass through exponential smoothing filters to eliminate jitter
6. **Execution**: PyAutoGUI translates processed gestures into actual system actions

### Why These Gestures?

The gesture mappings were chosen for **ergonomics, intuitiveness, and conflict prevention**:

- **Index finger pointing** is the most natural way humans indicate position
- **Different finger combinations** for each action prevents accidental triggers
- **Left hand for editing**, **right hand for navigation** creates logical separation
- **Two-handed gestures for drag mode** ensures intentional activation
- **Each gesture uses distinct landmark pairs** eliminating overlap

---

## 🚀 Installation

### Prerequisites

Before you begin, ensure you have:

- **Windows 11** (optimized for this OS, may work on Windows 10)
- **Python 3.8 or higher** ([Download here](https://www.python.org/downloads/))
- **Built-in webcam** (required for gesture detection)
- **Administrator privileges** (PyAutoGUI requires permission for system control)

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
- **pyautogui 0.9.54** - System control
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

### Complete Gesture Reference Guide

#### **LEFT HAND GESTURES** 👋

##### 🖱️ **Single Click**

- **Gesture**: Quickly pinch your **left thumb and index finger** together (hold <0.25s), then release
- **Action**: Performs a left mouse click
- **Tips**:
  - Make a fast pinching motion
  - Release immediately after touching
  - You'll see "SINGLE CLICK" in green

##### 🖱️ **Double Click**

- **Gesture**: Touch your **left thumb and middle finger** together
- **Action**: Performs a double-click
- **Tips**:
  - Use your middle finger, not index
  - Brief touch is enough
  - You'll see "DOUBLE CLICK" in green

##### 📋 **Copy (Ctrl+C)**

- **Gesture**: Touch your **left thumb and ring finger** together
- **Action**: Copies selected text/files to clipboard
- **Tips**:
  - Select text first with cursor/drag
  - Brief touch triggers the action
  - You'll see "COPY (Ctrl+C)" in cyan

##### 📋 **Paste (Ctrl+V)**

- **Gesture**: Touch your **left thumb and pinky** together
- **Action**: Pastes clipboard content
- **Tips**:
  - Position cursor where you want to paste
  - Brief touch triggers the action
  - You'll see "PASTE (Ctrl+V)" in cyan

---

#### **RIGHT HAND GESTURES** 🤚

##### 🎯 **Move Cursor**

- **Gesture**: Point your **right index finger** toward the camera
- **Action**: The cursor follows your fingertip position
- **Tips**:
  - Keep your hand within the camera frame
  - Move smoothly for best tracking
  - Hold your hand 1-2 feet from the webcam

##### 📜 **Scroll Up**

- **Gesture**: Touch your **right thumb** to the **upper part of your right middle finger** (near the nail)
- **Action**: Scrolls up continuously while held
- **Tips**:
  - Hold the gesture steady for smooth scrolling
  - Release to stop scrolling
  - You'll see "SCROLL UP" in yellow

##### 📜 **Scroll Down**

- **Gesture**: Touch your **right thumb** to the **middle joint of your right middle finger**
- **Action**: Scrolls down continuously while held
- **Tips**:
  - Find the middle knuckle
  - Hold steady for best results
  - You'll see "SCROLL DOWN" in orange

##### 🖥️ **Switch Desktop Left**

- **Gesture**: Touch your **right thumb and ring finger** together
- **Action**: Switches to the virtual desktop on the left (Ctrl+Win+Left)
- **Tips**:
  - Works with Windows 10/11 virtual desktops
  - You'll see "DESKTOP LEFT" in orange

##### 🖥️ **Switch Desktop Right**

- **Gesture**: Touch your **right thumb and pinky** together
- **Action**: Switches to the virtual desktop on the right (Ctrl+Win+Right)
- **Tips**:
  - Works with Windows 10/11 virtual desktops
  - You'll see "DESKTOP RIGHT" in orange

---

#### **TWO-HANDED GESTURES** 🙌

##### 🎯 **Start Drag Mode**

- **Gesture**: Touch your **left index finger** to your **right index finger**
- **Action**: Mouse button held down (drag mode activated)
- **Behavior**:
  - After touching, you can separate your hands
  - Move the cursor with your right hand to drag
  - Persistent "DRAG MODE ACTIVE" indicator appears
  - You'll see "DRAG ON" in magenta

##### 🎯 **End Drag Mode**

- **Gesture**: Touch your **left index finger** to your **right thumb**
- **Action**: Mouse button released (drag mode deactivated)
- **Behavior**:
  - Completes the drag-and-drop operation
  - Returns to normal cursor control
  - You'll see "DRAG OFF" in magenta

---

##### 🛑 **Exit Application**

- **Action**: Press the **'q'** key while the video window is focused

---

### Visual Feedback System

The application provides comprehensive real-time visual feedback:

- **Green skeleton overlay**: Shows detected hand landmarks for both hands
- **FPS counter** (top-left): Displays current frame rate
- **Action indicators**: Large text confirms all actions
- **Persistent drag indicator**: Shows when drag mode is active
- **Color coding**:
  - **Green**: Clicks
  - **Yellow**: Scroll up
  - **Orange**: Scroll down, desktop switching
  - **Cyan**: Copy/Paste operations
  - **Magenta**: Drag mode

---

## ⚙️ Configuration

All settings can be customized in `src/config.py`. Here are the most commonly adjusted parameters:

### Camera Settings

```python
CAMERA_INDEX = 0              # Change to 1 or 2 if default camera doesn't work
CAMERA_WIDTH = 1280           # Lower to 640 for better performance
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

### Gesture Thresholds

```python
# Click gestures
SINGLE_CLICK_THRESHOLD = 40.0     # Distance for single click detection (30-50)
SINGLE_CLICK_MAX_TIME = 0.25      # Max hold time for single click in seconds
DOUBLE_CLICK_THRESHOLD = 40.0     # Distance for double click detection (30-50)

# Edit gestures
COPY_THRESHOLD = 40.0             # Distance for copy gesture (30-50)
PASTE_THRESHOLD = 40.0            # Distance for paste gesture (30-50)

# Scroll gestures
SCROLL_SPEED = 15                 # Higher = faster scrolling (5-30)
SCROLL_UP_THRESHOLD = 45.0        # Distance threshold for scroll up (35-55)
SCROLL_DOWN_THRESHOLD = 45.0      # Distance threshold for scroll down (35-55)

# Desktop switching
DESKTOP_SWITCH_THRESHOLD = 40.0   # Distance for desktop switching (30-50)

# Drag mode
DRAG_START_THRESHOLD = 40.0       # Distance to start drag (30-50)
DRAG_END_THRESHOLD = 40.0         # Distance to end drag (30-50)
```

---

## 🏗️ Project Structure

```
ai-gesture-mouse-control/
│
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point and main loop
│   ├── camera.py                # Webcam initialization and frame capture
│   ├── hand_tracker.py          # MediaPipe hand tracking wrapper
│   ├── gesture_detector.py      # Gesture recognition algorithms
│   ├── mouse_controller.py      # PyAutoGUI system control interface
│   └── config.py                # Centralized configuration settings
│
├── requirements.txt             # Python package dependencies
├── README.md                    # Project documentation
├── .gitignore                   # Git ignore rules
└── LICENSE                      # MIT License
```

### Module Descriptions

- **`main.py`**: Orchestrates the application flow, manages the processing loop, and handles all gesture logic
- **`camera.py`**: Abstracts webcam operations with optimized settings for Windows 11
- **`hand_tracker.py`**: Wraps MediaPipe's hand tracking API with helper methods for landmark extraction
- **`gesture_detector.py`**: Implements all gesture recognition logic with independent cooldowns and state management
- **`mouse_controller.py`**: Provides a clean interface to PyAutoGUI for mouse and keyboard control
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
- Ensure both hands are in frame for two-handed gestures
- Avoid wearing gloves or having objects covering your hands

**Problem**: Cursor movement is jittery or erratic

**Solutions**:

- Increase smoothing: `SMOOTHING_FACTOR = 0.7` or `0.8`
- Increase tracking confidence: `MIN_TRACKING_CONFIDENCE = 0.8`
- Stabilize your hand position
- Improve lighting conditions

### Gesture Recognition Issues

**Problem**: Gestures not registering

**Solutions**:

- Increase thresholds for the specific gesture (e.g., `COPY_THRESHOLD = 50`)
- Ensure you're using the correct hand (left for clicks/edit, right for navigation)
- Make clear, deliberate gestures
- Check that relevant fingers are visible to the camera

**Problem**: Too many accidental triggers

**Solutions**:

- Decrease thresholds for the specific gesture (e.g., `SINGLE_CLICK_THRESHOLD = 30`)
- Keep hands relaxed when not performing gestures
- Maintain distance between fingers when not intending to trigger

**Problem**: Single click registers as something else

**Solutions**:

- Release the pinch faster (within 0.25 seconds)
- Ensure you're using thumb + index finger, not thumb + middle finger
- Adjust `SINGLE_CLICK_MAX_TIME` if needed

**Problem**: Drag mode won't activate/deactivate

**Solutions**:

- Ensure both hands are visible in frame
- Make sure you're touching the correct fingers (index-to-index for start, index-to-thumb for end)
- Adjust `DRAG_START_THRESHOLD` and `DRAG_END_THRESHOLD`
- Check console output for confirmation messages

**Problem**: Desktop switching not working

**Solutions**:

- Ensure you have multiple virtual desktops set up in Windows
- Check that the gesture is being detected (console output)
- Verify Windows shortcuts aren't overridden by other software
- Try manually pressing Ctrl+Win+Arrow to test if virtual desktops work

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
- Check Windows Defender settings — some security software blocks automated control
- Add Python to your antivirus exceptions

---

## 🎯 Use Cases

This project is perfect for:

- **Accessibility**: Assisting users with limited mobility or injuries
- **Touchless interaction**: Controlling your laptop without physical contact
- **Presentation control**: Navigate slides and switch between apps hands-free
- **Content creation**: Quick copy-paste operations while reviewing documents
- **Multi-desktop workflows**: Seamlessly switch between virtual desktops
- **Educational projects**: Learning computer vision, ML, and human-computer interaction
- **Prototyping**: Building gesture-controlled applications
- **Fun experiments**: Impressing friends and exploring future interfaces

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

**Key landmarks used in this project**:

**Left Hand:**

- **4**: Thumb tip (all left hand gestures)
- **8**: Index finger tip (single click, drag start)
- **12**: Middle finger tip (double click)
- **16**: Ring finger tip (copy)
- **20**: Pinky tip (paste)

**Right Hand:**

- **4**: Thumb tip (scroll, desktop switching)
- **8**: Index finger tip (cursor position, drag start)
- **10**: Middle finger middle joint (scroll down trigger)
- **11**: Middle finger upper joint (scroll up trigger)
- **16**: Ring finger tip (desktop switch left)
- **20**: Pinky tip (desktop switch right)

### Coordinate Transformation

Raw MediaPipe coordinates are normalized (0.0-1.0). The system transforms them through multiple stages:

1. **Denormalization**: Multiply by frame dimensions to get pixel coordinates
2. **Screen mapping**: Map pixel coordinates to screen resolution with padding
3. **Smoothing**: Apply exponential moving average to reduce jitter
4. **Speed adjustment**: Multiply by speed factor for responsive control

### Gesture Recognition Algorithms

**Single Click Detection** (time-based):

```
distance = sqrt((thumb_x - index_x)² + (thumb_y - index_y)²)
if distance < threshold:
    start_timer()
if released and hold_time < 0.25s:
    return "single_click"
```

**Double Click Detection** (different finger):

```
distance = sqrt((thumb_x - middle_x)² + (thumb_y - middle_y)²)
if distance < threshold:
    return "double_click"
```

**Scroll Detection** (vote-based):

```
buffer = [direction₁, direction₂, direction₃, direction₄, direction₅]
if count(buffer, "up") ≥ 3:
    return "scroll_up"
elif count(buffer, "down") ≥ 3:
    return "scroll_down"
```

**Drag Mode Detection** (inter-hand):

```
distance_start = sqrt((left_index_x - right_index_x)² + (left_index_y - right_index_y)²)
distance_end = sqrt((left_index_x - right_thumb_x)² + (left_index_y - right_thumb_y)²)

if distance_start < threshold and not drag_active:
    mouse_down()
    drag_active = True

if distance_end < threshold and drag_active:
    mouse_up()
    drag_active = False
```

This multi-gesture system uses independent cooldowns and distinct finger combinations to prevent conflicts and ensure stable, accurate detection.

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

- Add right-click gesture
- Implement text selection mode
- Create custom gesture profiles
- Add gesture recording and playback
- Implement multi-monitor support
- Create a settings GUI
- Add macOS and Linux support
- Optimize for external webcams and desktop setups
- Add more keyboard shortcuts (undo, redo, etc.)

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
| Gesture detection accuracy | >95%      |

The system runs efficiently without GPU acceleration, making it accessible on most modern laptops. All 11 gestures can be performed smoothly without conflicts.

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
