import sys
import os
import io
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

import time
import json
import signal
from random import randint

# Libraries import
import paho.mqtt.client as mqtt

# Import Django
import django
from django.conf import settings


# Project imports
from sec2sky import utils

logger = utils.get_logger()

# django project name is adleads, replace adleads with your project name
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sec2sky.settings")
django.setup()

from rest_framework.parsers import JSONParser
from api.serializers import *
from api.models import Detection, Sensor


# Configuration values
sensor_id = 1
response_delay = 3

#
# Name: on_connect
# Description: Handler when a connect is reached
#
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))

    # Subscribe to topic list
    client.subscribe(settings.MQTT['topic_sensor_detection'])
    client.subscribe(settings.MQTT['topic_sensor_register'])
    client.subscribe(settings.MQTT['topic_sensor_status'])


#
# Name: on_message
# Description: Handler when a message is received
#
def create_model(serializer, data):
    serializer = serializer(data=data)
    if serializer.is_valid():
        model = serializer.create(serializer.validated_data)
        model.save()
        logger.info("Object creation successful!")
    else:
        logger.error("Object creation failed. Wrong input data")
#
# Name: on_message
# Description: Handler when a message is received
#
def on_message(client, userdata, msg):
    logger.info("Message Received [topic: '" + msg.topic + "' payload: '" + str(msg.payload) + "']")

    # Deserialize JSON
    stream = io.BytesIO(msg.payload)
    data = JSONParser().parse(stream)

    # Detection Topic
    if msg.topic == settings.MQTT['topic_sensor_detection']:
        create_model(DetectionSerializer, data)
    # Sensor Topic
    elif msg.topic == settings.MQTT['topic_sensor_register']:
        create_model(SensorSerializer, data)
    # Status Topic
    elif msg.topic == settings.MQTT['topic_sensor_status']:
        pass
    else:
        pass

if __name__ == "__main__":

    # Configure MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()
