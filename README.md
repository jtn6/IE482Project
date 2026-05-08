# Object Sorting Robot



## Motivation / Overview

This project focuses on designing and implementing an automated sorting system that mimics a real world manufacturing process that can be found in warehouses. This system uses computer vision to detect object color and control a mechanical actuator to sort items in real time. The motivation behind this project is to explore how vision systems, microcontrollers, and automation can be integrated into a single workflow. This type of system is commonly used in industrial environments for material handling and quality control. This project is particularly relevant to students interested in robotics, manufacturing systems, and automation

---

## Demonstration

The system consists of a conveyor belt, a camera-based detection system, and a servo with a straw attached, acting as the "arm" for the sorting mechanism. When the conveyor belt is running, objects are placed on a conveyor belt and pass through a detection zone monitored by a webcam. The system identifies the object color and determines a sorting direction. After the object gets detected, a servo motor rotates to physically deflect the object off the conveyor belt into the appropriate bin, simulating a real-world factory sorting process.

### How the entire setup works:

The equipment needed for this project is/as follows:
- Laptop with camera (or external webcam)
- Arduino Uno
- Conveyor Belt
- Objects of interest (to place on the belt)
- SG90 Servo Motor
- Straw

An object is placed on a linear conveyor belt that moves objects downstream (in this case, I will be using small foam blocks colored red and blue). After the object moves into the region of interest in the camera frame, the system will then classify an object color. After an the color is identified, a sorting decision is then made and sent to the terminal "LEFT" or "RIGHT". The Arduino Uno then receives the command, and moves the servo arm to deflect the the object off the belt, into its respective container.


Youtube Demo Here:

https://youtu.be/HYyeJFBxogo

---


## Installation Instructions

### 1. Clone the repository

```
git clone https://github.com/jtn6/IE482Project
cd IE482Project
```

### 2. Create and Activate a Virtual Environment

```
python -m venv robotic_sorter
robotic_sorter\Scripts\Activate
```

### 3. Install Required Python Libraries

```
pip install opencv-python numpy pyserial
```

### 4. Arduino Setup

Upload the following code to your Arduino Uno:

```
#include <Servo.h>

Servo sorterServo;
String command = "";

const int REST_POS = 90;
const int LEFT_POS = 30;
const int RIGHT_POS = 150;

const int TRAVEL_DELAY = 2000;  // time from camera ROI to servo
const int TAP_TIME = 300;       // time servo stays out to hit object

void setup() {
  Serial.begin(9600);
  sorterServo.attach(9);
  sorterServo.write(REST_POS);
}

void loop() {
  if (Serial.available()) {
    command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LEFT") {
      delay(TRAVEL_DELAY);
      sorterServo.write(LEFT_POS);
      delay(TAP_TIME);
      sorterServo.write(REST_POS);
    }

    else if (command == "RIGHT") {
      delay(TRAVEL_DELAY);
      sorterServo.write(RIGHT_POS);
      delay(TAP_TIME);
      sorterServo.write(REST_POS);
    }
  }
}
```
After this is done, verify the code and upload it to the board.
Make sure the servo is connected to pin 9 on the board, and the Arduino is connected via USB.

### 5. Python Setup (main.py code)

Copy and paste this code:
```
#import all necessary libraries, can add more as needed

import cv2
import numpy as np
import serial
import time

#running the detection of red and blue only, can change colors as desired

print("Running red and blue detection") 

camera = cv2.VideoCapture(0)

arduino = serial.Serial("COM3", 9600)
time.sleep(2)

if not camera.isOpened():
    print("Error: Could not open webcam.")
    arduino.close()
    raise SystemExit

last_decision = ""
last_send_time = 0
cooldown = 3.0  # seconds
while True:
    success, frame = camera.read()

    if not success:
        print("Error: Could not read frame.")
        break

    # Flip frame so it acts like a mirror
    frame = cv2.flip(frame, 1)

    # Get frame size
    frame_height, frame_width, _ = frame.shape

    # Define ROI coordinates within the camera frame (this creates a center box that will only detect what's inside it.)
    x1 = int(frame_width * 0.3)
    y1 = int(frame_height * 0.3)
    x2 = int(frame_width * 0.7)
    y2 = int(frame_height * 0.7)

    # Extract ROI
    roi = frame[y1:y2, x1:x2]

    # Convert ROI to HSV values
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Blue range HSV values, can adjust as needed for different lighting conditions or shades of blue
    lower_blue = np.array([98, 170, 110])
    upper_blue = np.array([112, 230, 170])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Red range HSV values, red is tricky because it wraps around the hue spectrum, so we need two ranges to cover it. Can still adjust as needed for different lighting conditions or shades of red.
   # Red cube HSV range
    # Red HSV range
    lower_red = np.array([170, 170, 120])
    upper_red = np.array([180, 255, 190])

    red_mask = cv2.inRange(hsv, lower_red, upper_red)

    # Clean masks (this opens two windows, one for the red mask and one for the blue mask, so you can see what the camera is detecting. You can close these windows once you have the HSV values dialed in and the detection working well, or keep them open for debugging purposes.)
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

    # Decision logic when red or blue is detected
    if red_detected and not blue_detected:
        decision = "LEFT"
    elif blue_detected and not red_detected:
        decision = "RIGHT"
    elif red_detected and blue_detected:
        decision = "MULTIPLE OBJECTS"
    else:
        decision = "WAIT"

    # Only send when decision changes
    # Only send actual sorting commands
    current_time = time.time()

    if decision in ["LEFT", "RIGHT"]:
        if decision != last_decision and current_time - last_send_time > cooldown:
            arduino.write((decision + "\n").encode())
            print("Sent:", decision)
            last_decision = decision
            last_send_time = current_time

    elif decision == "WAIT":
        last_decision = "WAIT"

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
    # Press 'q' to quit the program and close all windows, release the camera, and close the serial connection to the Arduino. This is important to free up resources and allow other programs to use the camera and serial port in the future without issues.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
arduino.close()
cv2.destroyAllWindows()
```

