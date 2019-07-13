# Sendgrid imports and config
import os 
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_SENDER = os.getenv('SENDGRID_SENDER')
DEFAULT_TEMPLATE_ID = os.getenv('DEFAULT_TEMPLATE_ID')
DEFAULT_EMAIL_RECIPIENT = os.getenv('DEFAULT_EMAIL_RECIPIENT')
ERROR_EMAIL_TEMPLATE = os.getenv('ERROR_EMAIL_TEMPLATE')

def send_email (email, data, template=DEFAULT_TEMPLATE_ID): 
  message = Mail(
    from_email=SENDGRID_SENDER,
    to_emails=email)
  message.dynamic_template_data = data
  message.template_id = template
  try:
      sg = SendGridAPIClient(SENDGRID_API_KEY)
      response = sg.send(message)
      return response
  except Exception as e: 
    if not 'isErrorMail' in data:
      error_email({
        "subject": "Error when sending email",
        "email": email,
        "isErrorMail": True
        })

def error_email(data): 
  send_email(
    email=DEFAULT_EMAIL_RECIPIENT,
    data=data,
    template=ERROR_EMAIL_TEMPLATE
  )