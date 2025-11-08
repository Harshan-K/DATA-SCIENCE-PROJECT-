import os
from flask import Flask, request, render_template, flash, redirect
from werkzeug.utils import secure_filename
from twilio.rest import Client
from dotenv import load_dotenv
import cv2

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

app = Flask(__name__, template_folder="Web Part/templates", static_folder="Web Part/static")
app.secret_key = 'accident-detection-key'

# Configuration
UPLOAD_FOLDER = os.path.join("ML part", "inputs", "uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def send_whatsapp_notification(message):
    try:
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        from_whatsapp = "+14155238886"
        to_whatsapp = "+917604990626"
        
        print(f"Sending to: {to_whatsapp}")
        
        client = Client(account_sid, auth_token)
        
        msg = client.messages.create(
            body=message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:{to_whatsapp}"
        )
        
        print(f"SUCCESS: Message sent! SID: {msg.sid}")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def detect_accident(file_path):
    try:
        # Read file to verify it exists
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
        
        # Always detect accident for testing
        return True, [{"class": "accident", "confidence": 95.0}]
        
    except Exception as e:
        print(f"Detection error: {str(e)}")
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
            
            print(f"File saved: {file_path}")
            
            # Detect accidents
            accident_detected, detection_details = detect_accident(file_path)
            
            print(f"Accident detected: {accident_detected}")
            
            if accident_detected:
                # Send WhatsApp notification
                message = f"ACCIDENT DETECTED!\n\nFile: {filename}\nConfidence: 95%\nTime: Now\nAction Required: Immediate Response"
                
                print("Sending WhatsApp...")
                whatsapp_sent = send_whatsapp_notification(message)
                
                flash(f'ACCIDENT DETECTED in {filename}! WhatsApp {"SENT" if whatsapp_sent else "FAILED"}')
                return render_template('home.html', 
                                     accident_detected=True, 
                                     detection_details=detection_details,
                                     filename=filename,
                                     whatsapp_sent=whatsapp_sent)
            else:
                flash(f'No accident detected in {filename}')
                return render_template('home.html', 
                                     accident_detected=False, 
                                     filename=filename)
        else:
            flash('Invalid file type')
    
    return render_template('home.html')

if __name__ == '__main__':
    print("ACCIDENT DETECTION SYSTEM STARTING...")
    print("WhatsApp notifications: ENABLED")
    print("Open: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)