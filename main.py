import json

from flask import Flask, request, make_response
from flask_cors import CORS

from commands import command_list, commands, get_suggests
from config import MQTT_TOPIC
from mqtt_client import mqtt_client_instance

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST", "GET"])
def alisa_command_handler():
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    payload = request.json

    if payload['session']['new']:
        # Это новый пользователь.
        response['response']['buttons'] = get_suggests()
        response['response']['text'] = 'Привет! Что хочешь сделать с умной лампой Бастион?'
        return make_response(response, 200)

    command = payload['request']['original_utterance'].lower()

    if command in command_list:
        # Существующая команда
        response['response']['buttons'] = get_suggests()
        response['response']['text'] = f'Хорошо {commands[command]}'
        if command == "красный":
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    "fito": 0,
                    "light": {
                        "brightness": 0,
                        "temperature": 0
                    },
                    "rgb": {
                        "red": 255,
                        "green": 0,
                        "blue": 0
                    }
                })
            )
        if command == "зелёный":
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    "fito": 0,
                    "light": {
                        "brightness": 0,
                        "temperature": 0
                    },
                    "rgb": {
                        "red": 0,
                        "green": 255,
                        "blue": 0
                    }
                })
            )
        response['response']['end_session'] = True
        return make_response(response, 200)

    response['response']['buttons'] = get_suggests()
    response['response']['text'] = 'Уточните пожалуйста ...'
    return make_response(response, 200)
