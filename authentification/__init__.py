from functools import wraps

from flask import request, make_response, jsonify

from database import Token


def oauth2_decorator():
    """
    Проверяет наличие и срок экспирации токена доступа

    Extended Summary
    ----------------
    Добавляет аттрибут к оборачиваемой функции **user** - объект пользователя

    Returns
    -------
        function
    """

    def _oauth2_decorator(f):
        @wraps(f)
        def __oauth2_decorator(*args, **kwargs):
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

            return f(*args, **kwargs, user=token.user)
        return __oauth2_decorator
    return _oauth2_decorator


__all__ = ['oauth2_decorator']
