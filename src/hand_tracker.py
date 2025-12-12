"""Hand tracking using MediaPipe"""

import mediapipe as mp
import cv2
from typing import Optional, List, Dict
import numpy as np


class HandTracker:
    def __init__(self, max_hands: int, min_detection_confidence: float, min_tracking_confidence: float):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
    
    def process_frame(self, frame: np.ndarray) -> Optional[object]:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb_frame)
    
    def extract_hands_data(self, results: object, frame_shape: tuple) -> Dict[str, List]:
        hands_data = {'Left': [], 'Right': []}
        
        if not results.multi_hand_landmarks:
            return hands_data
        
        h, w, _ = frame_shape
        
        for hand_landmarks, hand_info in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = hand_info.classification[0].label
            landmarks = []
            
            for lm in hand_landmarks.landmark:
                landmarks.append({
                    'x': lm.x * w,
                    'y': lm.y * h,
                    'z': lm.z
                })
            
            hands_data[label] = landmarks
        
        return hands_data
    
    def draw_landmarks(self, frame: np.ndarray, results: object):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
    
    def close(self):
        self.hands.close()