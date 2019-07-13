from .jobs import error_email

import logging 
logger = logging.getLogger(__name__)

def missed_job(event):
  logger.debug('*Missed Job*')
  logger.debug(event)
  error_email(data={
    "subject": "A scheduled job was missed"
  })

def error_in_job(event): 
  logger.debug('*An error occurred in job*')
  logger.debug(event)
  error_email(data={
    "subject": "An error occurred in a scheduled job"
  })
