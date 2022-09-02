from functools import wraps

from flask import request, make_response, jsonify

from database import Token


def authenticate_user():
    """
    Проверяет наличие и срок экспирации токена доступа

    Extended Summary
    ----------------
    Добавляет аттрибут к оборачиваемой функции **user** - объект пользователя

    Returns
    -------
        function
    """

    def _authenticate_user(f):
        @wraps(f)
        def __authenticate_user(*args, **kwargs):
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
        return __authenticate_user
    return _authenticate_user


__all__ = ['authenticate_user']
