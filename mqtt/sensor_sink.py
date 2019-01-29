import sys
import os
import io
import uuid
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

    logger.info("Subscribe to topic "+ settings.MQTT['topic_dronetrap'])
    client.subscribe(settings.MQTT['topic_dronetrap'])

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
        command = msg.topic.split("/")[1]
        if command == "discovery":
            logger.info("Discovery received")
            sensor_id = data['deviceid']
            queryset = Sensor.objects.filter(device_id=sensor_id)

            # NOTE: This should be done with primary keys
            if queryset.exists():
                sensor = queryset[0]
                logger.info("Sensor updated successfully")
            else:
                sensor = Sensor()
                logger.info("Sensor created sucessfully")

            # Updating or generating data
            sensor.device_id = data['deviceid']
            sensor.serial_num = data['serialnum']
            sensor.model = data['model']
            sensor.version = data['version']
            sensor.available = data['available']
            sensor.energy = data['energy']
            sensor.token = str(uuid.uuid4())
            sensor.save()

            data_status = data['status']
            status = Status()
            status.sensor = sensor
            status.latitude = data_status['location']['latitude']
            status.longitude = data_status['location']['longitude']
            status.orientation = data_status['location']['orientation']
            status.wifi_status = data_status['wifi_status']
            status.rf0_status = data_status['rf0_status']
            status.rf1_status = data_status['rf1_status']
            status.gps_status = data_status['gps_status']
            status.gps_sats = data_status['gps_sats']
            status.cpu = data_status['CPU']
            status.temp = data_status['temp']
            status.ram_total = data_status['RAM']['total']
            status.ram_used = data_status['RAM']['used']
            status.ram_free = data_status['RAM']['free']
            status.disk_total = data_status['DISK']['total']
            status.disk_used = data_status['DISK']['user']
            status.disk_free = data_status['DISK']['free']
            status.disk_percent = data_status['DISK']['percent']
            status.save()

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
