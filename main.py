import json

from flask import Flask, request, make_response
from flask_cors import CORS

from commands import UTTERANCE_LIST, get_suggests, get_command_by_utterance, get_success_answer_by_command
from config import MQTT_TOPIC
from mqtt_client import mqtt_client_instance
from smart_lamp import DEFAULT_SETTING, get_rgb_setting_by_command

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
        response['response']['text'] = 'Привет! Что хочешь сделать с умной лампой Бастион?'
        return make_response(response, 200)

    utterance = payload['request']['original_utterance'].lower()

    if utterance in UTTERANCE_LIST:
        command = get_command_by_utterance(utterance)
        # Существующая команда
        if utterance == "красный":
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    **DEFAULT_SETTING,
                    "rgb": get_rgb_setting_by_command(command)
                })
            )
        if utterance == "зелёный":
            mqtt_client_instance.publish(
                MQTT_TOPIC,
                json.dumps({
                    **DEFAULT_SETTING,
                    "rgb": get_rgb_setting_by_command(command)
                })
            )
        response['response']['text'] = f'Хорошо, {get_success_answer_by_command(command)}.'
        response['response']['end_session'] = True
        return make_response(response, 200)

    response['response']['buttons'] = get_suggests()
    response['response']['text'] = 'Не могу понять. Владик помоги!'
    return make_response(response, 200)
