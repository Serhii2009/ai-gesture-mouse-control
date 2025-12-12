"""Main application entry point"""

import cv2
import time
from camera import Camera
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController
import config


def main():
    camera = Camera(
        config.CAMERA_INDEX,
        config.CAMERA_WIDTH,
        config.CAMERA_HEIGHT,
        config.CAMERA_FPS
    )
    
    hand_tracker = HandTracker(
        config.MAX_NUM_HANDS,
        config.MIN_DETECTION_CONFIDENCE,
        config.MIN_TRACKING_CONFIDENCE
    )
    
    gesture_detector = GestureDetector()
    
    mouse_controller = MouseController(
        config.SMOOTHING_FACTOR,
        config.MOUSE_SPEED_MULTIPLIER,
        config.SCREEN_PADDING
    )
    
    prev_time = 0
    action_display_counter = 0
    action_text = ""
    
    print("Starting AI CV Gesture Mouse Control...")
    print("=== LEFT HAND GESTURES ===")
    print("Thumb + Index (quick): Single Click")
    print("Thumb + Middle: Double Click")
    print("Thumb + Ring: Copy (Ctrl+C)")
    print("Thumb + Pinky: Paste (Ctrl+V)")
    print("")
    print("=== RIGHT HAND GESTURES ===")
    print("Index Finger: Move Cursor")
    print("Thumb + Upper Middle Finger: Scroll Up")
    print("Thumb + Middle Middle Finger: Scroll Down")
    print("Thumb + Ring: Switch Desktop Left (Ctrl+Win+Left)")
    print("Thumb + Pinky: Switch Desktop Right (Ctrl+Win+Right)")
    print("")
    print("=== DRAG MODE ===")
    print("Left Index + Right Index: Start Drag (Mouse Down)")
    print("Left Index + Right Thumb: End Drag (Mouse Up)")
    print("")
    print("Press 'q' to quit")
    
    try:
        while True:
            success, frame = camera.read_frame()
            if not success:
                break
            
            results = hand_tracker.process_frame(frame)
            hands_data = hand_tracker.extract_hands_data(results, frame.shape)
            
            # Drag mode detection (highest priority)
            if hands_data['Left'] and hands_data['Right']:
                if gesture_detector.detect_drag_start(
                    hands_data['Left'],
                    hands_data['Right'],
                    config.DRAG_START_THRESHOLD
                ):
                    mouse_controller.mouse_down()
                    gesture_detector.set_drag_active(True)
                    action_display_counter = 20
                    action_text = "DRAG ON"
                    print("Drag mode activated!")
                
                if gesture_detector.detect_drag_end(
                    hands_data['Left'],
                    hands_data['Right'],
                    config.DRAG_END_THRESHOLD
                ):
                    mouse_controller.mouse_up()
                    gesture_detector.set_drag_active(False)
                    action_display_counter = 20
                    action_text = "DRAG OFF"
                    print("Drag mode deactivated!")
            
            # Right hand gestures
            if hands_data['Right']:
                # Desktop switching
                if gesture_detector.detect_desktop_switch_left(
                    hands_data['Right'],
                    config.DESKTOP_SWITCH_THRESHOLD
                ):
                    mouse_controller.switch_desktop_left()
                    action_display_counter = 20
                    action_text = "DESKTOP LEFT"
                    print("Switch desktop left!")
                
                if gesture_detector.detect_desktop_switch_right(
                    hands_data['Right'],
                    config.DESKTOP_SWITCH_THRESHOLD
                ):
                    mouse_controller.switch_desktop_right()
                    action_display_counter = 20
                    action_text = "DESKTOP RIGHT"
                    print("Switch desktop right!")
                
                # Scrolling
                scroll_direction = gesture_detector.detect_scroll_gesture(
                    hands_data['Right'],
                    config.SCROLL_UP_THRESHOLD,
                    config.SCROLL_DOWN_THRESHOLD
                )
                
                if scroll_direction == "up":
                    mouse_controller.scroll_up(config.SCROLL_SPEED)
                    action_display_counter = 5
                    action_text = "SCROLL UP"
                elif scroll_direction == "down":
                    mouse_controller.scroll_down(config.SCROLL_SPEED)
                    action_display_counter = 5
                    action_text = "SCROLL DOWN"
                elif not gesture_detector.detect_desktop_switch_left(hands_data['Right'], config.DESKTOP_SWITCH_THRESHOLD) and \
                     not gesture_detector.detect_desktop_switch_right(hands_data['Right'], config.DESKTOP_SWITCH_THRESHOLD):
                    # Cursor movement when not scrolling or switching desktops
                    index_tip = gesture_detector.get_fingertip_position(hands_data['Right'], 8)
                    
                    if index_tip:
                        screen_x, screen_y = mouse_controller.map_to_screen(
                            index_tip[0],
                            index_tip[1],
                            config.CAMERA_WIDTH,
                            config.CAMERA_HEIGHT
                        )
                        
                        smooth_x, smooth_y = mouse_controller.smooth_movement(screen_x, screen_y)
                        mouse_controller.move_mouse(smooth_x, smooth_y)
            
            # Left hand gestures
            if hands_data['Left']:
                # Single click
                if gesture_detector.detect_single_click(
                    hands_data['Left'],
                    config.SINGLE_CLICK_THRESHOLD,
                    config.SINGLE_CLICK_MAX_TIME
                ):
                    mouse_controller.click()
                    action_display_counter = 20
                    action_text = "SINGLE CLICK"
                    print("Single click!")
                
                # Double click
                if gesture_detector.detect_double_click(
                    hands_data['Left'],
                    config.DOUBLE_CLICK_THRESHOLD
                ):
                    mouse_controller.double_click()
                    action_display_counter = 20
                    action_text = "DOUBLE CLICK"
                    print("Double click!")
                
                # Copy
                if gesture_detector.detect_copy(
                    hands_data['Left'],
                    config.COPY_THRESHOLD
                ):
                    mouse_controller.copy()
                    action_display_counter = 20
                    action_text = "COPY (Ctrl+C)"
                    print("Copy!")
                
                # Paste
                if gesture_detector.detect_paste(
                    hands_data['Left'],
                    config.PASTE_THRESHOLD
                ):
                    mouse_controller.paste()
                    action_display_counter = 20
                    action_text = "PASTE (Ctrl+V)"
                    print("Paste!")
            
            # Display action feedback
            if action_display_counter > 0:
                color = (0, 255, 0)
                if "SCROLL" in action_text:
                    color = (0, 255, 255) if "UP" in action_text else (255, 100, 0)
                elif "DRAG" in action_text:
                    color = (255, 0, 255)
                elif "DESKTOP" in action_text:
                    color = (255, 165, 0)
                elif "COPY" in action_text or "PASTE" in action_text:
                    color = (0, 200, 255)
                
                cv2.putText(
                    frame,
                    action_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    color,
                    3
                )
                action_display_counter -= 1
            
            # Display drag mode status
            if gesture_detector.is_drag_active():
                cv2.putText(
                    frame,
                    "DRAG MODE ACTIVE",
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (255, 0, 255),
                    2
                )
            
            # Draw landmarks
            if config.SHOW_LANDMARKS:
                hand_tracker.draw_landmarks(frame, results)
            
            # Calculate and display FPS
            if config.SHOW_FPS:
                curr_time = time.time()
                fps = 1 / (curr_time - prev_time) if prev_time > 0 else 0
                prev_time = curr_time
                
                cv2.putText(
                    frame,
                    f"FPS: {int(fps)}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )
            
            cv2.imshow("AI CV Gesture Mouse Control", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        camera.release()
        hand_tracker.close()
        cv2.destroyAllWindows()
        print("Application closed successfully")


if __name__ == "__main__":
    main()