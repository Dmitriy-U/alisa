import random

from paho.mqtt import client as mqtt_client
from config import MQTT_LOGIN, MQTT_PASSWORD, MQTT_HOST, MQTT_PORT

mqtt_client_instance = mqtt_client.Client(f'alisa-{random.randint(0, 1000)}')
mqtt_client_instance.username_pw_set(MQTT_LOGIN, MQTT_PASSWORD)
mqtt_client_instance.connect(
    host=MQTT_HOST,
    port=MQTT_PORT,
    keepalive=60
)
