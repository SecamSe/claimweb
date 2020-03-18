from flask_login import UserMixin

from package import db, login_manager


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    claim = db.Column(db.String(1024), nullable=False)
    comment = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
