# convert_vizwiz_to_yolo.py
import os
import json
import shutil
import kagglehub

# ---------------------------
# 1. הורדת VizWiz
# ---------------------------
def download_vizwiz(dataset_name="ingbiodanielh/vizwiz"):
    dataset_path = os.path.join("datasets", "vizwiz")
    if not os.path.exists(dataset_path):
        print("Downloading VizWiz dataset...")
        kagglehub.dataset_download(dataset_name)
    else:
        print("VizWiz already exists.")
    return dataset_path


# translate to YOLO

def convert_to_yolo(dataset_path, output_dir="data"):
    train_json = os.path.join(dataset_path, "train.json")  # by structre of VizWiz
    if not os.path.exists(train_json):
        raise FileNotFoundError(f"Train JSON not found: {train_json}")

    #create YOLO
    image_dir = os.path.join(output_dir, "train", "images")
    label_dir = os.path.join(output_dir, "train", "labels")
    os.makedirs(image_dir, exist_ok=True)
    os.makedirs(label_dir, exist_ok=True)

    with open(train_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        # הנתיב של התמונה
        image_src = item.get("image_path")  # ודא שזה הקובץ המקומי של התמונה
        if not image_src or not os.path.exists(image_src):
            continue

        # העתקת תמונה ל-YOLO
        image_name = os.path.basename(image_src)
        dest_image_path = os.path.join(image_dir, image_name)
        shutil.copy(image_src, dest_image_path)

        # יצירת קובץ label
        label_path = os.path.join(label_dir, image_name.replace(".jpg", ".txt"))
        with open(label_path, "w", encoding="utf-8") as f:
            # כאן דוגמה בסיסית: כל bbox = [class_id x_center y_center width height]
            for ann in item.get("annotations", []):
                cls_id = 0  # אם יש לך כמה קטגוריות אפשר למפות לפי מיפוי
                x, y, w, h = ann["bbox"]  # ודא שהפורמט מתאים VizWiz
                # המרה ל-YOLO: (x_center, y_center, width, height) יחסית לתמונה
                img_w, img_h = item.get("width"), item.get("height")
                x_center = (x + w/2) / img_w
                y_center = (y + h/2) / img_h
                w_rel = w / img_w
                h_rel = h / img_h
                f.write(f"{cls_id} {x_center} {y_center} {w_rel} {h_rel}\n")

    print("YOLO conversion completed!")


# 3. the main function to run the conversion
def prepare_dataset():
    dataset_path = download_vizwiz()
    convert_to_yolo(dataset_path)



if __name__ == "__main__":
    prepare_dataset()
