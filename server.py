from flask import Flask 
from flask_apscheduler import APScheduler
 
import time

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

@app.route('/')
def root (): 
  return 'Hello World!'