import os

# ====== CONFIGURATION ======
# תיקיות התמונות הקיימות
train_images_dir = "dataset/Data/images/train"
val_images_dir = "dataset/Data/images/val"

# תיקיות יעד ל-YOLO labels
train_labels_dir = "dataset/Data/labels/train"
val_labels_dir = "dataset/Data/labels/val"

# יצירת התיקיות אם לא קיימות
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# class_id (אם יש רק סוג אחד של אובייקט)
class_id = 0

# bounding box מלא (x_center, y_center, width, height)
bbox = (0.5, 0.5, 1.0, 1.0)

# ====== FUNCTION TO CREATE LABELS ======
def create_labels(images_dir, labels_dir):
    for img_name in os.listdir(images_dir):
        if not img_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        txt_path = os.path.join(labels_dir, img_name.rsplit('.',1)[0] + ".txt")
        x, y, w, h = bbox
        with open(txt_path, "w") as f:
            f.write(f"{class_id} {x} {y} {w} {h}\n")

# ====== CREATE LABELS FOR TRAIN AND VAL ======
create_labels(train_images_dir, train_labels_dir)
create_labels(val_images_dir, val_labels_dir)

print("✅ YOLO label files created for all images!")
