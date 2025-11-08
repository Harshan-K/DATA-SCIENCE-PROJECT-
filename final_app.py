from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from twilio.rest import Client
import os

app = Flask(__name__, template_folder="Web Part/templates", static_folder="Web Part/static")
app.secret_key = 'accident-detection-secret'

UPLOAD_FOLDER = "ML part/inputs/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

def send_whatsapp_message(message):
    try:
        print(f"Attempting to send WhatsApp message...")
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        
        msg = client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',
            to='whatsapp:+917604990626'
        )
        
        print(f"WhatsApp message sent successfully! SID: {msg.sid}")
        return True
        
    except Exception as e:
        print(f"WhatsApp sending failed: {str(e)}")
        return False

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print("Form submitted!")
        
        # Check if file is in request
        if 'uploadedImage' not in request.files:
            print("No file part in request")
            flash('No file selected')
            return redirect(url_for('home'))
        
        file = request.files['uploadedImage']
        print(f"File received: {file.filename}")
        
        # Check if file is selected
        if file.filename == '':
            print("No file selected")
            flash('No file selected')
            return redirect(url_for('home'))
        
        # Check if file is allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            print(f"File saved to: {file_path}")
            
            # ALWAYS detect accident for testing
            print("Detecting accident...")
            accident_detected = True
            detection_details = [{"class": "accident", "confidence": 95}]
            
            if accident_detected:
                print("Accident detected! Sending WhatsApp...")
                
                # Create WhatsApp message
                message = f"🚨 ACCIDENT DETECTED! 🚨\n\nFile: {filename}\nConfidence: 95%\nTime: Now\nLocation: Test Location\n\nImmediate response required!"
                
                # Send WhatsApp
                whatsapp_sent = send_whatsapp_message(message)
                
                print(f"WhatsApp sent: {whatsapp_sent}")
                
                flash(f'Accident detected in {filename}! WhatsApp notification {"SENT" if whatsapp_sent else "FAILED"}')
                
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
            print("Invalid file type")
            flash('Invalid file type. Please upload JPG, PNG, GIF, MP4, AVI, or MOV files.')
            return redirect(url_for('home'))
    
    return render_template('home.html')

if __name__ == '__main__':
    print("=" * 60)
    print("🚗 ACCIDENT DETECTION SYSTEM")
    print("=" * 60)
    print("📱 WhatsApp: ENABLED")
    print("🌐 URL: http://localhost:5000")
    print("📁 Upload folder:", UPLOAD_FOLDER)
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)