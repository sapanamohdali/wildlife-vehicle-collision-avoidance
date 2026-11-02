from pathlib import Path
import cv2
import torch
import time
import json
import paho.mqtt.client as mqtt
from ultralytics import YOLO

# ============================================================
# FINAL WILDLIFE + HUMAN THREAT DETECTION SYSTEM
# ============================================================

PROJECT_DIR = Path(
    "/Users/cupcake/PycharmProjects/PythonProject1"
)

ANIMAL_MODEL_PATH = (
    PROJECT_DIR
    / "runs"
    / "animal_detector"
    / "weights"
    / "best.pt"
)

HUMAN_MODEL_PATH = PROJECT_DIR / "yolov8n.pt"



VIDEO_PATH = (
    PROJECT_DIR
    / "input"
    / "wildlife_clear_test.mp4"
)



# ============================================================
# SETTINGS
# ============================================================

ANIMAL_CONFIDENCE = 0.50
HUMAN_CONFIDENCE = 0.50

CLEAR_DELAY = 10.0

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "edge/wildlife/status"


# ============================================================
# DEVICE
# ============================================================

if torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"


print("=" * 65)
print("FINAL WILDLIFE + HUMAN THREAT DETECTION SYSTEM")
print("=" * 65)

print(f"\nDevice: {DEVICE}")


# ============================================================
# CHECK FILES
# ============================================================

if not ANIMAL_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Animal model not found:\n{ANIMAL_MODEL_PATH}"
    )

if not HUMAN_MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Human model not found:\n{HUMAN_MODEL_PATH}"
    )

if not VIDEO_PATH.exists():
    raise FileNotFoundError(
        f"Video not found:\n{VIDEO_PATH}"
    )


# ============================================================
# LOAD MODELS
# ============================================================

print("\nLoading animal model...")

animal_model = YOLO(
    str(ANIMAL_MODEL_PATH)
)

print("Animal model loaded.")
print("Animal classes:", animal_model.names)


print("\nLoading human model...")

human_model = YOLO(
    str(HUMAN_MODEL_PATH)
)

print("Human model loaded.")


# ============================================================
# MQTT
# ============================================================

print("\nConnecting to MQTT broker...")

mqtt_client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="wildlife_final_system"
)

mqtt_connected = False

try:

    mqtt_client.connect(
        MQTT_BROKER,
        MQTT_PORT,
        60
    )

    mqtt_client.loop_start()

    mqtt_connected = True

    print("MQTT connected successfully.")

except Exception as error:

    print("MQTT connection failed:")
    print(error)


# ============================================================
# MQTT STATE
# ============================================================

last_published_state = None
last_published_object = None


def publish_status(status, object_type=None):

    global last_published_state
    global last_published_object

    # Don't publish the exact same state repeatedly.
    if (
        status == last_published_state
        and object_type == last_published_object
    ):
        return

    message = {
        "status": status
    }

    if object_type is not None:
        message["object"] = object_type

    message["timestamp"] = int(time.time())

    payload = json.dumps(message)

    print("\nMQTT PUBLISH:")
    print(payload)

    if mqtt_connected:

        result = mqtt_client.publish(
            MQTT_TOPIC,
            payload
        )

        result.wait_for_publish()

        print("MQTT message sent.")

    else:

        print("MQTT unavailable.")

    last_published_state = status
    last_published_object = object_type


# ============================================================
# OPEN VIDEO
# ============================================================

print("\nOpening wildlife video...")

cap = cv2.VideoCapture(
    str(VIDEO_PATH)
)

if not cap.isOpened():
    raise RuntimeError(
        "Could not open wildlife.mp4"
    )


fps = cap.get(
    cv2.CAP_PROP_FPS
)

total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)

print(f"Video FPS: {fps:.2f}")
print(f"Total frames: {total_frames}")


# ============================================================
# STATE VARIABLES
# ============================================================


frame_number = 0

# Real-time clearance timer
no_detection_start = None

current_state = "CLEAR"

current_object = None


# ============================================================
# INITIAL MQTT STATE
# ============================================================

publish_status(
    "CLEAR"
)


print("\nStarting final detection...")
print("Press ESC to stop.")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    # --------------------------------------------------------
    # ANIMAL DETECTION
    # --------------------------------------------------------

    animal_results = animal_model.track(
        frame,
        persist=True,
        tracker="bytetrack.yaml",
        conf=ANIMAL_CONFIDENCE,
        device=DEVICE,
        verbose=False
    )

    animal_result = animal_results[0]

    animal_found = False

    if animal_result.boxes is not None:

        for box in animal_result.boxes:

            confidence = float(
                box.conf[0]
            )

            if confidence < ANIMAL_CONFIDENCE:
                continue

            animal_found = True

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = (
                f"ANIMAL "
                f"{confidence * 100:.1f}%"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 0),
                2
            )


    # --------------------------------------------------------
    # HUMAN DETECTION
    # --------------------------------------------------------

    human_results = human_model.predict(
        frame,
        conf=HUMAN_CONFIDENCE,
        classes=[0],
        device=DEVICE,
        verbose=False
    )

    human_result = human_results[0]

    human_found = False

    if human_result.boxes is not None:

        for box in human_result.boxes:

            confidence = float(
                box.conf[0]
            )

            if confidence < HUMAN_CONFIDENCE:
                continue

            human_found = True

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            label = (
                f"HUMAN "
                f"{confidence * 100:.1f}%"
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 0, 0),
                2
            )

    # ========================================================
    # THREAT DECISION
    # ========================================================

    # Human has priority if both are detected.
    if human_found:

        current_state = "HUMAN DETECTED"
        current_object = "human"

        # Cancel the clearance timer.
        no_detection_start = None

        publish_status("THREAT", "human")

    elif animal_found:

        current_state = "ANIMAL DETECTED"
        current_object = "animal"

        # Cancel the clearance timer.
        no_detection_start = None

        publish_status("THREAT", "animal")

    else:

        # Start the timer when detections disappear.
        if no_detection_start is None:
            no_detection_start = time.monotonic()

        # Clear the threat only after 10 real seconds.
        elapsed_no_detection = (
            time.monotonic() - no_detection_start
        )

        if elapsed_no_detection >= CLEAR_DELAY:

            current_state = "CLEAR"
            current_object = None

            publish_status("CLEAR")


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.putText(
        frame,
        current_state,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 255),
        3
    )

    cv2.putText(
        frame,
        f"Frame: {frame_number}/{total_frames}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "Animal: GREEN | Human: BLUE",
        (30, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Wildlife Threat Detection System",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break



# ============================================================
# CLEANUP
# ============================================================

# Report if the video ends while a threat is still active.
if current_state in ("HUMAN DETECTED", "ANIMAL DETECTED"):
    publish_status("VIDEO_ENDED")

cap.release()

cv2.destroyAllWindows()

if mqtt_connected:

    mqtt_client.loop_stop()
    mqtt_client.disconnect()


print("\n" + "=" * 65)
print("FINAL WILDLIFE + HUMAN THREAT DETECTION FINISHED")
print("=" * 65)
