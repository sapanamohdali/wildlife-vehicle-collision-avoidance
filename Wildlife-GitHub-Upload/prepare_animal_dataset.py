import os
import shutil
from pathlib import Path

# ============================================================
# CREATE FINAL 1-CLASS ANIMAL DATASET
# ============================================================

PROJECT_DIR = Path("/Users/cupcake/PycharmProjects/PythonProject1")

SOURCE_DATASET = PROJECT_DIR / "dataset"
FINAL_DATASET = PROJECT_DIR / "dataset_animal"

# Original dataset class IDs
# 0 bear
# 1 deer
# 2 elephant
# 3 gaur
# 4 leopard
# 5 monkey
# 6 tiger
# 7 wild_boar

# Every wildlife class becomes simply "animal"
ANIMAL_CLASSES = {0, 1, 2, 3, 4, 5, 6, 7}


def process_split(split):
    print(f"\nProcessing {split.upper()}...")

    source_images = SOURCE_DATASET / "images" / split
    source_labels = SOURCE_DATASET / "labels" / split

    final_images = FINAL_DATASET / "images" / split
    final_labels = FINAL_DATASET / "labels" / split

    final_images.mkdir(parents=True, exist_ok=True)
    final_labels.mkdir(parents=True, exist_ok=True)

    if not source_images.exists():
        print(f"ERROR: Images folder not found:")
        print(source_images)
        return 0, 0

    if not source_labels.exists():
        print(f"ERROR: Labels folder not found:")
        print(source_labels)
        return 0, 0

    image_count = 0
    animal_annotation_count = 0

    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

    for image_path in source_images.iterdir():

        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in image_extensions:
            continue

        image_count += 1

        # Copy image
        destination_image = final_images / image_path.name
        shutil.copy2(image_path, destination_image)

        # Corresponding label
        label_path = source_labels / f"{image_path.stem}.txt"
        destination_label = final_labels / f"{image_path.stem}.txt"

        new_annotations = []

        if label_path.exists():

            with open(label_path, "r") as file:
                lines = file.readlines()

            for line in lines:

                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) != 5:
                    continue

                try:
                    class_id = int(parts[0])
                    x_center = parts[1]
                    y_center = parts[2]
                    width = parts[3]
                    height = parts[4]
                except ValueError:
                    continue

                # Any of the 8 wildlife classes becomes class 0 = animal
                if class_id in ANIMAL_CLASSES:
                    new_line = (
                        f"0 {x_center} {y_center} "
                        f"{width} {height}\n"
                    )

                    new_annotations.append(new_line)
                    animal_annotation_count += 1

        # Write label file.
        # If there is no annotation, this becomes an empty/background image.
        with open(destination_label, "w") as file:
            file.writelines(new_annotations)

    print(f"{split.upper()}: {image_count} images processed")
    print(f"{split.upper()}: {animal_annotation_count} animal annotations")

    return image_count, animal_annotation_count


def create_yaml():
    yaml_path = FINAL_DATASET / "data.yaml"

    yaml_content = f"""train: {FINAL_DATASET}/images/train
val: {FINAL_DATASET}/images/val
test: {FINAL_DATASET}/images/test

nc: 1

names:
  0: animal
"""

    with open(yaml_path, "w") as file:
        file.write(yaml_content)

    print("\nYAML created:")
    print(yaml_path)


def main():

    print("=" * 60)
    print("CREATING FINAL 1-CLASS ANIMAL DATASET")
    print("=" * 60)

    if not SOURCE_DATASET.exists():
        print("\nERROR: Original dataset not found:")
        print(SOURCE_DATASET)
        return

    # Remove old destination if it somehow exists
    if FINAL_DATASET.exists():
        print("\nRemoving previous dataset_animal...")
        shutil.rmtree(FINAL_DATASET)

    total_images = 0
    total_annotations = 0

    for split in ["train", "val", "test"]:
        images, annotations = process_split(split)
        total_images += images
        total_annotations += annotations

    create_yaml()

    print("\n" + "=" * 60)
    print("FINAL ANIMAL DATASET CREATED")
    print("=" * 60)

    print(f"\nTotal images: {total_images}")
    print(f"Total animal annotations: {total_annotations}")

    print("\nCLASS:")
    print("  0: animal")

    print("\nDataset location:")
    print(FINAL_DATASET)

    print("\nDATASET READY.")


if __name__ == "__main__":
    main()