import sys
import os
import io
import uuid
import traceback
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


def to_float(str):
    try:
        return float(str)
    except ValueError:
        return None

def to_int(str):
    try:
        return int(str)
    except ValueError:
        return None

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

            data_field = data['data']

            # Updating or generating data
            sensor.device_id = data['deviceid']
            sensor.serial_num = data['serialnum']
            sensor.model = data_field['model']
            sensor.version = data_field['version']
            sensor.available = data_field['available']
            sensor.energy = data_field['energy']
            sensor.token = str(uuid.uuid4())
            sensor.save()

            status = Status()
            status.sensor = sensor
            status.latitude = to_float(data_field['location']['latitude'])
            status.longitude = to_float(data_field['location']['longitude'])
            status.orientation = to_float(data_field['location']['orientation'])
            status.wifi_status = data_field['wifi_status']
            status.rf0_status = data_field['rf0_status']
            status.rf1_status = data_field['rf1_status']
            status.gps_status = data_field['gps_status']
            status.gps_sats = data_field['gps_sats']
            status.cpu = data_field['CPU']
            status.temp = data_field['temp']
            status.ram_total = to_int(data_field['RAM']['total'])
            status.ram_used = to_int(data_field['RAM']['used'])
            status.ram_free = to_int(data_field['RAM']['free'])
            status.disk_total = data_field['DISK']['total']
            status.disk_used = data_field['DISK']['used']
            status.disk_free = data_field['DISK']['free']
            status.disk_percent = data_field['DISK']['percent']
            status.save()

        elif command == "state":
            logger.info("State received")
        elif command == "detection":
            logger.info("Detection received")
        else:
            logger.error("topic not recognised")

    except Exception as e:
        logger.error('Exception: '+ str(e))
        traceback.print_exc()





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
