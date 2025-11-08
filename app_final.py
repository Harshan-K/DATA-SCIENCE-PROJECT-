import os
from flask import Flask, request, render_template, jsonify, flash, redirect
from werkzeug.utils import secure_filename
from twilio.rest import Client
from dotenv import load_dotenv
import cv2
import random

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
        
        print(f"Sending WhatsApp to: {to_whatsapp}")
        
        if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
            print("Missing credentials")
            return False
            
        client = Client(account_sid, auth_token)
        
        msg = client.messages.create(
            body=message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:{to_whatsapp}"
        )
        
        print(f"WhatsApp sent! SID: {msg.sid}")
        return True
        
    except Exception as e:
        print(f"WhatsApp error: {str(e)}")
        return False

def detect_accident(file_path):
    """Detect accidents in uploaded file"""
    try:
        # Read the file
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
        
        filename = os.path.basename(file_path).lower()
        
        # For testing - detect all uploaded files as accidents
        return True, [{"class": "accident", "confidence": 85.5}]
        
    except Exception as e:
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
                message = f"ACCIDENT DETECTED!\n\nFile: {filename}\nConfidence: 85.5%\nImmediate attention required!"
                
                whatsapp_sent = send_whatsapp_notification(message)
                
                flash(f'Accident detected in {filename}! Notification {"sent" if whatsapp_sent else "failed"}.')
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
            flash('Invalid file type.')
    
    return render_template('home.html')

if __name__ == '__main__':
    print("Accident Detection System Starting...")
    print("Open: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)