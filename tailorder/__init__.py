# Copyright (c) 2019, Bai Web and Mobile Lab
# MIT License. See license.txt
# ----------------------------
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_cors import CORS
__version__ = '0.3.0'

db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app=app, cors_allowed_origins='*')


def create_app():

    app.config.from_object(Config)

    db.init_app(app)
    socketio.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
