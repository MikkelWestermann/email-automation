# Sendgrid imports and config
import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_SENDER = os.getenv('SENDGRID_SENDER')
DEFAULT_TEMPLATE_ID = os.getenv('DEFAULT_TEMPLATE_ID')

def send_email (email, data): 
  message = Mail(
    from_email=SENDGRID_SENDER,
    to_emails=email)
  message.dynamic_template_data = data
  message.template_id = DEFAULT_TEMPLATE_ID
  try:
      sg = SendGridAPIClient(SENDGRID_API_KEY)
      response = sg.send(message)
      return response
  except Exception as e: 
      print(e) 