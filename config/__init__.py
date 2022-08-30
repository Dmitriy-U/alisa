import json

from pathlib import Path

script_location = Path(__file__).absolute().parent.parent

with open(f'{script_location}/config/config.json') as f:
    config = json.load(f)

MQTT_HOST = config["MQTT_HOST"]
MQTT_PORT = config["MQTT_PORT"]
MQTT_LOGIN = config["MQTT_LOGIN"]
MQTT_PASSWORD = config["MQTT_PASSWORD"]
MQTT_TOPIC = config["MQTT_TOPIC"]
TOKEN_EXPIRES_DELTA_MINUTES = config["TOKEN_EXPIRES_DELTA_MINUTES"]
DATABASE_PATH = f'{script_location}/{config["DATABASE_PATH"]}'

__all__ = ['MQTT_HOST', 'MQTT_PORT', 'MQTT_LOGIN', 'MQTT_PASSWORD', 'MQTT_TOPIC', 'TOKEN_EXPIRES_DELTA_MINUTES',
           'DATABASE_PATH']
