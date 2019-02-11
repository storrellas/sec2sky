import sys
import os
import io
import traceback
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import time
import json
import signal

# Libraries import
import paho.mqtt.client as mqtt

# Import Django
import django
from django.conf import settings

# Project imports
from random import randint
from sec2sky import utils


logger = utils.get_logger()

# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sec2sky.settings")
django.setup()

from rest_framework.parsers import JSONParser
from api.serializers import *
from api.models import *

# Global variables
sensor_discovery = {}
sensor_discovery_period =  3

#
# Name: on_connect
# Description: Handler when a connect is reached
#
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))

    # Subscribe to topic list
    # logger.info("Subscribe to topic "+ settings.MQTT['topic_dronetrap'])
    # client.subscribe(settings.MQTT['topic_dronetrap'])

    logger.info("Subscribe to topic "+ settings.MQTT['topic_start_discovery'])
    client.subscribe(settings.MQTT['topic_start_discovery'])
    logger.info("Subscribe to topic "+ settings.MQTT['topic_manager_set'])
    client.subscribe(settings.MQTT['topic_manager_set'])
    logger.info("Subscribe to topic "+ settings.MQTT['topic_manager_unset'])
    client.subscribe(settings.MQTT['topic_manager_unset'])


#
# Name: on_message
# Description: Handler when a message is received
#
def on_message(client, userdata, msg):
    logger.info("topic: '" + msg.topic + "'' payload: '" + str(msg.payload) + "'")

    try:

        # Deserialize JSON
        stream = io.BytesIO(msg.payload)
        data = JSONParser().parse(stream)

        # Parse topic
        # sensor_id = msg.topic.split("/")[1]
        # command = msg.topic.split("/")[2]
        # if len(msg.topic.split("/")) > 3:
        #     subcommand =  msg.topic.split("/")[3]
        deviceid = msg.topic.split("/")[1]
        command = msg.topic.split("/")[2]

        # Treat topic
        if command == "start_discovery":
            logger.info("Start Discovery received")

            # Store new sensor to perform discovery
            deviceid = data['deviceid']
            if deviceid in sensor_discovery.keys():
                sensor_discovery[deviceid] = data

        elif command == "set":
            logger.info("State manager/set received")
            sensor_discovery.pop(deviceid)
        elif command == "unset":
            logger.info("State manager/unset received")
        elif command == "state":
            logger.info("State received")
        elif command == "detection":
            logger.info("Detection received")
        else:
            logger.error("topic not recognised")

    except Exception as e:
        logger.error('Exception: '+ str(e))
        traceback.print_exc()

#
# Name: alarm_handler
# Description: Handler when alarm is raised
#
def alarm_handler(signum, frame):
    #logger.info('Signal handler called with signal ' + str(signum) )

    # MQTT publish message
    if len(sensor_discovery) > 0:
        logger.info("Sending message sensor discoveries pending ...")
        for device_id in sensor_discovery:
            topic = 'dronetrap/discovery'
            client.publish(topic, json.dumps(sensor_discovery[device_id]))

    # Create signal for next alarm
    #signal.alarm(randint(1, 10))
    signal.alarm(sensor_discovery_period)

if __name__ == "__main__":

    # Set the signal handler and a 5-second alarm
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(sensor_discovery_period)

    # Configure MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT['hostname'], 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()
