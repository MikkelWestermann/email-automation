import logging 
logger = logging.getLogger(__name__)
def missed_job(event):
  logger.debug('*Missed Job*')
  logger.debug(event)

def error_in_job(event): 
  logger.debug('*An error occurred in job*')
  logger.debug(event)
