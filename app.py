import json

from flask import Flask, request, make_response, render_template, jsonify
from flask_cors import CORS

from mqtt_client import mqtt_client_instance
from authentification import authenticate_user
from config import MQTT_TOPIC, DATABASE_PATH, YANDEX_CLIENT_SECRET, TOKEN_EXPIRES_IS_SECONDS, TOKEN_TYPE
from database import db, User, AuthorizationGrant, Token, Client, AuthorizationCode
from smart_lamp import DEFAULT_SETTING, get_rgb_setting_by_command, get_light_setting_by_command, get_info_answer
from commands import (UTTERANCE_LIST, get_suggests, get_command_by_utterance, get_success_answer_by_command,
                      is_color_command, is_switch_command, is_info_command, )

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Тестовые данные
test_client_id = '75bfbd31-54f3-4863-aa6b-f741a6f5edd8'
test_user_data = {
    "email": "1@1.ru",
    "password": "11111",
}

with app.app_context():
    db.create_all()

    test_user = User.query.filter_by(email=test_user_data["email"]).first()
    if test_user is None:
        test_user = User(**test_user_data)
        db.session.add(test_user)
        db.session.commit()

    test_client = Client.query.filter_by(id=test_client_id).first()
    if test_client is None:
        test_client = Client(id=test_client_id, title='Яндекс Умный дом')
        db.session.add(test_client)
        db.session.commit()

state = {}


def on_message(client, userdata, message):
    """Обработчик сообщений"""

    global state
    state = json.loads(message.payload.decode("utf-8"))


mqtt_client_instance.on_message = on_message


@app.post("/")
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


# Авторизация Яндекс Диалоги


@app.get("/authorization-code")
def smart_home_authorization_code():
    """Получение авторизационного кода"""

    client = Client.query.filter_by(id=request.args.get('client_id')).first()

    data = {**request.args.to_dict()}

    if client is not None:
        data['client_title'] = client.title

    return render_template('authorization-code.html', **data)


@app.post("/authorization-code-grant")
def smart_home_get_authorization_code_grant():
    """Генерация кода авторизации"""

    user = User.query.filter_by(email=request.json['email']).first()

    if user is None:
        return jsonify({'error': f"Пользователь с email: {request.json['email']} не найден"}), 404

    if not user.check_password(request.json['password']):
        return jsonify({'error': "Пароль не верный"}), 403

    authorization_grant = AuthorizationGrant.query.filter_by(
        user_uuid=user.uuid,
        client_id=request.json['clientId']
    ).first()
    if authorization_grant is not None:
        return jsonify({"error": "Права уже предоставлены"}), 400

    authorization_grant = AuthorizationGrant(client_id=request.json['clientId'], scope=request.json['scope'], user=user)
    authorization_code = AuthorizationCode(authorization_grant=authorization_grant)
    db.session.add(authorization_grant)
    db.session.add(authorization_code)
    db.session.commit()

    return jsonify({"code": authorization_grant.authorization_code.code})


@app.post("/token")
def smart_home_get_token():
    """Получение токенов по коду авторизации"""

    if request.form.get('client_secret') != YANDEX_CLIENT_SECRET:
        return jsonify({'error': "Секрет приложения неверный"}), 400

    authorization_code = AuthorizationCode.query.filter_by(code=request.form.get('code')).first()
    if authorization_code is None:
        return jsonify({'error': "Отсутствует код авторизации или был использован"}), 404

    token = Token(authorization_grant=authorization_code.authorization_grant)
    db.session.add(token)
    db.session.delete(authorization_code)
    db.session.commit()

    response = {
        "token_type": TOKEN_TYPE,
        "expires_in": TOKEN_EXPIRES_IS_SECONDS,
        "scope": authorization_code.authorization_grant.scope,
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
    }

    print('--> token response -->', response)

    return jsonify(response)


@app.post("/refresh-token")
def smart_home_refresh_token():
    """Обновление и выдача новых токенов"""

    if request.form.get('client_secret') != YANDEX_CLIENT_SECRET:
        return jsonify({'error': "Секрет приложения неверный"}), 400

    token = Token.query.filter_by(refresh_token=request.form.get('refresh_token')).first()

    if token is None:
        return jsonify({'error': "Отсутствует токен обновления"}), 401

    new_token = Token(authorization_grant=token.authorization_grant)
    db.session.add(new_token)
    db.session.delete(token)
    db.session.commit()

    response = {
        "token_type": TOKEN_TYPE,
        "expires_in": TOKEN_EXPIRES_IS_SECONDS,
        "scope": new_token.authorization_grant.scope,
        "access_token": new_token.access_token,
        "refresh_token": new_token.refresh_token,
    }

    print('--> refresh-token response -->', response)

    return jsonify(response)


# Методы умного дома


@app.get("/smart-home/v1.0")
@authenticate_user
def smart_home_check(user):
    """Проверка доступности"""

    return make_response({}, 200)


@app.post("/smart-home/v1.0/user/unlink")
@authenticate_user
def smart_home_user_unlink(user):
    """Разъединение аккаунтов"""

    headers = request.headers
    request_id = headers.get('X-Request-Id')

    if request_id is None:
        return make_response({"error": "Отсутствует request_id в заголовке запроса"}, 404)

    # TODO: Удалять все токены и связь AuthorizationGrant

    return make_response({"request_id": request_id}, 200)


@app.get("/smart-home/v1.0/user/devices")
@authenticate_user
def smart_home_get_user_devices(user):
    """Получение устройств пользователя"""

    headers = request.headers
    request_id = headers.get('X-Request-Id')
    if request_id is None:
        return make_response({"error": "Отсутствует request_id в заголовке запроса"}, 404)

    body = {
        "request_id": request_id,
        "payload": {
            "user_id": user.uuid,
            "devices": [
                {
                    "id": '79e22dd5-dbef-41b4-bce4-60853e6ebe21',
                    "name": 'Умная лампа',
                    "description": 'Лампа, которая умеет менять цвет, яркость, температуру света',
                    "room": 'Столовая',
                    "type": 'devices.types.light',
                    "custom_data": {},
                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off",
                            "retrievable": True,
                            "reportable": True,
                        },
                    ],
                    "properties": [],
                    "device_info": {
                        "manufacturer": "Бастион",
                        "model": "Умная лампа",
                        "hw_version": "1.0.0",
                        "sw_version": "1.0.0"
                    }
                }
            ],
        }
    }

    return make_response(body, 200)


@app.post("/smart-home/v1.0/user/devices/query")
@authenticate_user
def smart_home_user_devices_query(user):
    """Действия с устройствами"""

    return make_response({}, 200)
