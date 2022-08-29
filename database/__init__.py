import uuid

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from main import app
from config import TOKEN_EXPIRES_DELTA_MINUTES

db = SQLAlchemy(app)


def get_default_expires_in_datetime() -> datetime:
    return datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRES_DELTA_MINUTES)


class User(db.Model):
    uuid = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # TODO: шифровать password
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'


class AuthorizationCode(db.Model):
    __table_args__ = (db.UniqueConstraint('scope', 'client_id', 'user_uuid'),)

    code = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    client_id = db.Column(db.String(64), index=True, nullable=False)
    scope = email = db.Column(db.String(55), nullable=False)

    user_uuid = db.Column(db.String(64), db.ForeignKey('user.uuid'), nullable=False)
    user = db.relationship('User', backref=db.backref('authorization_codes', lazy='dynamic'))

    def __init__(self, client_id, user, scope):
        self.client_id = client_id
        self.user = user
        self.scope = scope

    def __repr__(self):
        return f'<AuthorizationCode {self.code}>'


class Token(db.Model):
    __table_args__ = (db.UniqueConstraint('access_token', 'refresh_token'),)

    access_token = db.Column(db.String(64), primary_key=True, default=uuid.uuid4)
    refresh_token = db.Column(db.String(64), index=True, nullable=False, default=uuid.uuid4)
    expires_in = db.Column(db.DateTime, nullable=False, default=get_default_expires_in_datetime)
    active = db.Column(db.String(64), nullable=False, default=uuid.uuid4)

    user_uuid = db.Column(db.String(64), db.ForeignKey('user.uuid'), nullable=False)
    user = db.relationship('User', backref=db.backref('authorization_codes', lazy='dynamic'))

    def __init__(self, user):
        self.user = user

    def __repr__(self):
        return f'<Token {self.code}>'


__all__ = ['db', 'User', 'AuthorizationCode', 'Token']
