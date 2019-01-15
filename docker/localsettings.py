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
