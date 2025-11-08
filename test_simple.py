#!/usr/bin/env python3
"""
Simple test script using yolov8n.pt model
"""

import os
import sys
from ultralytics import YOLO
import torch
import ultralytics

# Disable weights_only for model loading
os.environ['TORCH_WEIGHTS_ONLY'] = 'False'

def test_detection(file_path):
    """Test accident detection with yolov8n model"""
    
    # Use yolov8n.pt model (will download if not exists)
    model_path = os.path.join("ML part", "yolov8n.pt")
    
    print(f"Loading model: {model_path}")
    model = YOLO("yolov8n.pt")  # This will auto-download
    
    print(f"Analyzing file: {file_path}")
    
    try:
        results = model.predict(source=file_path, save=False, show=False)
        
        detection_found = False
        
        for result in results:
            if result.boxes is not None and len(result.boxes) > 0:
                detection_found = True
                print(f"\\nDetections found:")
                for box in result.boxes:
                    conf = box.conf[0].item()
                    if conf >= 0.3:  # Lower threshold for testing
                        class_id = int(box.cls[0].item())
                        class_name = result.names[class_id]
                        
                        print(f"  - Class: {class_name}")
                        print(f"  - Confidence: {round(conf * 100, 2)}%")
                        print(f"  - Coordinates: {[round(x) for x in box.xyxy[0].tolist()]}")
        
        if not detection_found:
            print("No objects detected with confidence >= 30%")
        
        return detection_found
        
    except Exception as e:
        print(f"Error in detection: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_simple.py <path_to_image_or_video>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    
    print("Simple Detection Test")
    print("=" * 30)
    
    test_detection(file_path)

if __name__ == "__main__":
    main()