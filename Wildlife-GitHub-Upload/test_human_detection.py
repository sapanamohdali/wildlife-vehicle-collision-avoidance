from pathlib import Path
import cv2
import torch
from ultralytics import YOLO

# ============================================================
# HUMAN DETECTION TEST
# ============================================================

PROJECT_DIR = Path(
    "/Users/cupcake/PycharmProjects/PythonProject1"
)

MODEL_PATH = PROJECT_DIR / "yolov8n.pt"
VIDEO_PATH = PROJECT_DIR / "input" / "human.mp4"


# ============================================================
# DEVICE
# ============================================================

if torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"


print("=" * 60)
print("HUMAN DETECTION TEST")
print("=" * 60)

print(f"\nDevice: {DEVICE}")


# ============================================================
# CHECK FILES
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"YOLO model not found:\n{MODEL_PATH}"
    )

if not VIDEO_PATH.exists():
    raise FileNotFoundError(
        f"Human video not found:\n{VIDEO_PATH}"
    )


# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading YOLO human detection model...")

model = YOLO(str(MODEL_PATH))

print("Model loaded successfully.")


# ============================================================
# OPEN VIDEO
# ============================================================

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise RuntimeError("Could not open human.mp4")


fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(
    cap.get(cv2.CAP_PROP_FRAME_COUNT)
)

print(f"\nFPS: {fps:.2f}")
print(f"Total frames: {total_frames}")

print("\nStarting human detection...")
print("Press ESC to stop.")


# ============================================================
# DETECTION
# ============================================================

frame_number = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    results = model.predict(
        frame,
        conf=0.50,
        classes=[0],
        device=DEVICE,
        verbose=False
    )

    result = results[0]

    human_found = False

    if result.boxes is not None:

        for box in result.boxes:

            confidence = float(box.conf[0])

            if confidence < 0.50:
                continue

            human_found = True

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            # Draw human box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (255, 0, 0),
                2
            )

            label = f"HUMAN {confidence * 100:.1f}%"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 0, 0),
                2
            )


    # ========================================================
    # STATUS
    # ========================================================

    if human_found:
        status = "HUMAN DETECTED"
    else:
        status = "CLEAR"


    cv2.putText(
        frame,
        status,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.1,
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


    cv2.imshow(
        "Human Detection Test",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 60)
print("HUMAN DETECTION TEST FINISHED")
print("=" * 60)