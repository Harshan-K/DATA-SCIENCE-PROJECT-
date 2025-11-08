# Traffic And Accident Detection System ⚠️🚗💥

A comprehensive accident detection system that automatically detects accidents in uploaded images/videos and sends WhatsApp notifications to emergency contacts. Built with YOLOv8, Flask, and Twilio.

## Features

- 🚗 **Real-time Accident Detection** using YOLOv8 model
- 📱 **WhatsApp Notifications** via Twilio API
- 🌐 **Web Interface** for easy file uploads
- 📊 **API Endpoint** for programmatic access
- 🎯 **High Accuracy** with confidence threshold filtering
- 📁 **Multiple File Formats** (Images: JPG, PNG, GIF | Videos: MP4, AVI, MOV)

## Quick Start

### Option 1: Easy Setup (Windows)
```bash
# Simply run the batch file
run.bat
```

### Option 2: Easy Setup (Linux/Mac)
```bash
# Make script executable and run
chmod +x run.sh
./run.sh
```

### Option 3: Manual Setup

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure WhatsApp notifications:**
   - Edit `ML part/.env` file with your Twilio credentials
   - Get credentials from [Twilio Console](https://console.twilio.com/)

4. **Start the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   - Navigate to `http://localhost:5000`

## Configuration

Update the `ML part/.env` file with your credentials:

```env
# Twilio WhatsApp Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
FROM_WHATSAPP_NUMBER=+14155238886
TO_WHATSAPP_NUMBER=your_phone_number

# Email Configuration (optional)
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=recipient@gmail.com
```

## Usage

### Web Interface
1. Open `http://localhost:5000` in your browser
2. Upload an image or video file
3. Click "Detect Accidents"
4. View results and WhatsApp notification status

### Command Line Testing
```bash
# Test a specific file
python test_detection.py "path/to/your/file.jpg"
```

### API Usage
```bash
# POST request to detect accidents
curl -X POST -F "file=@your_image.jpg" http://localhost:5000/api/detect
```

## Project Structure

```
Accident-Detection-and-Notification-Camera/
├── app.py                 # Main Flask application
├── test_detection.py      # Command-line testing script
├── run.bat               # Windows startup script
├── run.sh                # Linux/Mac startup script
├── requirements.txt      # Python dependencies
├── ML part/
│   ├── .env             # Environment variables
│   ├── best.pt          # Trained YOLO model
│   ├── inputs/uploads/  # Uploaded files
│   └── results/         # Detection results
└── Web Part/
    ├── templates/       # HTML templates
    └── static/         # CSS, JS, images
```

## Model Information

- **Primary Model:** `best.pt` (custom trained model)
- **Fallback Model:** `yolov8n.pt` (default YOLOv8 nano)
- **Confidence Threshold:** 50%
- **Supported Classes:** Accident detection classes

## Troubleshooting

### Common Issues

1. **Model not found:**
   - Ensure `best.pt` or `yolov8n.pt` exists in `ML part/` folder

2. **WhatsApp notifications not working:**
   - Verify Twilio credentials in `.env` file
   - Check phone number format (+country_code)
   - Ensure Twilio WhatsApp sandbox is configured

3. **File upload errors:**
   - Check file format (supported: JPG, PNG, GIF, MP4, AVI, MOV)
   - Ensure `ML part/inputs/uploads/` directory exists

### Getting Twilio Credentials

1. Sign up at [Twilio](https://www.twilio.com/)
2. Go to Console Dashboard
3. Find Account SID and Auth Token
4. Set up WhatsApp Sandbox
5. Get WhatsApp phone number

## API Reference

### POST /api/detect

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (image or video)

**Response:**
```json
{
  "accident_detected": true,
  "detection_details": [
    {
      "class": "accident",
      "confidence": 85.5
    }
  ],
  "filename": "test.jpg",
  "whatsapp_sent": true
}
```

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please check the troubleshooting section or create an issue in the repository.



## run 
python app_final.py then go to http://localhost:5000 to use it.
