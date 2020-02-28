import os
import json
from flask import Flask, request
app = Flask(__name__)

from flask_cors import CORS, cross_origin
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/": {"origins": os.getenv('FRONTEND_BASE_URL')}})

from datetime import datetime 

import logging
if os.getenv('FLASK_DEBUG') == 'true':
  logging.basicConfig(level=logging.DEBUG) 

# import helper functions 
from helpers import missed_job, error_in_job, send_email

# APScheduler imports and config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# import event constants 
from apscheduler.events import EVENT_JOB_MISSED, EVENT_JOB_ERROR

# configure postgres jobstore
POSTGRES_URI = os.getenv('POSTGRES_URI')
jobstore = {
  'default': SQLAlchemyJobStore(url=POSTGRES_URI)
}

scheduler = BackgroundScheduler(
  jobstores=jobstore, 
  job_defaults={'misfire_grace_time': 24*60*60} # If job is missed, still execute job if it's less than 24 hours after next_run_time
) 
# add event listeners
scheduler.add_listener(missed_job, EVENT_JOB_MISSED)
scheduler.add_listener(error_in_job, EVENT_JOB_ERROR)
# start the scheduler
scheduler.start()

@app.route('/', methods=['GET', 'POST'])
@cross_origin(['Content-Type', 'application/json'])
def root ():
  if request.method == 'GET': 
    return 'ok', 200
  elif request.method == 'POST': 
    data = request.data
    email, data, template = json.loads(data).values()
    # Check that email is provided
    if email is None:
      return 'Missing email', 500
    
    # Send email with data
    response;
    if template is None:
      response = send_email(email=email, data=data)
    else:
      response = send_email(email=email, data=data, template=template);

    # Check the status code from sendgrid request
    if response.status_code < 400:
      return 'ok', 200
    else:
      return 'Something went wrong, ' + response.status_code
      

@app.route('/schedule', methods=['POST'])
@cross_origin(['Content-Type', 'application/json'])
def schedule_route ():
  if request.method == 'POST': 
    data = request.data
    email, date, data = json.loads(data).values()
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

if __name__ == '__main__': 
  app.run(host='0.0.0.0', port=os.getenv('DEFAULT_PORT') or 5000)