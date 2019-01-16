import os
MQTT = {
    'hostname': os.environ.get('MOSQUITTO_HOST'),
    # General topics
    'topic_dronetrap': 'dronetrap/#',
    'topic_sensor': 'sensor/#',
    # Specific command topics
    'topic_discovery': 'dronetrap/+/discovery',
    'topic_start_discovery': 'sensor/+/start_discovery',
    'topic_manager_set': 'dronetrap/+/manager/set'
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sec2sky',
        'USER': 'sec2sky',
        'PASSWORD': 's3c2sky',
        'HOST': 'sec2sky_db',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
