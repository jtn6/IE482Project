# Object Sorting Robot

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
- [ ] Draft hardware, conveyor, servo layout
- [ ] Create final presentation.  *Due May 5*
- [ ] Provide system documentation (README.md).  *Due May 15*


## Measures of Success
- The system accureately detects and classifies objects based on color
- The robot correctly sorts objects into the appropriate location
- The system operates consistently with minimal errors
- The sorting process is clearly demonstrated in real time
- Another user can follow the README instructions to run the system independently
