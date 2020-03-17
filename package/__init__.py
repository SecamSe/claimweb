from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config

app = Flask(__name__)
app.secret_key = 'secret'
app.config.from_object(Config)

db = SQLAlchemy(app)

login_manager = LoginManager(app)

from package import models, routes

db.create_all()
