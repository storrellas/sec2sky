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
from api.models import *


# Configuration values
dronetrap_id = 1

#
# Name: on_connect
# Description: Handler when a connect is reached
#
def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code "+str(rc))

    # Subscribe to topic list
    # logger.info("Subscribe to topic "+ settings.MQTT['topic_dronetrap'])
    # client.subscribe(settings.MQTT['topic_dronetrap'])

    logger.info("Subscribe to topic "+ settings.MQTT['topic_discovery'])
    client.subscribe(settings.MQTT['topic_discovery'])

#
# Name: creates_model
# Description: Creates a model given some JSON data
#
def create_model(serializer, data):
    serializer = serializer(data=data)
    if serializer.is_valid():
        model = serializer.create(serializer.validated_data)

        print("Create Model")
        print(serializer.validated_data)

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

    try:

        # Deserialize JSON
        stream = io.BytesIO(msg.payload)
        data = JSONParser().parse(stream)

        # Parse topic
        sensor_id = msg.topic.split("/")[1]
        command = msg.topic.split("/")[2]
        if command == "discovery":
            logger.info("Discovery received")
            sensor_id = msg.topic.split("/")[1]
            queryset = Sensor.objects.filter(name=sensor_id)

            # NOTE: This should be done with primary keys
            if queryset.exists():
                sensor = queryset[0]
                sensor.name = sensor_id
                sensor.description = data['description']
                sensor.latitude = data['latitude']
                sensor.longitude = data['longitude']
                sensor.save()
                logger.info("Sensor updated successfully")
            else:
                sensor = Sensor.objects.create(name=sensor_id,
                                               description=data['description'],
                                               latitude=data['latitude'],
                                               longitude=data['longitude'])
                logger.info("Sensor created sucessfully")

            if sensor.swarm is not None:
                logger.info("Sensor ASSIGNED. Notify Sensor sim")
                topic = 'dronetrap/' + str(dronetrap_id) + '/manager/set'
                serializer = SensorSerializer(sensor)
                client.publish(topic, json.dumps(serializer.validated_data))
            else:
                logger.info("Sensor unassigned")

        elif command == "state":
            logger.info("State received")
        elif command == "detection":
            logger.info("Detection received")
        else:
            logger.error("topic not recognised")

    except Exception as e:
        logger.error('Exception: '+ str(e))




    # # Detection Topic
    # if msg.topic == settings.MQTT['topic_sensor_detection']:
    #     create_model(DetectionSerializer, data)
    # # Sensor Topic
    # elif msg.topic == settings.MQTT['topic_sensor_register']:
    #     create_model(SensorSerializer, data)
    # # Status Topic
    # elif msg.topic == settings.MQTT['topic_sensor_status']:
    #     create_model(StatusSerializer, data)
    # else:
    #     pass

if __name__ == "__main__":

    # Configure MQTT Client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(settings.MQTT['hostname'], 1883, 60)


    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    client.loop_forever()
