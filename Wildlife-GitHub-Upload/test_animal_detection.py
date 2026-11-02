from pathlib import Path
import cv2
import torch
from ultralytics import YOLO

# ============================================================
# ANIMAL DETECTION TEST
# ============================================================

PROJECT_DIR = Path("/Users/cupcake/PycharmProjects/PythonProject1")

MODEL_PATH = PROJECT_DIR / "runs" / "animal_detector" / "weights" / "best.pt"
VIDEO_PATH = PROJECT_DIR / "input" / "wildlife.mp4"

print("=" * 60)
print("ANIMAL DETECTION TEST")
print("=" * 60)

# ------------------------------------------------------------
# Check files
# ------------------------------------------------------------

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model not found:\n{MODEL_PATH}"
    )

if not VIDEO_PATH.exists():
    raise FileNotFoundError(
        f"Video not found:\n{VIDEO_PATH}"
    )

# ------------------------------------------------------------
# Device
# ------------------------------------------------------------

if torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"

print(f"\nDevice: {DEVICE}")
print(f"Model: {MODEL_PATH}")
print(f"Video: {VIDEO_PATH}")

# ------------------------------------------------------------
# Load model
# ------------------------------------------------------------

print("\nLoading trained animal model...")

model = YOLO(str(MODEL_PATH))

print("Model loaded successfully.")
print("Classes:", model.names)

# ------------------------------------------------------------
# Open video
# ------------------------------------------------------------

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise RuntimeError("Could not open wildlife.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(f"\nFPS: {fps:.2f}")
print(f"Total frames: {total_frames}")

print("\nStarting detection...")
print("Press ESC to stop.")

# ------------------------------------------------------------
# Detection loop
# ------------------------------------------------------------

frame_number = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame_number += 1

    results = model.predict(
        source=frame,
        conf=0.50,
        device=DEVICE,
        verbose=False
    )

    result = results[0]

    animal_found = False

    if result.boxes is not None and len(result.boxes) > 0:

        for box in result.boxes:

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            animal_found = True

            # Draw box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"ANIMAL {confidence * 100:.1f}%"

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 25)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if animal_found:

        status = "ANIMAL DETECTED"

    else:

        status = "CLEAR"

    cv2.putText(
        frame,
        status,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    # Frame counter
    cv2.putText(
        frame,
        f"Frame: {frame_number}/{total_frames}",
        (30, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow("Animal Detection Test", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == 27:  # ESC
        break

# ------------------------------------------------------------
# Cleanup
# ------------------------------------------------------------

cap.release()
cv2.destroyAllWindows()

print("\n" + "=" * 60)
print("ANIMAL DETECTION TEST FINISHED")
print("=" * 60)