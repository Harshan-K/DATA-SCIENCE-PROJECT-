from twilio.rest import Client

def test_whatsapp_direct():
    try:
        print("Testing WhatsApp with exact credentials...")
        
        client = Client(
            'AC5801f476fea235cd6ed2b62457f3c988', 
            'e4b4b65334574f0c56f4cf3c8b4f096a'
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