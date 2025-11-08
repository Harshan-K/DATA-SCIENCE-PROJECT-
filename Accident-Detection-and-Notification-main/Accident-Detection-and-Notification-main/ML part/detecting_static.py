import os
import torch
from ultralytics import YOLO
import ultralytics  # Needed for add_safe_globals

# ----------------------------
# Setup safe globals for PyTorch
# ----------------------------
torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel])

# ----------------------------
# Load model
# ----------------------------
model_path = "shub.pt"
if not os.path.exists(model_path):
    print(f"{model_path} not found, using default yolov8n.pt model.")
    model_path = "yolov8n.pt"

model = YOLO(model_path)

# ----------------------------
# Paths
# ----------------------------
base_path = os.getcwd()
inputs_images = os.path.join(base_path, "inputs/images")
inputs_videos = os.path.join(base_path, "inputs/videos")
save_path = os.path.join(base_path, "results")

# Create results folder if not exists
os.makedirs(save_path, exist_ok=True)

# ----------------------------
# Detect all images
# ----------------------------
if os.path.exists(inputs_images):
    for img_file in os.listdir(inputs_images):
        if img_file.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(inputs_images, img_file)
            print(f"\nProcessing image: {img_file}")
            results = model.predict(source=img_path, project=save_path, save=True, show=True)
            result = results[0]
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cords = [round(x) for x in box.xyxy[0].tolist()]
                conf = round(box.conf[0].item(), 2)
                print(f"Object: {class_id} | Coordinates: {cords} | Probability: {conf}")
            print("---")

# ----------------------------
# Detect all videos
# ----------------------------
if os.path.exists(inputs_videos):
    for vid_file in os.listdir(inputs_videos):
        if vid_file.lower().endswith((".mp4", ".avi", ".mov")):
            vid_path = os.path.join(inputs_videos, vid_file)
            print(f"\nProcessing video: {vid_file}")
            results = model.predict(source=vid_path, project=save_path, save=True, show=True)
            result = results[0]
            for box in result.boxes:
                class_id = result.names[box.cls[0].item()]
                cords = [round(x) for x in box.xyxy[0].tolist()]
                conf = round(box.conf[0].item(), 2)
                print(f"Object: {class_id} | Coordinates: {cords} | Probability: {conf}")
            print("---")
