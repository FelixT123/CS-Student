#!/usr/bin/python3

import sys
import Adafruit_DHT
import datetime
import time
import logging
import logging.handlers as handlers
import os
import RPi.GPIO as GPIO
import zmq

SENSOR = Adafruit_DHT.DHT11
TH_PIN = 4
P_PIN = 17
DEGREE_SIGN = u'\N{DEGREE SIGN}'
BIND_URI = "tcp://*:%d" % 9909
zmq_sock = None

def read_sensors():
    obstacle = 0
    humidity, temperature = Adafruit_DHT.read(SENSOR, TH_PIN)
    date_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if GPIO.input(P_PIN):
        obstacle = 1

    if humidity is not None and temperature is not None:
        logger.debug(u'Temp={0:0.1f}{1}C  Humidity={2:0.1f}%  Obstacle={3}'.format(temperature, DEGREE_SIGN, humidity, obstacle))
        zmq_sock.send_json({'time': date_time, 'celsius': temperature, 'humidity': humidity, 'obstacle': obstacle})
    else:
        logger.debug(u'Obstacle={0}'.format(obstacle))
        zmq_sock.send_json({'time': date_time, 'obstacle': obstacle})

def log_setup():
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    if not os.path.exists('logs'):
        os.makedirs('logs')
    dirname = os.path.dirname(__file__)
    log_file_name = os.path.join(dirname, 'logs/tempHumidity.log')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log_handler = handlers.TimedRotatingFileHandler(log_file_name, when='midnight', interval=1, backupCount=90)
    log_handler.setLevel(logging.DEBUG)
    log_handler.setFormatter(formatter)

    logger.addHandler(log_handler)

def photoelectric_sensor_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(P_PIN, GPIO.IN)

def zmq_setup():
    global zmq_sock
    zmq_context = zmq.Context()
    zmq_sock = zmq_context.socket(zmq.PUB)
    zmq_sock.set_hwm(1)
    zmq_sock.bind(BIND_URI)

try:
    logger = logging.getLogger(__name__)
    log_setup()
    logger.info('Program started')

    zmq_setup()
    photoelectric_sensor_setup()

    while True:
        read_sensors()
        time.sleep(1)
except KeyboardInterrupt:
    logger.info('Program terminated manually')
except Exception as e:
    logger.error('Program terminated unexpectedly: %s' % e)