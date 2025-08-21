import os
import zipfile
import subprocess
import shutil
import random

# Base path of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Raw dataset path
DATASET_RAW = os.path.join(BASE_DIR, "dataset_vizwiz")
# YOLO images path
YOLO_IMAGES = os.path.join(BASE_DIR, "images")

# Kaggle dataset identifier
KAGGLE_DATASET = "jackpoison/vizwiz"

def download_and_extract():
    zip_path = os.path.join(BASE_DIR, "vizwiz.zip")

    # Download from Kaggle if not already downloaded
    if not os.path.exists(zip_path):
        print("📥 Downloading VizWiz dataset from Kaggle...")
        subprocess.run(["kaggle", "datasets", "download", "-d", KAGGLE_DATASET, "-p", BASE_DIR])
    else:
        print("✔ Dataset already downloaded")

    # Extract files
    if not os.path.exists(DATASET_RAW):
        os.makedirs(DATASET_RAW)

    print(" Extracting files...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATASET_RAW)

    print(" Done downloading and extracting")

def prepare_yolo_split(train_ratio=0.8):
    """
    Split images into YOLO format: train/ and val/
    """
    # You may need to adjust the path depending on how VizWiz is structured
    images_dir = os.path.join(DATASET_RAW, "train")  
    if not os.path.exists(images_dir):
        raise RuntimeError("❌ Could not find an 'images' folder inside dataset")


    # Collect all images
    all_images = [f for f in os.listdir(images_dir) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

    random.shuffle(all_images)
    split_idx = int(len(all_images) * train_ratio)

    train_files = all_images[:split_idx]
    val_files = all_images[split_idx:]

    # Copy images to YOLO folders
    for fname in train_files:
        shutil.copy(os.path.join(images_dir, fname), os.path.join(YOLO_IMAGES, "train", fname))

    for fname in val_files:
        shutil.copy(os.path.join(images_dir, fname), os.path.join(YOLO_IMAGES, "val", fname))

    print(f"✅ Moved {len(train_files)} images to train and {len(val_files)} images to val")

if __name__ == "__main__":
    download_and_extract()
    prepare_yolo_split()
