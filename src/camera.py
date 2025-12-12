"""Camera initialization and frame processing"""

import cv2
from typing import Optional, Tuple
import numpy as np


class Camera:
    def __init__(self, index: int, width: int, height: int, fps: int):
        self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        if not self.cap.isOpened():
            raise RuntimeError("Failed to open camera")
    
    def read_frame(self) -> Tuple[bool, Optional[np.ndarray]]:
        success, frame = self.cap.read()
        if success:
            frame = cv2.flip(frame, 1)
        return success, frame
    
    def release(self):
        self.cap.release()