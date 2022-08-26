from flask import Flask, request, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

commands = {
    "включить": "on",
    "выключить": "off"
}

commands_list = list(commands.keys())


@app.route("/", methods=["POST", "GET"])
def alisa_command_handler():
    print("-->", request.json)
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

    if command in commands_list:
        response['response']['buttons'] = get_suggests()
        response['response']['text'] = f'Хорошо {commands[command]}'
        return make_response(response, 200)

    response['response']['buttons'] = get_suggests()
    response['response']['text'] = 'Уточните пожалуйста ...'
    return make_response(response, 200)


def get_suggests():
    suggests = list()
    for command in commands_list:
        suggests.append({'title': command, 'hide': True})
    print('suggests -->', suggests)
    return suggests
