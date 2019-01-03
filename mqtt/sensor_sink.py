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
from api.serializers import DetectionSerializer
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

    # Subscribe to topic
    client.subscribe(settings.MQTT['topic'])

#
# Name: on_message
# Description: Handler when a message is received
#
def on_message(client, userdata, msg):
    logger.info("topic: '" + msg.topic + "'' payload: '" + str(msg.payload) + "'")


if __name__ == "__main__":


    message = {
               'sensor': 1,
               'description': 'mydescription',
               'thread_id': 1,
               'home_latitude' : 43.2,
               'home_longitude' : 43.2,
               'latitude' : 43.2,
               'altitude' : 43.2,
               'longitude' : 43.2,
               'rssi' : 43.2,
               'signal_type' : "MySignalType"
               }

    # message_str = json.dumps(message)
    # print( type(message) )
    # print( type(message_str) )
    # str = json.dumps(message)
    # binary = ' '.join(format(ord(letter), 'b') for letter in str)
    # stream = io.BytesIO(binary)
    #
    # data = JSONParser().parse(message)
    serializer = DetectionSerializer(data=message)
    print(serializer.is_valid())

    sensor = Sensor.objects.get(id=serializer.data['sensor'])
    #print(serializer.data['sensor'])
    print(serializer.data['sensor'])
    print(sensor)

    serializer.data['sensor'] = sensor
    print(serializer.create(serializer.data))
    sys.exit(0)

    # Configure MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()
