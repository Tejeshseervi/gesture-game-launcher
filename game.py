import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

right_pressed = False
left_pressed = False
last_hover_time = 0

def count_extended_fingers(landmarks):
    count = 0
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        if landmarks[tip].y < landmarks[pip].y:
            count += 1

    # Thumb
    if landmarks[4].x < landmarks[3].x:
        count += 1

    return count

def detect_gesture(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    gesture = None
    extended = 0

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        extended = count_extended_fingers(hand_landmarks.landmark)

    return extended, frame

def hill_climb_mode():
    global right_pressed, left_pressed
    print("[INFO] Gesture Mode: Hill Climb Racing")
    print("[INFO] Open hand = Accelerate (→), Fist = Brake (←), Q = Quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        extended, annotated = detect_gesture(frame)

        if extended >= 4:  # open
            if not right_pressed:
                pyautogui.keyDown('right')
                right_pressed = True
                print("[ACTION] Accelerating →")
            if left_pressed:
                pyautogui.keyUp('left')
                left_pressed = False
            cv2.putText(annotated, "ACCELERATING", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        elif extended == 0:  # fist
            if not left_pressed:
                pyautogui.keyDown('left')
                left_pressed = True
                print("[ACTION] Braking ←")
            if right_pressed:
                pyautogui.keyUp('right')
                right_pressed = False
            cv2.putText(annotated, "BRAKING", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            if right_pressed:
                pyautogui.keyUp('right')
                right_pressed = False
            if left_pressed:
                pyautogui.keyUp('left')
                left_pressed = False
            cv2.putText(annotated, "NO GESTURE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)

        cv2.imshow("Hill Climb Racing", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def subway_surfers_mode():
    global last_hover_time
    print("[INFO] Gesture Mode: Subway Surfers")
    print("[INFO] 1 finger=Left, 2=Right, 3=Up, 4+=Down, Hoverboard=Show 3 fingers twice quickly, Q = Quit")
    
    last_gesture_time = 0
    last_extended = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        extended, annotated = detect_gesture(frame)
        current_time = time.time()

        if extended == 1:
            pyautogui.press('left')
            print("[ACTION] Move Left")
            time.sleep(0.5)

        elif extended == 2:
            pyautogui.press('right')
            print("[ACTION] Move Right")
            time.sleep(0.5)

        elif extended == 3:
            if current_time - last_hover_time < 1.2:
                pyautogui.press('space')
                pyautogui.press('space')
                print("[ACTION] Hoverboard (Double Space)")
                last_hover_time = 0
            else:
                pyautogui.press('up')
                print("[ACTION] Jump")
                last_hover_time = current_time
            time.sleep(0.5)

        elif extended >= 4:
            pyautogui.press('down')
            print("[ACTION] Roll Down")
            time.sleep(0.5)

        cv2.imshow("Subway Surfers", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# MAIN MENU
print("Choose your Game Mode:")
print("1. Hill Climb Racing")
print("2. Subway Surfers")
choice = input("Enter choice (1 or 2): ")

if choice == '1':
    hill_climb_mode()
elif choice == '2':
    subway_surfers_mode()
else:
    print("Invalid choice. Exiting...")

# Cleanup
cap.release()
cv2.destroyAllWindows()
pyautogui.keyUp('right')
pyautogui.keyUp('left')
print("[INFO] Exited cleanly.")
