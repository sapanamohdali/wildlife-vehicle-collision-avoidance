# Wildlife–Vehicle Collision Detection and Avoidance System

An AI-powered wildlife detection and vehicle collision avoidance prototype designed to help reduce animal–vehicle collisions using computer vision and real-time alert communication.

## Project Overview

Wildlife crossing roads can create dangerous situations for both animals and road users. This project explores a camera-based system that detects animals near roads and communicates potential threats through an alert mechanism.

The system uses YOLO-based object detection, OpenCV for video processing, and MQTT for communication.

## Key Features

- **Animal Detection:** Detects animals in video using a custom-trained YOLO model.
- **Human Detection:** Uses a YOLO model to identify humans.
- **Video Processing:** Processes video frames using OpenCV.
- **Clearance Monitoring:** Includes a 10-second clearance timer after detections disappear.
- **MQTT Communication:** Publishes wildlife status messages to an MQTT broker.
- **Testing Modules:** Includes scripts for testing detection, clearance, and MQTT functionality.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| OpenCV | Video and image processing |
| YOLO / Ultralytics | Object detection |
| PyTorch | Deep learning framework |
| Paho MQTT | Message communication |
| Mosquitto | MQTT broker |

## Project Structure

```text
wildlife-vehicle-collision-avoidance/
│
├── Wildlife-GitHub-Upload/
│   ├── final_detection.py
│   ├── train_animal_model.py
│   ├── prepare_animal_dataset.py
│   ├── safe_distance_preview.py
│   ├── test_animal_detection.py
│   ├── test_human_detection.py
│   ├── test_clearance.py
│   ├── test_mqtt.py
│   └── make_clear_test_video.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Project Status

Academic prototype under development. The repository currently contains the Python source files and initial dependency list. Further integration, testing, and deployment work may be added.

## Future Improvements

- Integrate roadside camera feeds.
- Improve detection under different lighting and weather conditions.
- Implement distance and collision-risk estimation.
- Develop a monitoring dashboard.
- Test the system in realistic wildlife-road scenarios.

## Author

**Sapana**

Computer Science and Engineering Student

## Project Domain

Artificial Intelligence | Computer Vision | Deep Learning | IoT | Road Safety | Wildlife Conservation
