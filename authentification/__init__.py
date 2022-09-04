from datetime import datetime
from functools import wraps
from flask import request, make_response, jsonify

from database import Token


def authenticate_user(f):
    """
    Проверяет наличие и срок экспирации токена доступа

    Extended Summary
    ----------------
    Добавляет аттрибут к оборачиваемой функции **user** - объект пользователя

    Returns
    -------
        function
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        headers = request.headers

        if headers.get('Authorization') is None:
            return make_response({"error": "Отсутствует Bearer токен"}, 401)

        authorization = headers.get('Authorization')
        access_token = authorization.split('Bearer ', 1)[1]
        token = Token.query.filter_by(access_token=access_token).first()

        if token is None:
            return jsonify({'error': "Отсутствует токен доступа"}), 401

        expired_in_datatime_timestamp = int(round(token.expired_in_datatime().timestamp()))
        now_datatime_timestamp = int(round(datetime.now().timestamp()))

        print('now timestamp -->', now_datatime_timestamp)
        print('expires_in timestamp -->', expired_in_datatime_timestamp)

        if now_datatime_timestamp > expired_in_datatime_timestamp:
            return jsonify({'error': "Срок жизни токена доступа истёк"}), 401

        defaults = {"user": token.authorization_grant.user}
        defaults.update(kwargs)

        return f(*args, **defaults)

    return decorator


__all__ = ['authenticate_user']
