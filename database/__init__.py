import uuid

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

from config import TOKEN_EXPIRES_IS_SECONDS

db = SQLAlchemy()


def get_default_expires_in_datetime() -> datetime:
    return datetime.now() + timedelta(seconds=TOKEN_EXPIRES_IS_SECONDS)


def get_default_uuid() -> str:
    return str(uuid.uuid4())


class User(db.Model):
    uuid = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # TODO: шифровать password
    password = db.Column(db.String(255), nullable=False)

    authorization_grants = db.relationship("AuthorizationGrant", back_populates="user", cascade="all, delete")

    def check_password(self, password: str) -> bool:
        return self.password == password

    def __repr__(self):
        return f'<User {self.uuid} email={self.email}>'


class Client(db.Model):
    id = db.Column(db.String(64), primary_key=True, unique=True)
    title = db.Column(db.String(255), unique=True, nullable=False)

    authorization_grants = db.relationship("AuthorizationGrant", back_populates="client", cascade="all, delete")

    def __repr__(self):
        return f'<Client {self.id} title={self.title}>'


class AuthorizationGrant(db.Model):
    uuid = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    scope = db.Column(db.String(55), nullable=False)

    client_id = db.Column(db.String(64), db.ForeignKey('client.id'), nullable=False)
    client = db.relationship("Client", back_populates="authorization_grants")

    user_uuid = db.Column(db.String(64), db.ForeignKey('user.uuid'), nullable=False)
    user = db.relationship("User", back_populates="authorization_grants")

    authorization_code = db.relationship("AuthorizationCode", back_populates="authorization_grant", uselist=False, cascade="all, delete")
    tokens = db.relationship("Token", back_populates="authorization_grant", cascade="all, delete")

    def __repr__(self):
        return f'<AuthorizationGrant {self.uuid} client_id={self.client_id} user_uuid={self.user_uuid}>'


class AuthorizationCode(db.Model):
    code = db.Column(db.String(64), primary_key=True, default=get_default_uuid)

    authorization_grant_uuid = db.Column(db.String(64), db.ForeignKey('authorization_grant.uuid'), nullable=False)
    authorization_grant = db.relationship("AuthorizationGrant", back_populates="authorization_code")

    def __repr__(self):
        return f'<AuthorizationCode {self.code} authorization_grant_uuid={self.authorization_grant_uuid}>'


class Token(db.Model):
    __table_args__ = (db.UniqueConstraint('access_token', 'refresh_token'),)

    access_token = db.Column(db.String(64), primary_key=True, default=get_default_uuid)
    refresh_token = db.Column(db.String(64), index=True, nullable=False, default=get_default_uuid)
    expires_in = db.Column(db.Integer, nullable=False, default=TOKEN_EXPIRES_IS_SECONDS)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    authorization_grant_uuid = db.Column(db.String(64), db.ForeignKey('authorization_grant.uuid'), nullable=False)
    authorization_grant = db.relationship("AuthorizationGrant", back_populates="tokens")

    def __repr__(self):
        return f'<Token access_token={self.access_token} refresh_token={self.refresh_token} ' \
               f'authorization_grant_uuid={self.authorization_grant_uuid}>'

    def expired_in_datatime(self):
        return self.created_at + timedelta(seconds=TOKEN_EXPIRES_IS_SECONDS)
