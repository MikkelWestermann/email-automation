import os
import json
from flask import Flask, request
app = Flask(__name__)
 
# Sendgrid imports and config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_SENDER = os.getenv('SENDGRID_SENDER')

# APScheduler imports and config
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def root (): 
  if request.method == 'GET': 
    return 'ok', 200
  elif request.method == 'POST': 
    email, date = request.get_json().values()
    if email is None or date is None:
      return 'Missing email / date', 500
    scheduler.add_job(send_email, 'date', run_date=date, args=[email])
    return 'ok', 200
    
def send_email (email): 
  print('email: ', email)
  message = Mail(
    from_email=SENDGRID_SENDER,
    to_emails=email,
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
  try:
      sg = SendGridAPIClient(SENDGRID_API_KEY)
      response = sg.send(message)
      return response
  except Exception as e: 
      print(e) 