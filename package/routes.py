from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from package import app, db
from package.models import User, Claim


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    next_page = request.args.get('next')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(next_page)
        else:
            flash('Неправильное имя либо пароль')

    else:
        flash('Заполните все поля')

    return render_template('login.html', next=next_page)


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    next_page = request.args.get('next')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page') + '?next=' + next_page)

    return render_template('register.html', next=next_page)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response


@app.route('/users', methods=['GET'])
@login_required
def users():
    return render_template('users.html', users=User.query.all())


@app.route('/claim', methods=['GET'])
def claim():
    return render_template('claim.html', claims=Claim.query.all())
