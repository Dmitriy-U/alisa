import json

from flask import Flask, request, make_response
from flask_cors import CORS

from config import MQTT_TOPIC
from mqtt_client import mqtt_client_instance
from smart_lamp import DEFAULT_SETTING, get_rgb_setting_by_command, get_light_setting_by_command
from commands import (UTTERANCE_LIST, get_suggests, get_command_by_utterance, get_success_answer_by_command,
                      is_color_command, is_switch_command, )

app = Flask(__name__)
CORS(app)

state = {}


def on_message(client, userdata, message):
    """Обработчик сообщений"""

    global state
    state = json.loads(message.payload.decode("utf-8"))


mqtt_client_instance.on_message = on_message


@app.route("/", methods=["POST", "GET"])
def alisa_command_handler():
    global state

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
        response['response']['text'] = 'Привет! Что хочешь сделать с умной лампой Бастион?'
        return make_response(response, 200)

    utterance = payload['request']['original_utterance'].lower()

    if utterance in UTTERANCE_LIST:
        # обработка существующей команды
        command = get_command_by_utterance(utterance)

        if is_color_command(command):
            # установка цвета
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    **DEFAULT_SETTING,
                    "rgb": get_rgb_setting_by_command(command)
                })
            )

        if is_switch_command(command):
            # включение/выключение
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    **DEFAULT_SETTING,
                    "light": get_light_setting_by_command(command)
                })
            )

        response['response']['text'] = f'Хорошо, {get_success_answer_by_command(command)}.'
        response['response']['end_session'] = True
        return make_response(response, 200)

    # обработка несуществующей команды
    response['response']['buttons'] = get_suggests()
    response['response']['text'] = 'Не могу понять. Владик помоги!'
    return make_response(response, 200)
