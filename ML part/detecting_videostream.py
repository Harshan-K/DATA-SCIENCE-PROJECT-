import os
from ultralytics import YOLO
import cv2

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the model
model_path = os.path.join(BASE_DIR, "best.pt")
model = YOLO(model_path)

# Frame dimensions
frame_width = 640
frame_height = 480

# Video stream URL
stream_url = "http://kamera.mikulov.cz:8888/mjpg/video.mjpg"

# Create temp folder if it doesn't exist
temp_dir = os.path.join(BASE_DIR, "temp")
os.makedirs(temp_dir, exist_ok=True)
temp_image_path = os.path.join(temp_dir, "temp.jpg")

# Start capturing video stream
cap = cv2.VideoCapture(stream_url)

while cap.isOpened():
    is_frame, frame = cap.read()
    if not is_frame:
        break

    resized_frame = cv2.resize(frame, (frame_width, frame_height))
    cv2.imwrite(temp_image_path, resized_frame)

    # Perform object detection
    model.predict(source=temp_image_path, show=True)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
