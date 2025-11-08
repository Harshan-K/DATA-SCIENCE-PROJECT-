#!/usr/bin/env python3
"""
Test email notification functionality
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

def test_email():
    """Test email notification"""
    print("Testing Email Notification...")
    print("=" * 40)
    
    # Get credentials from .env
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")
    to_email = os.getenv("TO_EMAIL")
    
    print(f"From Email: {from_email}")
    print(f"To Email: {to_email}")
    print(f"SMTP Username: {smtp_username}")
    print()
    
    if not all([smtp_username, smtp_password, from_email, to_email]):
        print("ERROR: Missing email credentials in .env file")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "TEST: Accident Detection System"
        
        body = """
        TEST EMAIL FROM ACCIDENT DETECTION SYSTEM
        
        This is a test email to verify that the email notification system is working properly.
        
        If you receive this email, the accident detection system can successfully send email notifications.
        
        System Status: OPERATIONAL
        Test Time: Now
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        print("Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        print("Logging in...")
        server.login(smtp_username, smtp_password)
        
        print("Sending email...")
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print("SUCCESS: Email sent successfully!")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to send email")
        print(f"Error details: {str(e)}")
        return False

if __name__ == "__main__":
    test_email()