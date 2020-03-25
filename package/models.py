from flask_login import UserMixin
from wtforms import SubmitField, BooleanField, StringField, PasswordField, validators
from flask_wtf import Form

from package import db, login_manager


class Usergroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), nullable=False, unique=True)
    Users = db.relationship('User', backref=db.backref('usergroup', lazy=True))


class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    make_date = db.Column(db.Date)
    executor_comment = db.Column(db.String(1024))
    claim = db.Column(db.String(1024), nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    source_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executer_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    email = db.Column(db.String(length=120))
    fullname = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    group_user_id = db.Column(db.Integer, db.ForeignKey('usergroup.id'))
    Claims = db.relationship('Claim',
                             primaryjoin="Claim.source_user_id==User.id",
                             foreign_keys=[Claim.source_user_id],
                             backref=db.backref('user', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan'
                             )
    Claims_executer = db.relationship('Claim',
                                      primaryjoin="Claim.executer_user_id==User.id",
                                      foreign_keys=[Claim.executer_user_id],
                                      backref=db.backref('executer_user', lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all, delete-orphan'
                                      )


class RegForm(Form):
    login = StringField('Имя для входа',
                        [validators.DataRequired()])
    fullname = StringField('Ф.И.О.',
                           [validators.DataRequired()])
    email = StringField('Адрес E-mail',
                        [validators.Email(),
                         validators.Length(min=6, max=35)])
    group = StringField('Группа')
    password = PasswordField('Новый пароль', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли не совпадают')])
    confirm = PasswordField('Подтверждение пароля')
    submit = SubmitField('Сохранить')


class ProfileForm(Form):
    login = StringField('Имя для входа',
                        [validators.DataRequired()])
    fullname = StringField('Ф.И.О.',
                           [validators.DataRequired()])
    email = StringField('Адрес E-mail',
                        [validators.Email(),
                         validators.Length(min=6, max=35)])
    group = StringField('Группа')

    submit = SubmitField('Сохранить')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
