import os
import sys
from flask import Flask, request, render_template, jsonify, flash, redirect
from werkzeug.utils import secure_filename
from twilio.rest import Client
from dotenv import load_dotenv
import torch

# Disable weights_only for PyTorch model loading
torch.serialization.add_safe_globals([
    'ultralytics.nn.tasks.DetectionModel',
    'torch.nn.modules.container.Sequential',
    'torch.nn.modules.conv.Conv2d',
    'torch.nn.modules.batchnorm.BatchNorm2d',
    'torch.nn.modules.activation.SiLU',
    'ultralytics.nn.modules.conv.Conv',
    'ultralytics.nn.modules.block.C2f',
    'ultralytics.nn.modules.head.Detect'
])

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

app = Flask(__name__, template_folder="Web Part/templates", static_folder="Web Part/static")
app.secret_key = 'accident-detection-secret-key'

# Configuration
UPLOAD_FOLDER = os.path.join("ML part", "inputs", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Create directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_whatsapp_notification(message):
    """Send WhatsApp notification using Twilio"""
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_whatsapp = os.getenv("FROM_WHATSAPP_NUMBER")
        to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")
        
        if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
            print("Missing Twilio credentials in .env file")
            return False
            
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            body=message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:+{to_whatsapp}"
        )
        
        print(f"WhatsApp message sent successfully: {message.sid}")
        return True
        
    except Exception as e:
        print(f"Error sending WhatsApp message: {str(e)}")
        return False

def detect_accident_simple(file_path):
    """Simple detection using OpenCV for demo purposes"""
    try:
        # For demo purposes, we'll simulate accident detection
        # In a real scenario, you would use your trained YOLO model here
        
        import cv2
        import random
        
        # Read the image/video
        if file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            cap = cv2.VideoCapture(file_path)
            ret, frame = cap.read()
            cap.release()
            if not ret:
                return False, []
        else:
            frame = cv2.imread(file_path)
            if frame is None:
                return False, []
        
        # Simulate accident detection based on file name or random
        filename = os.path.basename(file_path).lower()
        
        # If filename contains "accident", simulate detection
        if "accident" in filename:
            return True, [{"class": "accident", "confidence": 85.5}]
        
        # Random detection for demo (30% chance)
        if random.random() < 0.3:
            return True, [{"class": "vehicle_collision", "confidence": 72.3}]
        
        return False, []
        
    except Exception as e:
        print(f"Error in detection: {str(e)}")
        return False, []

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        if 'uploadedImage' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['uploadedImage']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # Detect accidents
            accident_detected, detection_details = detect_accident_simple(file_path)
            
            if accident_detected:
                # Send WhatsApp notification
                message = f"ACCIDENT DETECTED!\n\n"
                message += f"File: {filename}\n"
                for detail in detection_details:
                    message += f"Type: {detail['class']}\n"
                    message += f"Confidence: {detail['confidence']}%\n"
                message += f"\nImmediate attention required!"
                
                whatsapp_sent = send_whatsapp_notification(message)
                
                flash(f'Accident detected in {filename}! WhatsApp notification {"sent" if whatsapp_sent else "failed"}.')
                return render_template('home.html', 
                                     accident_detected=True, 
                                     detection_details=detection_details,
                                     filename=filename,
                                     whatsapp_sent=whatsapp_sent)
            else:
                flash(f'No accident detected in {filename}.')
                return render_template('home.html', 
                                     accident_detected=False, 
                                     filename=filename)
        else:
            flash('Invalid file type. Please upload images (PNG, JPG, JPEG) or videos (MP4, AVI, MOV).')
    
    return render_template('home.html')

@app.route('/api/detect', methods=['POST'])
def api_detect():
    """API endpoint for accident detection"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    accident_detected, detection_details = detect_accident_simple(file_path)
    
    response = {
        'accident_detected': accident_detected,
        'detection_details': detection_details,
        'filename': filename
    }
    
    if accident_detected:
        message = f"ACCIDENT DETECTED via API!\n\nFile: {filename}\n"
        for detail in detection_details:
            message += f"Type: {detail['class']}, Confidence: {detail['confidence']}%\n"
        
        whatsapp_sent = send_whatsapp_notification(message)
        response['whatsapp_sent'] = whatsapp_sent
    
    return jsonify(response)

if __name__ == '__main__':
    print("Starting Accident Detection Web Application...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print("Note: Using simplified detection for demo purposes")
    print("Files with 'accident' in name will trigger detection")
    app.run(host='0.0.0.0', port=5000, debug=True)