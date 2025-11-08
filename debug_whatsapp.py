from twilio.rest import Client

def test_whatsapp_direct():
    try:
        print("Testing WhatsApp with exact credentials...")
        
        client = Client(
            account_sid, 
            auth_token
        )
        
        message = client.messages.create(
            body='DIRECT TEST: Accident detection system working!',
            from_='whatsapp:+14155238886',
            to='whatsapp:+917604990626'
        )
        
        print(f"SUCCESS: Message SID: {message.sid}")
        print(f"Status: {message.status}")
        return True
        
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False

if __name__ == "__main__":
    test_whatsapp_direct()