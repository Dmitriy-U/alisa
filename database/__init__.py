import uuid

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from config.__init__ import TOKEN_EXPIRES_DELTA_MINUTES

db = SQLAlchemy()


def get_default_expires_in_datetime() -> datetime:
    return datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRES_DELTA_MINUTES)


def get_default_uuid() -> str:
    return str(uuid.uuid4())


class User(db.Model):
    uuid = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # TODO: шифровать password
    password = db.Column(db.String(255), nullable=False)

    authorization_codes = db.relationship("AuthorizationCode", back_populates="user")
    tokens = db.relationship("Token", back_populates="user")

    def __repr__(self):
        return f'<User {self.email}>'


class AuthorizationCode(db.Model):
    __table_args__ = (db.UniqueConstraint('scope', 'client_id', 'user_uuid'),)

    code = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    client_id = db.Column(db.String(64), index=True, nullable=False)
    scope = db.Column(db.String(55), nullable=False)

    user_uuid = db.Column(db.String(64), db.ForeignKey('user.uuid'), nullable=False)
    user = db.relationship("User", back_populates="authorization_codes")

    def __repr__(self):
        return f'<AuthorizationCode {self.code}>'


class Token(db.Model):
    __table_args__ = (db.UniqueConstraint('access_token', 'refresh_token'),)

    access_token = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    refresh_token = db.Column(db.String(64), index=True, nullable=False, default=get_default_uuid)
    expires_in = db.Column(db.DateTime, nullable=False, default=get_default_expires_in_datetime)
    active = db.Column(db.String(64), nullable=False, default=get_default_uuid)

    user_uuid = db.Column(db.String(64), db.ForeignKey('user.uuid'), nullable=False)
    user = db.relationship('User', back_populates="tokens")

    def __repr__(self):
        return f'<Token {self.code}>'