### 6. Python Setup (hsv_detector.py code)

In the event that you're still having trouble figuring out hsv values for the colors of objects you want to detect or just want to change the color, I created an HSV detector file that opens a camera window and detects the hsv value of the object that your mouse is hovering over. You can run this before or after the main.py code, and edit the values as desired. Copy and paste this code:

```
#For purposes of detecting HSV values, this file will print the HSV values so that I can determine the correct HSV ranges for red and blue objects. This is not used in the final program, but just used solely for detecting HSV values and determining ranges.

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

#Press q to close all windows
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

```
---

## References

The following resources were used during development:

- https://docs.opencv.org/
- https://www.arduino.cc/reference/en/
- https://pyserial.readthedocs.io/
- YouTube tutorials on OpenCV color detection and Arduino servo control

---

## Future Work

If more time were available, several improvements could be made:
- improve detection under different lighting conditions
- add more support for object types beyond color classification
- replace simple servo deflection with a more precise mechanical sorting system

---

# Initial Proposal:

Team Members:
- Jonathan Nguyen (jtn6@buffalo.edu)

--- 

## Project Objective
The goal of this project is to design and implement an object sorting system using robotics and computer vision. A camera will detect objects placed in front of the system and classify them based on visual features such as color. Based on the classification, the system will send commands to a robot to sort the objects into designated locations (such as bins).


## Contributions
This project is unique because it integrates computer vision with automated material handling, similar to a real-world industrial sorting system. It demonstrates how robots can make decisions based on visual input and perform sorting tasks without human intervention. The project is also relevant to manufacturing and industrial engineering applications, such as quality control and automated workflows. Additionally, the system can be expanded to classify more complex objects using machine learning techniques.


## Project Plan

The system will be developed using Python and OpenCV for object detection and classification. Initially, color-based detection will be used to identify objects. The detected object type will then be mapped to a sorting decision. After this is completed, an Arduino Uno microcontroller will control the robot hardware, including a servo-based sorting mechanism. Commands will be sent from the computer to the Arduino via USB.

During the demonstration phase, objects will be placed onto a Mini-Mover conveyor belt and transported through a fixed detection zone monitored by a camera. As each object passes through this region of interest (ROI), the vision system will classify the object based on color. Once detected, the system will assign a sorting decision (e.g., LEFT or RIGHT). After a short delay—corresponding to the time it takes for the object to travel from the detection zone to the sorting point—the Arduino will actuate a servo motor.

The servo, equipped with an attached arm (e.g., a boba straw), will physically deflect the object off the conveyor belt. This mimics an industrial sorting process where items are redirected in real time based on classification.

The implementation will involve developing the vision system, testing classification accuracy, designing and building the sorting mechanism, and integrating the full system. Online resources such as OpenCV tutorials and Arduino motor control guides will be used to support development throughout the project.

## Milestones/Schedule Checklist
- [x] Complete this proposal document.  *Due March 31*
- [x] Develop object detection using OpenCV (color-based classification)
- [x] Map object types to sorting decisions (left/right bins)
- [x] Build robot hardware (motor/servo and arduino setup)
- [x] Integrate vision system with sorting mechanism
- [x] Create progress report.  *Due April 21*
- [x] Test sorting accuracy and improve reliability
- [x] Draft hardware, conveyor, servo layout
- [x] Create final presentation.  *Due May 5*
- [ ] Provide system documentation (README.md).  *Due May 15*


## Measures of Success
- The system accurately detects and classifies objects based on color
- The robot correctly sorts objects into the appropriate location
- The system operates consistently with minimal errors
- The sorting process is clearly demonstrated in real time
- Another user can follow the README instructions to run the system independently
