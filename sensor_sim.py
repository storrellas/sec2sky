import paho.mqtt.client as mqtt
import time
import json
import signal
from random import randint
from sec2sky import utils

logger = utils.get_logger()

import os
# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sec2sky.settings")
import django
django.setup()

from django.conf import settings

# Configuration values
sensor_id = 1
response_delay = 3
topic = 'sensor'

#
# Name: on_connect
# Description: Handler when a connect is reached
#
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))

#
# Name: on_message
# Description: Handler when a message is received
#
def on_message(client, userdata, msg):
    logger.info("topic: '" + msg.topic + "'' payload: '" + str(msg.payload) + "'")

#
# Name: alarm_handler
# Description: Handler when alarm is raised
#
def alarm_handler(signum, frame):
    #logger.info('Signal handler called with signal' + str(signum) )

    message = {'id': 1, 'sender': 'sergi'}

    # MQTT publish message
    logger.info("Sending message '" + json.dumps(message) + "' ...")
    client.publish(topic, json.dumps(message))

    # Create signal for next alarm
    signal.alarm(randint(1, 10))

if __name__ == "__main__":

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(1)

    # Configure MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()
