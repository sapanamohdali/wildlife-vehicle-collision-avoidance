from pathlib import Path
import cv2
import math

# ============================================================
# CAMERA DISTANCE CALIBRATION
# ============================================================

PROJECT_DIR = Path(
    "/Users/cupcake/PycharmProjects/PythonProject1"
)

VIDEO_PATH = PROJECT_DIR / "input" / "wildlife.mp4"

# Camera design parameters
CAMERA_HEIGHT = 4.0       # metres
VERTICAL_FOV = 56.0       # degrees

# Use a clear frame from the video
CALIBRATION_FRAME = 600

cap = cv2.VideoCapture(str(VIDEO_PATH))

if not cap.isOpened():
    raise RuntimeError("Could not open wildlife.mp4")

cap.set(cv2.CAP_PROP_POS_FRAMES, CALIBRATION_FRAME)

success, frame = cap.read()

if not success:
    raise RuntimeError("Could not read calibration frame")

height, width = frame.shape[:2]

# ============================================================
# CALCULATE FOCAL LENGTH IN PIXELS
# ============================================================

vfov_rad = math.radians(VERTICAL_FOV)

fy = (
    height / 2.0
) / math.tan(vfov_rad / 2.0)

print("=" * 65)
print("FIXED CAMERA DISTANCE CALIBRATION")
print("=" * 65)

print(f"Image size       : {width} x {height}")
print(f"Camera height    : {CAMERA_HEIGHT} m")
print(f"Vertical FOV     : {VERTICAL_FOV} degrees")
print(f"Calculated fy    : {fy:.2f} pixels")

print()
print("Click the ROAD VANISHING POINT / HORIZON.")
print("Then press ENTER.")
print("Press ESC to cancel.")

selected_y = None


# ============================================================
# MOUSE CALLBACK
# ============================================================

def mouse_callback(event, x, y, flags, param):

    global selected_y

    if event == cv2.EVENT_LBUTTONDOWN:

        selected_y = y

        print(
            f"\nSelected horizon position: y = {y} pixels"
        )


cv2.namedWindow("Camera Calibration")

cv2.setMouseCallback(
    "Camera Calibration",
    mouse_callback
)


# ============================================================
# WAIT FOR HORIZON SELECTION
# ============================================================

while True:

    display = frame.copy()

    if selected_y is not None:

        cv2.line(
            display,
            (0, selected_y),
            (width, selected_y),
            (0, 0, 255),
            4
        )

        cv2.putText(
            display,
            "CALIBRATED HORIZON",
            (30, max(selected_y - 20, 30)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

    cv2.putText(
        display,
        "Click road vanishing point / horizon",
        (30, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow(
        "Camera Calibration",
        display
    )

    key = cv2.waitKey(30) & 0xFF

    if key == 13 and selected_y is not None:
        break

    if key == 27:
        cap.release()
        cv2.destroyAllWindows()
        print("Calibration cancelled.")
        exit()


cv2.destroyAllWindows()
cap.release()


# ============================================================
# DISTANCE CALCULATION
# ============================================================

def distance_from_pixel_y(pixel_y):

    difference = pixel_y - selected_y

    if difference <= 0:
        return None

    distance = (
        CAMERA_HEIGHT * fy / difference
    )

    return distance


# ============================================================
# DISPLAY REFERENCE DISTANCES
# ============================================================

frame = frame.copy()

cv2.line(
    frame,
    (0, selected_y),
    (width, selected_y),
    (0, 0, 255),
    4
)

cv2.putText(
    frame,
    "HORIZON / VANISHING LINE",
    (30, max(selected_y - 20, 30)),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 0, 255),
    2
)


# Calculate where known distances appear in the image
reference_distances = [5, 10, 15, 20, 30]

for distance in reference_distances:

    pixel_difference = (
        CAMERA_HEIGHT * fy / distance
    )

    pixel_y = int(
        selected_y + pixel_difference
    )

    if 0 <= pixel_y < height:

        cv2.line(
            frame,
            (0, pixel_y),
            (width, pixel_y),
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"{distance} m",
            (20, max(pixel_y - 8, 25)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )


# ============================================================
# RESULT
# ============================================================

print()
print("=" * 65)
print("CALIBRATION RESULT")
print("=" * 65)

print(f"Horizon pixel Y : {selected_y}")
print(f"Camera height   : {CAMERA_HEIGHT} m")
print(f"Vertical FOV    : {VERTICAL_FOV} degrees")
print()
print("Reference distances have been drawn.")
print("5 m, 10 m, 15 m, 20 m and 30 m")
print()
print("Press any key to close.")

cv2.imshow(
    "Calibrated Distance Reference",
    frame
)

cv2.waitKey(0)

cv2.destroyAllWindows()