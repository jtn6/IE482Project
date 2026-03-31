# {Object Sorting Robot}

Team Members:
- Jonathan Nguyen (jtn6@buffalo.edu)

--- 

## Project Objective
The goal of this project is to design and implement an object sorting system using robotics and computer vision. A camera will detect objects placed in front of the  system and classify them based on visual features such as color. Based on the classification, the system will send commands to a robot to sort the objects into designated locations (such as bins).


## Contributions
 This project is unique because it integrates computer vision with automated material handling, similar to a real-world industrial sorting system. It demonstrates how robots can make decisions based on visual input and perform sorting tasks without human intervention. The project is also relevant to manufacturing and industrial engineering applications, such as quality control and automated workflows. Additionally, the system can be expanded to classify more complex objects using machine learning techniques.


## Project Plan
 The system will be developed using Python and OpenCV for object detection/classification. Initially, color based detection will be used to identify objects. The detected object type will then be mapped to a sorting decision.

 An Arduino Uno microcontroller will control the robot hardware, which may include a servo-based sorting mechanism. Commands will be sent from the computer to the robot by USB. 

 The implementation will involve developing the vision system, testing classification accuraacy, building the sorting mechanism, and integrating the full system. Online resources such as OpenCV tutorials and Arduino motor control guides will be used to make this happen.

## Milestones/Schedule Checklist
- [x] Complete this proposal document.  *Due March 31*
- [ ] Develop object detection using OpenCV (color-based classification)
- [ ] Map object types to sorting decisions (left/right bins)
- [ ] Build robot hardware (motor/servo and arduino setup)
- [ ] Integrate vision system with sorting mechanism
- [ ] Create progress report.  *Due April 21*
- [ ] Test sorting accuracy and improve reliability
- [ ] Create final presentation.  *Due May 5*
- [ ] Provide system documentation (README.md).  *Due May 15*


## Measures of Success
{How will you know you succeeded?  If you were to receive partial credit, what should we look for?}
- The system accureately detects and classifies objects based on color
- The robot correctly sorys objects into the appropriate locationo
- The system operates consistently with minimal errors
- The sorting process is clearly demonstrated in real time
- Another user can follow the README instructions to run the system independently