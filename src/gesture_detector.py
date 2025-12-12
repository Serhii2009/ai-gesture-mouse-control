"""Gesture detection logic"""

import numpy as np
import time
from typing import List, Dict, Optional, Tuple
from collections import deque


class GestureDetector:
    def __init__(self, pinch_threshold: float, hold_frames: int, double_click_time: float):
        self.pinch_threshold = pinch_threshold
        self.hold_frames = hold_frames
        self.double_click_time = double_click_time
        
        # Left hand pinch state
        self.pinch_counter = 0
        self.was_pinching = False
        self.pinch_start_time = None
        self.click_cooldown = 0
        
        # Right hand scroll state
        self.scroll_direction = None
        self.scroll_buffer = deque(maxlen=5)
    
    def get_fingertip_position(self, landmarks: List[Dict], finger_index: int) -> Optional[Tuple[float, float]]:
        if not landmarks or len(landmarks) <= finger_index:
            return None
        tip = landmarks[finger_index]
        return (tip['x'], tip['y'])
    
    def get_landmark_position(self, landmarks: List[Dict], index: int) -> Optional[Tuple[float, float]]:
        if not landmarks or len(landmarks) <= index:
            return None
        point = landmarks[index]
        return (point['x'], point['y'])
    
    def calculate_distance_2d(self, landmarks: List[Dict], index1: int, index2: int) -> float:
        if not landmarks or len(landmarks) <= max(index1, index2):
            return float('inf')
        
        p1 = landmarks[index1]
        p2 = landmarks[index2]
        
        dx = p1['x'] - p2['x']
        dy = p1['y'] - p2['y']
        
        return np.sqrt(dx**2 + dy**2)
    
    def detect_pinch_click(self, landmarks: List[Dict]) -> Optional[str]:
        if self.click_cooldown > 0:
            self.click_cooldown -= 1
            return None
        
        distance = self.calculate_distance_2d(landmarks, 4, 8)
        current_time = time.time()
        
        # Check if currently pinching
        if distance < self.pinch_threshold:
            self.pinch_counter += 1
            
            # Start timer on first detection
            if self.pinch_start_time is None and self.pinch_counter >= self.hold_frames:
                self.pinch_start_time = current_time
        else:
            # Released pinch
            if self.was_pinching and self.pinch_start_time is not None:
                hold_duration = current_time - self.pinch_start_time
                
                # Determine click type based on hold duration
                if hold_duration >= self.double_click_time:
                    click_type = "double"
                else:
                    click_type = "single"
                
                # Reset state
                self.pinch_counter = 0
                self.was_pinching = False
                self.pinch_start_time = None
                self.click_cooldown = 15
                
                return click_type
            
            # Reset if not pinching
            self.pinch_counter = 0
            self.was_pinching = False
            self.pinch_start_time = None
        
        # Update pinching state
        is_pinching = self.pinch_counter >= self.hold_frames
        if is_pinching:
            self.was_pinching = True
        
        return None
    
    def detect_scroll_gesture(self, landmarks: List[Dict], up_threshold: float, down_threshold: float) -> Optional[str]:
        """
        Detects scroll gesture based on thumb position relative to middle finger
        Returns: 'up', 'down', or None
        """
        # Thumb tip (4)
        # Middle finger upper phalanx (11) - closer to tip
        # Middle finger middle phalanx (10) - middle joint
        
        # Calculate distance from thumb to upper phalanx (near nail)
        dist_to_upper = self.calculate_distance_2d(landmarks, 4, 11)
        
        # Calculate distance from thumb to middle phalanx (middle joint)
        dist_to_middle = self.calculate_distance_2d(landmarks, 4, 10)
        
        current_direction = None
        
        # Check if thumb is touching upper phalanx (scroll up)
        if dist_to_upper < up_threshold:
            current_direction = "up"
        # Check if thumb is touching middle phalanx (scroll down)
        elif dist_to_middle < down_threshold:
            current_direction = "down"
        
        # Add to buffer for smoothing
        self.scroll_buffer.append(current_direction)
        
        # Determine most common direction in buffer (vote-based smoothing)
        if len(self.scroll_buffer) >= 3:
            directions = [d for d in self.scroll_buffer if d is not None]
            if len(directions) >= 3:
                # Count occurrences
                up_count = directions.count("up")
                down_count = directions.count("down")
                
                # Return direction with most votes
                if up_count > down_count and up_count >= 3:
                    self.scroll_direction = "up"
                    return "up"
                elif down_count > up_count and down_count >= 3:
                    self.scroll_direction = "down"
                    return "down"
        
        # If no clear direction, clear buffer and return None
        if current_direction is None:
            self.scroll_buffer.clear()
            self.scroll_direction = None
        
        return self.scroll_direction