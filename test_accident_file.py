#!/usr/bin/env python3
"""
Test accident detection with file upload simulation
"""

import os
import shutil
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

def send_whatsapp_notification(message):
    """Send WhatsApp notification using Twilio"""
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_whatsapp = os.getenv("FROM_WHATSAPP_NUMBER")
        to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:+{to_whatsapp}"
        )
        
        print(f"SUCCESS: WhatsApp message sent! SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"ERROR: WhatsApp failed - {str(e)}")
        return False

def simulate_accident_detection():
    """Simulate accident detection workflow"""
    print("Accident Detection Simulation")
    print("=" * 40)
    
    # Check if sample image exists
    sample_image = os.path.join("ML part", "inputs", "images", "image1.jpg")
    upload_folder = os.path.join("ML part", "inputs", "uploads")
    
    if not os.path.exists(sample_image):
        print(f"Sample image not found: {sample_image}")
        return
    
    # Create upload folder if not exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Copy sample image to uploads folder with accident name
    accident_file = os.path.join(upload_folder, "accident_test.jpg")
    shutil.copy2(sample_image, accident_file)
    
    print(f"File uploaded: accident_test.jpg")
    print("Analyzing file for accidents...")
    
    # Simulate accident detection (based on filename)
    filename = "accident_test.jpg"
    if "accident" in filename.lower():
        print("ACCIDENT DETECTED!")
        
        # Simulate detection details
        detection_details = [
            {"class": "vehicle_collision", "confidence": 87.5},
            {"class": "damaged_vehicle", "confidence": 72.3}
        ]
        
        print("Detection Details:")
        for detail in detection_details:
            print(f"  - Type: {detail['class']}")
            print(f"  - Confidence: {detail['confidence']}%")
        
        # Send WhatsApp notification
        message = f"🚨 ACCIDENT DETECTED! 🚨\n\n"
        message += f"File: {filename}\n"
        for detail in detection_details:
            message += f"Type: {detail['class']}\n"
            message += f"Confidence: {detail['confidence']}%\n"
        message += f"\nImmediate attention required!\nLocation: Test Location\nTime: Now"
        
        print("\nSending WhatsApp notification...")
        whatsapp_sent = send_whatsapp_notification(message)
        
        if whatsapp_sent:
            print("✅ Complete workflow successful!")
            print("✅ File processed")
            print("✅ Accident detected")
            print("✅ WhatsApp notification sent")
        else:
            print("⚠️ Accident detected but WhatsApp failed")
    
    else:
        print("No accident detected in file")

if __name__ == "__main__":
    simulate_accident_detection()