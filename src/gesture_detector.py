"""Gesture detection logic"""

import numpy as np
import time
from typing import List, Dict, Optional, Tuple
from collections import deque


class GestureDetector:
    def __init__(self):
        # Left hand single click state
        self.single_click_start_time = None
        self.single_click_cooldown = 0
        
        # Left hand double click state
        self.double_click_cooldown = 0
        
        # Left hand copy state
        self.copy_cooldown = 0
        
        # Left hand paste state
        self.paste_cooldown = 0
        
        # Right hand scroll state
        self.scroll_direction = None
        self.scroll_buffer = deque(maxlen=5)
        
        # Right hand desktop switching state
        self.desktop_switch_left_cooldown = 0
        self.desktop_switch_right_cooldown = 0
        
        # Drag mode state
        self.drag_active = False
        self.drag_start_cooldown = 0
        self.drag_end_cooldown = 0
    
    def get_fingertip_position(self, landmarks: List[Dict], finger_index: int) -> Optional[Tuple[float, float]]:
        if not landmarks or len(landmarks) <= finger_index:
            return None
        tip = landmarks[finger_index]
        return (tip['x'], tip['y'])
    
    def calculate_distance_2d(self, landmarks: List[Dict], index1: int, index2: int) -> float:
        if not landmarks or len(landmarks) <= max(index1, index2):
            return float('inf')
        
        p1 = landmarks[index1]
        p2 = landmarks[index2]
        
        dx = p1['x'] - p2['x']
        dy = p1['y'] - p2['y']
        
        return np.sqrt(dx**2 + dy**2)
    
    def calculate_distance_between_hands(self, left_landmarks: List[Dict], right_landmarks: List[Dict], 
                                         left_index: int, right_index: int) -> float:
        if not left_landmarks or not right_landmarks:
            return float('inf')
        if len(left_landmarks) <= left_index or len(right_landmarks) <= right_index:
            return float('inf')
        
        p1 = left_landmarks[left_index]
        p2 = right_landmarks[right_index]
        
        dx = p1['x'] - p2['x']
        dy = p1['y'] - p2['y']
        
        return np.sqrt(dx**2 + dy**2)
    
    def detect_single_click(self, landmarks: List[Dict], threshold: float, max_time: float) -> bool:
        if self.single_click_cooldown > 0:
            self.single_click_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 8)
        current_time = time.time()
        
        if distance < threshold:
            if self.single_click_start_time is None:
                self.single_click_start_time = current_time
        else:
            if self.single_click_start_time is not None:
                hold_duration = current_time - self.single_click_start_time
                self.single_click_start_time = None
                
                if hold_duration < max_time:
                    self.single_click_cooldown = 15
                    return True
            
            self.single_click_start_time = None
        
        return False
    
    def detect_double_click(self, landmarks: List[Dict], threshold: float) -> bool:
        if self.double_click_cooldown > 0:
            self.double_click_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 12)
        
        if distance < threshold:
            self.double_click_cooldown = 20
            return True
        
        return False
    
    def detect_copy(self, landmarks: List[Dict], threshold: float) -> bool:
        if self.copy_cooldown > 0:
            self.copy_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 16)
        
        if distance < threshold:
            self.copy_cooldown = 20
            return True
        
        return False
    
    def detect_paste(self, landmarks: List[Dict], threshold: float) -> bool:
        if self.paste_cooldown > 0:
            self.paste_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 20)
        
        if distance < threshold:
            self.paste_cooldown = 20
            return True
        
        return False
    
    def detect_scroll_gesture(self, landmarks: List[Dict], up_threshold: float, down_threshold: float) -> Optional[str]:
        dist_to_upper = self.calculate_distance_2d(landmarks, 4, 11)
        dist_to_middle = self.calculate_distance_2d(landmarks, 4, 10)
        
        current_direction = None
        
        if dist_to_upper < up_threshold:
            current_direction = "up"
        elif dist_to_middle < down_threshold:
            current_direction = "down"
        
        self.scroll_buffer.append(current_direction)
        
        if len(self.scroll_buffer) >= 3:
            directions = [d for d in self.scroll_buffer if d is not None]
            if len(directions) >= 3:
                up_count = directions.count("up")
                down_count = directions.count("down")
                
                if up_count > down_count and up_count >= 3:
                    self.scroll_direction = "up"
                    return "up"
                elif down_count > up_count and down_count >= 3:
                    self.scroll_direction = "down"
                    return "down"
        
        if current_direction is None:
            self.scroll_buffer.clear()
            self.scroll_direction = None
        
        return self.scroll_direction
    
    def detect_desktop_switch_left(self, landmarks: List[Dict], threshold: float) -> bool:
        if self.desktop_switch_left_cooldown > 0:
            self.desktop_switch_left_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 16)
        
        if distance < threshold:
            self.desktop_switch_left_cooldown = 20
            return True
        
        return False
    
    def detect_desktop_switch_right(self, landmarks: List[Dict], threshold: float) -> bool:
        if self.desktop_switch_right_cooldown > 0:
            self.desktop_switch_right_cooldown -= 1
            return False
        
        distance = self.calculate_distance_2d(landmarks, 4, 20)
        
        if distance < threshold:
            self.desktop_switch_right_cooldown = 20
            return True
        
        return False
    
    def detect_drag_start(self, left_landmarks: List[Dict], right_landmarks: List[Dict], threshold: float) -> bool:
        if self.drag_start_cooldown > 0:
            self.drag_start_cooldown -= 1
            return False
        
        if self.drag_active:
            return False
        
        distance = self.calculate_distance_between_hands(left_landmarks, right_landmarks, 8, 8)
        
        if distance < threshold:
            self.drag_start_cooldown = 20
            return True
        
        return False
    
    def detect_drag_end(self, left_landmarks: List[Dict], right_landmarks: List[Dict], threshold: float) -> bool:
        if self.drag_end_cooldown > 0:
            self.drag_end_cooldown -= 1
            return False
        
        if not self.drag_active:
            return False
        
        distance = self.calculate_distance_between_hands(left_landmarks, right_landmarks, 8, 4)
        
        if distance < threshold:
            self.drag_end_cooldown = 20
            return True
        
        return False
    
    def set_drag_active(self, active: bool):
        self.drag_active = active
    
    def is_drag_active(self) -> bool:
        return self.drag_active