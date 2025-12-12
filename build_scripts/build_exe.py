"""
PyInstaller build script for AirMouse application
Run this script to build the executable
"""

import PyInstaller.__main__
import os
import sys

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(project_root, 'src')
resources_dir = os.path.join(project_root, 'resources')
icon_path = os.path.join(resources_dir, 'app_icon.ico')

# Verify icon exists
if not os.path.exists(icon_path):
    print(f"ERROR: Icon file not found at {icon_path}")
    print("Please create resources/app_icon.ico before building")
    sys.exit(1)

print("=" * 60)
print("Building AirMouse Desktop Application")
print("=" * 60)

# PyInstaller arguments
args = [
    os.path.join(src_dir, 'main.py'),  # Entry point
    
    # Output configuration
    '--name=AirMouse',                  # Executable name
    '--onefile',                        # Single executable file
    '--windowed',                       # No console window (GUI mode)
    '--clean',                          # Clean build cache
    
    # Icon
    f'--icon={icon_path}',
    
    # Add all Python files from src individually
    f'--add-data={os.path.join(src_dir, "camera.py")};src',
    f'--add-data={os.path.join(src_dir, "hand_tracker.py")};src',
    f'--add-data={os.path.join(src_dir, "gesture_detector.py")};src',
    f'--add-data={os.path.join(src_dir, "mouse_controller.py")};src',
    f'--add-data={os.path.join(src_dir, "config.py")};src',
    f'--add-data={os.path.join(src_dir, "__init__.py")};src',
    
    # Hidden imports (libraries that PyInstaller might miss)
    '--hidden-import=cv2',
    '--hidden-import=mediapipe',
    '--hidden-import=pyautogui',
    '--hidden-import=numpy',
    '--hidden-import=PIL',
    '--hidden-import=pyscreeze',
    '--hidden-import=pytweening',
    '--hidden-import=pymsgbox',
    '--hidden-import=pyperclip',
    
    # MediaPipe specific
    '--hidden-import=mediapipe.python',
    '--hidden-import=mediapipe.python.solutions',
    '--hidden-import=mediapipe.python.solutions.hands',
    '--hidden-import=google.protobuf',
    
    # Collect all MediaPipe data files
    '--collect-all=mediapipe',
    
    # OpenCV data
    '--collect-all=cv2',
    
    # Output directories
    '--distpath=dist',
    '--workpath=build',
    '--specpath=build',
    
    # Runtime options
    '--noupx',                          # Don't use UPX compression (can cause issues)
]

# Run PyInstaller
print("\nStarting build process...")
print(f"Icon: {icon_path}")
print(f"Source: {src_dir}")
print("\nThis may take several minutes...\n")

PyInstaller.__main__.run(args)

print("\n" + "=" * 60)
print("Build complete!")
print("=" * 60)
print(f"\nExecutable location: {os.path.join(project_root, 'dist', 'AirMouse.exe')}")
print("\nNext steps:")
print("1. Test the executable: dist/AirMouse.exe")
print("2. Create installer using Inno Setup (see instructions)")