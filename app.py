import json

from flask import Flask, request, make_response, render_template, jsonify
from flask_cors import CORS

from config import MQTT_TOPIC, DATABASE_PATH
from database import User, AuthorizationCode, db
from mqtt_client import mqtt_client_instance
from smart_lamp import DEFAULT_SETTING, get_rgb_setting_by_command, get_light_setting_by_command, get_info_answer
from commands import (UTTERANCE_LIST, get_suggests, get_command_by_utterance, get_success_answer_by_command,
                      is_color_command, is_switch_command, is_info_command, )

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

    test_user = User.query.filter_by(email='1@1.ru').first()

    if test_user is None:
        test_user = User(email='1@1.ru', password="11111")
        db.session.add(test_user)
        db.session.commit()

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

        if is_info_command(command):
            # информация
            response['response']['text'] = get_info_answer(state)
            response['response']['end_session'] = True
            return make_response(response, 200)

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


@app.route("/smart-home", methods=["GET"])
def smart_home_handler():
    """Обработчик команд"""

    print('--> request', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    response['response']['text'] = 'Не могу понять.'
    return make_response(response, 200)


@app.get("/authorization-code")
def smart_home_authorization_code():
    """Получение авторизационного кода"""

    return render_template('authorization-code.html', **request.args.to_dict())


@app.post("/authorization-code-grant")
def smart_home_get_authorization_code_grant():
    """Генерация авторизационного кода"""

    user = User.query.filter_by(email=request.json['email']).first()

    if user is None:
        return jsonify({'error': f"Пользователь с email: {request.json['email']} не найден"}), 404

    if not user.check_password(request.json['password']):
        return jsonify({'error': "Пароль не верный"}), 403

    authorization_code = AuthorizationCode.query.filter_by(user_uuid=user.uuid).first()
    if authorization_code is not None:
        return jsonify({"code": authorization_code.code})

    authorization_code = AuthorizationCode(client_id=request.json['clientId'], scope=request.json['scope'], user=user)
    db.session.add(authorization_code)
    db.session.commit()

    return jsonify({"code": authorization_code.code})


@app.post("/token")
def smart_home_get_token():
    """Получение токенов по авторизационному коду"""

    try:
        print('smart_home_get_token query params -->', request.args.to_dict())
        print('smart_home_get_token payload -->', request.json)
    except Exception:
        pass

    return make_response(request.json, 500)


@app.route("/refresh-token", methods=["GET", "POST"])
def smart_home_refresh_token():
    """Обновление и выдача новых токенов"""

    try:
        print('--> request args', request.args.to_dict())
        print('--> request json', request.json)
    except Exception:
        pass

    response = {
        "store": "test",
        "response": {
            "end_session": False
        }
    }

    response['response']['text'] = 'Не могу понять.'
    return make_response(response, 200)
