"""Main application entry point"""

import cv2
import time
from camera import Camera
from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController
import config


def main():
    # Initialize components
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
    
    gesture_detector = GestureDetector(
        config.PINCH_THRESHOLD,
        config.PINCH_HOLD_FRAMES,
        config.DOUBLE_CLICK_HOLD_TIME
    )
    
    mouse_controller = MouseController(
        config.SMOOTHING_FACTOR,
        config.MOUSE_SPEED_MULTIPLIER,
        config.SCREEN_PADDING
    )
    
    # FPS calculation
    prev_time = 0
    click_display_counter = 0
    click_type_text = ""
    scroll_display_counter = 0
    scroll_direction_text = ""
    
    print("Starting AI CV Gesture Mouse Control...")
    print("Right hand index finger: Move mouse")
    print("Left hand pinch: Single click (quick) or Double click (hold 2s)")
    print("Right hand thumb + middle finger upper part: Scroll UP")
    print("Right hand thumb + middle finger middle part: Scroll DOWN")
    print("Press 'q' to quit")
    
    try:
        while True:
            # Read frame
            success, frame = camera.read_frame()
            if not success:
                break
            
            # Process hand tracking
            results = hand_tracker.process_frame(frame)
            hands_data = hand_tracker.extract_hands_data(results, frame.shape)
            
            # Right hand: Mouse movement and scrolling
            if hands_data['Right']:
                # Check for scroll gesture
                scroll_direction = gesture_detector.detect_scroll_gesture(
                    hands_data['Right'],
                    config.SCROLL_UP_THRESHOLD,
                    config.SCROLL_DOWN_THRESHOLD
                )
                
                if scroll_direction == "up":
                    mouse_controller.scroll_up(config.SCROLL_SPEED)
                    scroll_display_counter = 5
                    scroll_direction_text = "SCROLL UP"
                elif scroll_direction == "down":
                    mouse_controller.scroll_down(config.SCROLL_SPEED)
                    scroll_display_counter = 5
                    scroll_direction_text = "SCROLL DOWN"
                else:
                    # Normal mouse movement when not scrolling
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
            
            # Left hand: Click gesture
            if hands_data['Left']:
                click_result = gesture_detector.detect_pinch_click(hands_data['Left'])
                
                if click_result == "single":
                    mouse_controller.click()
                    click_display_counter = 20
                    click_type_text = "SINGLE CLICK!"
                    print("Single click detected!")
                elif click_result == "double":
                    mouse_controller.double_click()
                    click_display_counter = 20
                    click_type_text = "DOUBLE CLICK!"
                    print("Double click detected!")
            
            # Display click feedback
            if click_display_counter > 0:
                cv2.putText(
                    frame,
                    click_type_text,
                    (50, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (0, 255, 0),
                    3
                )
                click_display_counter -= 1
            
            # Display scroll feedback
            if scroll_display_counter > 0:
                color = (0, 255, 255) if "UP" in scroll_direction_text else (255, 100, 0)
                cv2.putText(
                    frame,
                    scroll_direction_text,
                    (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    color,
                    3
                )
                scroll_display_counter -= 1
            
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
            
            # Display frame
            cv2.imshow("AI CV Gesture Mouse Control", frame)
            
            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        # Cleanup
        camera.release()
        hand_tracker.close()
        cv2.destroyAllWindows()
        print("Application closed successfully")


if __name__ == "__main__":
    main()