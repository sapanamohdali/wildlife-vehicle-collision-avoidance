
from pathlib import Path
import cv2

PROJECT_DIR = Path("/Users/cupcake/PycharmProjects/PythonProject1")
INPUT_VIDEO = PROJECT_DIR / "input" / "wildlife.mp4"
OUTPUT_VIDEO = PROJECT_DIR / "input" / "wildlife_clear_test.mp4"

EMPTY_SECONDS = 15

cap = cv2.VideoCapture(str(INPUT_VIDEO))

if not cap.isOpened():
    raise RuntimeError(f"Cannot open video: {INPUT_VIDEO}")

fps = cap.get(cv2.CAP_PROP_FPS)
if fps <= 0:
    fps = 25.0

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(
    str(OUTPUT_VIDEO), fourcc, fps, (width, height)
)

if not writer.isOpened():
    cap.release()
    raise RuntimeError("Could not create the test video.")

# Copy the original wildlife video.
while True:
    success, frame = cap.read()
    if not success:
        break
    writer.write(frame)

cap.release()

# Add 15 seconds of an empty black scene.
empty_frame = (0 * __import__("numpy").ones(
    (height, width, 3), dtype="uint8"
))

for _ in range(int(fps * EMPTY_SECONDS)):
    writer.write(empty_frame)

writer.release()

print("Test video created successfully:")
print(OUTPUT_VIDEO)
print(f"Added {EMPTY_SECONDS} seconds of empty scene.")
