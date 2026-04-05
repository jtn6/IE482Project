#For purposes of detecting HSV values, this file will print the HSV values so that I can 
#determine the correct HSV ranges for red and blue objects. This is not used in the final program, but just used solely for detecting HSV values and determining ranges.

import cv2

# Global variable to store the current frame
current_frame = None

def show_hsv_value(event, x, y, flags, param):
    global current_frame

    if event == cv2.EVENT_MOUSEMOVE and current_frame is not None:
        # Get the BGR pixel value at the mouse location
        bgr_pixel = current_frame[y, x]

        # Convert that one pixel to HSV
        hsv_pixel = cv2.cvtColor(
            cv2.UMat(cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)).get()[y:y+1, x:x+1],
            cv2.COLOR_HSV2BGR
        )

def mouse_callback(event, x, y, flags, param):
    global current_frame

    if current_frame is None:
        return

    if event == cv2.EVENT_MOUSEMOVE:
        hsv_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2HSV)
        bgr_value = current_frame[y, x]
        hsv_value = hsv_frame[y, x]

        print(f"Mouse at ({x}, {y})  BGR={bgr_value}  HSV={hsv_value}")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    exit()

cv2.namedWindow("HSV Picker")
cv2.setMouseCallback("HSV Picker", mouse_callback)

while True:
    success, frame = camera.read()

    if not success:
        print("Error: Could not read frame.")
        break

    frame = cv2.flip(frame, 1)
    current_frame = frame.copy()

    cv2.putText(
        frame,
        "Move mouse over object to print HSV values. Press q to quit.",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2
    )

    cv2.imshow("HSV Picker", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()