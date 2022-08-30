import random

from paho.mqtt import client as mqtt_client
from config.__init__ import MQTT_LOGIN, MQTT_PASSWORD, MQTT_HOST, MQTT_PORT, MQTT_TOPIC


def on_connect(client, userdata, flags, rc):
    """Обработчик подключения к устройству"""

    client.subscribe(MQTT_TOPIC)


mqtt_client_instance = mqtt_client.Client(f'alisa-{random.randint(0, 1000)}')
mqtt_client_instance.username_pw_set(MQTT_LOGIN, MQTT_PASSWORD)
mqtt_client_instance.on_connect = on_connect
mqtt_client_instance.connect(host=MQTT_HOST, port=MQTT_PORT, keepalive=60)
mqtt_client_instance.loop_start()

__all__ = ['mqtt_client_instance']
