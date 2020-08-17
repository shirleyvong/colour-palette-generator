from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask import current_app as app
from flask_bcrypt import Bcrypt
import datetime
import jwt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Palette(db.Model, SerializerMixin):
  __tablename__ = 'palettes'

  id = db.Column(db.Integer, primary_key=True)
  colours = db.Column(db.ARRAY(db.String(6)), nullable=False)
  image =  db.Column(db.LargeBinary, nullable=False)

  def __repr__(self):
    return '[' + ', '.join(self.colours) + ']'

  def as_dict(self):
    return {
    'id': self.id,
    'colours': self.colours
  }


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)

  def __init__(self, username, password):
    self.username = username
    self.password = bcrypt.generate_password_hash(password)

  def encode_auth_token(self, user_id):
    try:
      payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
      }
      return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    except Exception as e:
      app.logger.info(e)
      return e

  @staticmethod
  def decode_auth_token(auth_token):
    try:
      payload = jwt.decode(auth_token, app.config['SECRET_KEY'])
      return payload['sub']
    except jwt.ExpiredSignatureError:
      return 'Signature expired, please log in again.'
    except jwt.InvalidTokenError:
      return 'Invalid token, please log in again.'


class BlacklistedToken(db.Model):
  __tablename__ = 'blacklisted_tokens'

  id = db.Column(db.Integer, primary_key=True)
  token = db.Column(db.String(500), unique=True, nullable=False)
  blacklisted_on = db.Column(db.DateTime, nullable=False)

  def __init__(self, token):
    self.token = token
    self.blacklisted_on = datetime.datetime.now()