"""Mouse control using PyAutoGUI"""

import pyautogui
import numpy as np
from typing import Optional, Tuple


class MouseController:
    def __init__(self, smoothing: float, speed_multiplier: float, padding: int):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
        self.screen_width, self.screen_height = pyautogui.size()
        self.smoothing = smoothing
        self.speed_multiplier = speed_multiplier
        self.padding = padding
        
        self.prev_x = None
        self.prev_y = None
    
    def map_to_screen(self, x: float, y: float, frame_width: int, frame_height: int) -> Tuple[int, int]:
        screen_x = np.interp(
            x,
            [self.padding, frame_width - self.padding],
            [0, self.screen_width]
        )
        screen_y = np.interp(
            y,
            [self.padding, frame_height - self.padding],
            [0, self.screen_height]
        )
        
        return int(screen_x), int(screen_y)
    
    def smooth_movement(self, x: int, y: int) -> Tuple[int, int]:
        if self.prev_x is None or self.prev_y is None:
            self.prev_x, self.prev_y = x, y
            return x, y
        
        smooth_x = int(self.prev_x + (x - self.prev_x) * self.smoothing * self.speed_multiplier)
        smooth_y = int(self.prev_y + (y - self.prev_y) * self.smoothing * self.speed_multiplier)
        
        self.prev_x, self.prev_y = smooth_x, smooth_y
        
        return smooth_x, smooth_y
    
    def move_mouse(self, x: int, y: int):
        pyautogui.moveTo(x, y, _pause=False)
    
    def click(self):
        pyautogui.click(_pause=False)
    
    def double_click(self):
        pyautogui.doubleClick(_pause=False)
    
    def scroll_up(self, speed: int):
        pyautogui.scroll(speed, _pause=False)
    
    def scroll_down(self, speed: int):
        pyautogui.scroll(-speed, _pause=False)
    
    def copy(self):
        pyautogui.hotkey('ctrl', 'c', _pause=False)
    
    def paste(self):
        pyautogui.hotkey('ctrl', 'v', _pause=False)
    
    def switch_desktop_left(self):
        pyautogui.hotkey('ctrl', 'win', 'left', _pause=False)
    
    def switch_desktop_right(self):
        pyautogui.hotkey('ctrl', 'win', 'right', _pause=False)
    
    def mouse_down(self):
        pyautogui.mouseDown(_pause=False)
    
    def mouse_up(self):
        pyautogui.mouseUp(_pause=False)