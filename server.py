import os
import json
from flask import Flask, request
app = Flask(__name__)

from datetime import datetime 
 
# Sendgrid imports and config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SENDGRID_SENDER = os.getenv('SENDGRID_SENDER')
DEFAULT_TEMPLATE_ID = os.getenv('DEFAULT_TEMPLATE_ID')

# APScheduler imports and config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from helpers import missed_job, error_in_job
POSTGRES_URI = os.getenv('POSTGRES_URI')
jobstore = {
  'default': SQLAlchemyJobStore(url=POSTGRES_URI)
}
scheduler = BackgroundScheduler(
  jobstores=jobstore, 
  job_defaults={'misfire_grace_period': 24*60*60} # If job is missed, still execute job if it's less than 24 hours after next_run_time
) 
scheduler.add_listener(missed_job, 'EVENT_JOB_MISSED')
scheduler.add_listener(error_in_job, 'EVENT_JOB_ERROR')
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
def root (): 
  if request.method == 'GET': 
    return 'ok', 200
  elif request.method == 'POST': 
    email, date, data = request.get_json().values()
    # Check that email and date is provided
    if email is None or date is None:
      return 'Missing email / date', 500
    # Format the provided date to ISO8601
    py_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ').isoformat()
    # Check that the provided date has not already happened
    if py_date < datetime.now().isoformat(): 
      return 'Date has already happened', 500
    # Add send email job to schedule
    scheduler.add_job(send_email, 'date', run_date=py_date, args=[email, data])
    return 'ok', 200
    
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

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=os.getenv('DEFAULT_PORT') or 5000)