import os
import sys
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import torch
from ultralytics import YOLO
import ultralytics
from twilio.rest import Client
from dotenv import load_dotenv
import cv2
from PIL import Image

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

app = Flask(__name__, template_folder="Web Part/templates", static_folder="Web Part/static")
app.secret_key = 'your-secret-key-here'

# Setup safe globals for PyTorch
torch.serialization.add_safe_globals([ultralytics.nn.tasks.DetectionModel])

# Configuration
UPLOAD_FOLDER = os.path.join("ML part", "inputs", "uploads")
RESULTS_FOLDER = os.path.join("ML part", "results")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Load YOLO model
model_path = os.path.join("ML part", "best.pt")
if not os.path.exists(model_path):
    model_path = os.path.join("ML part", "yolov8n.pt")
    if not os.path.exists(model_path):
        print("No model found. Please ensure best.pt or yolov8n.pt is in the ML part folder.")
        sys.exit(1)

model = YOLO(model_path)

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

def detect_accident(file_path):
    """Detect accidents in uploaded file"""
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
                            'confidence': round(conf * 100, 2)
                        })
                        
                        accident_detected = True
        
        return accident_detected, detection_details
        
    except Exception as e:
        print(f"Error in accident detection: {str(e)}")
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
            accident_detected, detection_details = detect_accident(file_path)
            
            if accident_detected:
                # Send WhatsApp notification
                message = f"🚨 ACCIDENT DETECTED! 🚨\n\n"
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
    
    accident_detected, detection_details = detect_accident(file_path)
    
    response = {
        'accident_detected': accident_detected,
        'detection_details': detection_details,
        'filename': filename
    }
    
    if accident_detected:
        message = f"🚨 ACCIDENT DETECTED via API! 🚨\n\nFile: {filename}\n"
        for detail in detection_details:
            message += f"Type: {detail['class']}, Confidence: {detail['confidence']}%\n"
        
        whatsapp_sent = send_whatsapp_notification(message)
        response['whatsapp_sent'] = whatsapp_sent
    
    return jsonify(response)

if __name__ == '__main__':
    print("Starting Accident Detection Web Application...")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Model path: {model_path}")
    app.run(host='0.0.0.0', port=5000, debug=True)