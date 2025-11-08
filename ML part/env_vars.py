from dotenv import load_dotenv
import os

# Load .env from the same directory as this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ----------------------------
# Twilio credentials
# ----------------------------
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("FROM_WHATSAPP_NUMBER")
to_whatsapp_number = os.getenv("TO_WHATSAPP_NUMBER")

# ----------------------------
# Email credentials
# ----------------------------
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")

# ----------------------------
# Debug: confirm variables loaded
# ----------------------------
print("Loaded environment variables:")
print("TWILIO_ACCOUNT_SID =", account_sid)
print("FROM_EMAIL =", from_email)
