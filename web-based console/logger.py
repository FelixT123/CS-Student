import logging
import os
from logging.handlers import TimedRotatingFileHandler

def getLogger(name):
  # Create logs directory if it doesn't exist
  if not os.path.exists('logs'):
    os.makedirs('logs')

  # specifying the log file's name as "logs/logfile" and rotating the log file at midnight each day.
  logHandler = TimedRotatingFileHandler(filename="logs/logfile", when="midnight")
  logFormatter = logging.Formatter('[%(asctime)s][%(name)-14s][%(levelname)-8s] %(message)s')
  logHandler.setFormatter(logFormatter)

  # display the log messages on the console.
  consoleHandler = logging.StreamHandler()
  consoleHandler.setFormatter(logFormatter)

  logger = logging.getLogger(name)
  
  # there are two handlers: logHandler and consoleHandler
  logger.addHandler(logHandler)
  logger.addHandler(consoleHandler)
  logger.setLevel(logging.INFO)  
  logger.setLevel(logging.DEBUG)

  return logger

