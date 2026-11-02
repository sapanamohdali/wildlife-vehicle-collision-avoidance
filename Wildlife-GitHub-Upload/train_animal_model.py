from pathlib import Path
import torch
from ultralytics import YOLO

# ============================================================
# FINAL ANIMAL DETECTOR TRAINING
# ============================================================

PROJECT_DIR = Path("/Users/cupcake/PycharmProjects/PythonProject1")

DATASET = PROJECT_DIR / "dataset_animal" / "data.yaml"
MODEL = PROJECT_DIR / "yolo26n.pt"

# ------------------------------------------------------------
# Select device
# ------------------------------------------------------------

if torch.backends.mps.is_available():
    DEVICE = "mps"
else:
    DEVICE = "cpu"

print("=" * 60)
print("FINAL ANIMAL DETECTOR TRAINING")
print("=" * 60)

print(f"\nDevice: {DEVICE}")
print(f"\nDataset:")
print(DATASET)

print("\nClass:")
print("0 = animal")

# ------------------------------------------------------------
# Check files
# ------------------------------------------------------------

if not DATASET.exists():
    raise FileNotFoundError(
        f"Dataset YAML not found:\n{DATASET}"
    )

if not MODEL.exists():
    raise FileNotFoundError(
        f"YOLO model not found:\n{MODEL}"
    )

# ------------------------------------------------------------
# Load pretrained YOLO model
# ------------------------------------------------------------

print("\nLoading YOLO26n pretrained model...")

model = YOLO(str(MODEL))

print("Model loaded successfully.")

# ------------------------------------------------------------
# Train
# ------------------------------------------------------------

print("\nStarting training...")
print("Do not run another training script at the same time.")

results = model.train(
    data=str(DATASET),

    epochs=8,
    imgsz=640,
    batch=4,

    device=DEVICE,

    workers=2,

    patience=4,

    pretrained=True,

    augment=True,

    project=str(PROJECT_DIR / "runs"),
    name="animal_detector",

    exist_ok=True,

    save=True,
    val=True,
    plots=True,

    verbose=True
)

# ------------------------------------------------------------
# Finished
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("ANIMAL DETECTOR TRAINING FINISHED")
print("=" * 60)

print("\nBest model should be located at:")

print(
    PROJECT_DIR
    / "runs"
    / "animal_detector"
    / "weights"
    / "best.pt"
)