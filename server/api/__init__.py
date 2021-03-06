from flask import Flask, send_from_directory
from api.blueprints.palette import palette
from api.blueprints.auth import auth
from api.models import db, bcrypt
from api.config import Config

def create_app():
  app = Flask(__name__, static_folder='./build/')

  app.config.from_object(Config)
  app.register_blueprint(palette, url_prefix='/api/palettes')
  app.register_blueprint(auth, url_prefix='/api/auth')
  db.init_app(app)
  bcrypt.init_app(app)

  return app
