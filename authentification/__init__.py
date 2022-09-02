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

        print('access_token -->', access_token)
        print('expires_in -->', token.expires_in)

        defaults = {"user": token.user}
        defaults.update(kwargs)

        return f(*args, **defaults)

    return decorator


__all__ = ['authenticate_user']
