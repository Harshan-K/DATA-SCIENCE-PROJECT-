#!/usr/bin/env python3
"""
Simple script to test accident detection on a single file
Usage: python test_detection.py <path_to_image_or_video>
"""

import sys
import os
from ultralytics import YOLO
import torch
import ultralytics
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

# Setup safe globals for PyTorch
torch.serialization.add_safe_globals([
    ultralytics.nn.tasks.DetectionModel,
    torch.nn.modules.container.Sequential,
    torch.nn.modules.conv.Conv2d,
    torch.nn.modules.batchnorm.BatchNorm2d,
    torch.nn.modules.activation.SiLU,
    torch.nn.modules.pooling.AdaptiveAvgPool2d,
    torch.nn.modules.linear.Linear,
    torch.nn.modules.dropout.Dropout
])

def send_whatsapp_notification(message):
    """Send WhatsApp notification using Twilio"""
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_whatsapp = os.getenv("FROM_WHATSAPP_NUMBER")
        to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")
        
        if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
            print("ERROR: Missing Twilio credentials in .env file")
            return False
            
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:+{to_whatsapp}"
        )
        
        print(f"SUCCESS: WhatsApp message sent successfully: {message.sid}")
        return True
        
    except Exception as e:
        print(f"ERROR: Error sending WhatsApp message: {str(e)}")
        return False

def detect_accident(file_path):
    """Detect accidents in the given file"""
    # Load model
    model_path = os.path.join("ML part", "best.pt")
    if not os.path.exists(model_path):
        model_path = os.path.join("ML part", "yolov8n.pt")
        if not os.path.exists(model_path):
            print("ERROR: No model found. Please ensure best.pt or yolov8n.pt is in the ML part folder.")
            return False, []
    
    print(f"Loading model: {model_path}")
    model = YOLO(model_path)
    
    print(f"Analyzing file: {file_path}")
    
    try:
        results = model.predict(source=file_path, save=False, show=False)
        
        accident_detected = False
        detection_details = []
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    conf = box.conf[0].item()
                    if conf >= 0.5:  # Confidence threshold
                        class_id = int(box.cls[0].item())
                        class_name = result.names[class_id] if class_id in result.names else "Unknown"
                        
                        detection_details.append({
                            'class': class_name,
                            'confidence': round(conf * 100, 2),
                            'coordinates': [round(x) for x in box.xyxy[0].tolist()]
                        })
                        
                        accident_detected = True
        
        return accident_detected, detection_details
        
    except Exception as e:
        print(f"ERROR: Error in accident detection: {str(e)}")
        return False, []

def main():
    if len(sys.argv) != 2:
        print("Usage: python test_detection.py <path_to_image_or_video>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    
    print("Accident Detection Test")
    print("=" * 50)
    
    accident_detected, detection_details = detect_accident(file_path)
    
    if accident_detected:
        print("ACCIDENT DETECTED!")
        print(f"File: {os.path.basename(file_path)}")
        print("\nDetection Details:")
        
        for i, detail in enumerate(detection_details, 1):
            print(f"  {i}. Type: {detail['class']}")
            print(f"     Confidence: {detail['confidence']}%")
            print(f"     Coordinates: {detail['coordinates']}")
        
        # Send WhatsApp notification
        message = f"ACCIDENT DETECTED!\n\n"
        message += f"File: {os.path.basename(file_path)}\n"
        for detail in detection_details:
            message += f"Type: {detail['class']}\n"
            message += f"Confidence: {detail['confidence']}%\n"
        message += f"\nImmediate attention required!"
        
        print("\nSending WhatsApp notification...")
        whatsapp_sent = send_whatsapp_notification(message)
        
        if not whatsapp_sent:
            print("WARNING: WhatsApp notification failed - check your .env configuration")
    
    else:
        print("No accident detected")
        print(f"File: {os.path.basename(file_path)}")
        print("The file appears to be safe with no accidents detected.")

if __name__ == "__main__":
    main()