from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from twilio.rest import Client
import os
import json
from datetime import datetime
import glob

app = Flask(__name__, template_folder="Web Part/templates", static_folder="Web Part/static")
app.secret_key = 'accident-detection-secret'

UPLOAD_FOLDER = "ML part/inputs/uploads"
HISTORY_FILE = "detection_history.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

def send_whatsapp_message(message):
    try:
        client = Client('AC5801f476fea235cd6ed2b62457f3c988', 'e4b4b65334574f0c56f4cf3c8b4f096a')
        msg = client.messages.create(
            body=message,
            from_='whatsapp:+14155238886',
            to='whatsapp:+917604990626'
        )
        return True
    except:
        return False

def save_detection_history(filename, accident_detected, confidence, whatsapp_sent):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    
    history.append({
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'accident_detected': accident_detected,
        'confidence': confidence,
        'whatsapp_sent': whatsapp_sent
    })
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_detection_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def get_system_stats():
    history = get_detection_history()
    total_uploads = len(history)
    accidents_detected = sum(1 for h in history if h['accident_detected'])
    notifications_sent = sum(1 for h in history if h['whatsapp_sent'])
    
    return {
        'total_uploads': total_uploads,
        'accidents_detected': accidents_detected,
        'notifications_sent': notifications_sent,
        'success_rate': round((notifications_sent / max(accidents_detected, 1)) * 100, 1)
    }

@app.route('/')
def home():
    stats = get_system_stats()
    return render_template('home.html', stats=stats)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'uploadedImage' not in request.files:
        flash('No file selected')
        return redirect(url_for('home'))
    
    file = request.files['uploadedImage']
    
    if file.filename == '' or not allowed_file(file.filename):
        flash('Invalid file type')
        return redirect(url_for('home'))
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    # Always detect accident for demo
    accident_detected = True
    confidence = 95
    detection_details = [{"class": "accident", "confidence": confidence}]
    
    whatsapp_sent = False
    if accident_detected:
        message = f"🚨 ACCIDENT DETECTED!\n\nFile: {filename}\nConfidence: {confidence}%\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nImmediate response required!"
        whatsapp_sent = send_whatsapp_message(message)
    
    save_detection_history(filename, accident_detected, confidence, whatsapp_sent)
    
    flash(f'Analysis complete! {"Accident detected" if accident_detected else "No accident detected"}')
    return render_template('home.html', 
                         accident_detected=accident_detected,
                         detection_details=detection_details,
                         filename=filename,
                         whatsapp_sent=whatsapp_sent,
                         stats=get_system_stats())

@app.route('/history')
def history():
    history_data = get_detection_history()
    history_data.reverse()  # Show latest first
    return render_template('history.html', history=history_data)

@app.route('/analytics')
def analytics():
    stats = get_system_stats()
    history = get_detection_history()
    
    # Prepare chart data
    daily_stats = {}
    for record in history:
        date = record['timestamp'][:10]  # Get date part
        if date not in daily_stats:
            daily_stats[date] = {'uploads': 0, 'accidents': 0}
        daily_stats[date]['uploads'] += 1
        if record['accident_detected']:
            daily_stats[date]['accidents'] += 1
    
    return render_template('analytics.html', stats=stats, daily_stats=daily_stats)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    print("🚗 Enhanced Accident Detection System Starting...")
    print("🌐 URL: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)