import cv2
import numpy as np
import serial
import time

print("Running red and blue detection")

camera = cv2.VideoCapture(0)

arduino = serial.Serial("COM3", 9600)
time.sleep(2)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    arduino.close()
    raise SystemExit

last_decision = ""

while True:
    success, frame = camera.read()

    if not success:
        print("Error: Could not read frame.")
        break

    # Flip frame so it acts like a mirror
    frame = cv2.flip(frame, 1)

    # Get frame size
    frame_height, frame_width, _ = frame.shape

    # Define ROI coordinates
    x1 = int(frame_width * 0.3)
    y1 = int(frame_height * 0.3)
    x2 = int(frame_width * 0.7)
    y2 = int(frame_height * 0.7)

    # Extract ROI
    roi = frame[y1:y2, x1:x2]

    # Convert ROI to HSV
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Blue range
    lower_blue = np.array([100, 180, 150])
    upper_blue = np.array([115, 255, 255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Red range
    lower_red_1 = np.array([0, 120, 70])
    upper_red_1 = np.array([10, 255, 255])
    lower_red_2 = np.array([170, 120, 70])
    upper_red_2 = np.array([180, 255, 255])

    red_mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    red_mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    red_mask = red_mask_1 + red_mask_2

    # Clean masks
    kernel = np.ones((5, 5), np.uint8)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_detected = False
    blue_detected = False
    decision = "WAIT"

    # Draw ROI box
    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Draw red objects
    for contour in red_contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            red_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x + x1, y + y1), (x + w + x1, y + h + y1), (0, 255, 0), 2)
            cv2.putText(
                frame,
                "Red Object",
                (x + x1, y + y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Draw blue objects
    for contour in blue_contours:
        area = cv2.contourArea(contour)
        if area > 600:
            blue_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x + x1, y + y1), (x + w + x1, y + h + y1), (0, 165, 255), 2)
            cv2.putText(
                frame,
                "Blue Object",
                (x + x1, y + y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 165, 255),
                2
            )

    # Decision logic
    if red_detected and not blue_detected:
        decision = "LEFT"
    elif blue_detected and not red_detected:
        decision = "RIGHT"
    elif red_detected and blue_detected:
        decision = "MULTIPLE OBJECTS"
    else:
        decision = "WAIT"

    # Only send when decision changes
    if decision != last_decision:
        arduino.write((decision + "\n").encode())
        print("Sent:", decision)
        last_decision = decision

    # Show decision
    cv2.putText(
        frame,
        f"Decision: {decision}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        3
    )

    # Show windows
    cv2.imshow("Color Detection", frame)
    cv2.imshow("Red Mask", red_mask)
    cv2.imshow("Blue Mask", blue_mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
arduino.close()
cv2.destroyAllWindows()