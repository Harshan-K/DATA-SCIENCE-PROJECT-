#!/usr/bin/env python3
"""
Test WhatsApp notification functionality
"""

import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join("ML part", ".env"))

def test_whatsapp():
    """Test WhatsApp notification"""
    print("Testing WhatsApp Notification...")
    print("=" * 40)
    
    # Get credentials from .env
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_whatsapp = os.getenv("FROM_WHATSAPP_NUMBER")
    to_whatsapp = os.getenv("TO_WHATSAPP_NUMBER")
    
    print(f"Account SID: {account_sid[:10]}..." if account_sid else "Account SID: Not found")
    print(f"Auth Token: {auth_token[:10]}..." if auth_token else "Auth Token: Not found")
    print(f"From Number: {from_whatsapp}")
    print(f"To Number: {to_whatsapp}")
    print()
    
    if not all([account_sid, auth_token, from_whatsapp, to_whatsapp]):
        print("ERROR: Missing Twilio credentials in .env file")
        print("Please check your ML part/.env file")
        return False
    
    try:
        client = Client(account_sid, auth_token)
        
        test_message = "TEST: Accident Detection System is working! This is a test message from your accident detection app."
        
        print("Sending test message...")
        message = client.messages.create(
            body=test_message,
            from_=f"whatsapp:{from_whatsapp}",
            to=f"whatsapp:{to_whatsapp}"
        )
        
        print(f"SUCCESS: WhatsApp message sent!")
        print(f"Message SID: {message.sid}")
        print(f"Status: {message.status}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to send WhatsApp message")
        print(f"Error details: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp()