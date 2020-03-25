from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_table import Table, Col, DateCol
import datetime

from package import app, db
from package.models import User, Claim, Usergroup, ProfileForm


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
    fullname = request.form.get('fullname')
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
            new_user = User(login=login, fullname=fullname, password=hash_pwd)
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


@app.route('/users', methods=['POST', 'GET'])
@login_required
def users():
    task = request.args.get('task')
    if task == 'delete':
        User.query.filter_by(id=request.args.get('id')).delete()
        db.session.commit()
    elif task == 'edit':
        pass

    users = User.query.outerjoin(Usergroup).all()
    groups = Usergroup.query.all()

    return render_template('users.html', users=users, groups=groups)


@app.route('/claim', methods=['POST', 'GET'])
@login_required
def claim():
    task = request.args.get('task')
    if task == 'delete':
        Claim.query.filter_by(id=request.args.get('id')).delete()
        db.session.commit()
    elif task == 'edit':
        pass
    elif task == 'make':
        upd = db.session.query(Claim).get(request.args.get('id'))
        upd.make_date = datetime.date.today()
        upd.executer_user_id = current_user.get_id()
        db.session.commit()

    claims = Claim.query.join(User, Claim.source_user_id == User.id).all()
    #   Claim.query.join(User).all()
    return render_template('claim.html', claims=claims)


@app.route('/add_claim', methods=['POST'])
def add_claim():
    date = datetime.date.today()
    claim = request.form.get('claim')
    comment = request.form.get('comment')
    new_claim = Claim(date=date, claim=claim, comment=comment, source_user_id=current_user.get_id())
    db.session.add(new_claim)
    db.session.commit()
    return redirect(url_for('claim'))


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    form = ProfileForm(request.form)
    groups = db.session.query(Usergroup).all()
    if request.method == 'POST' and form.validate_on_submit():
        upd = db.session.query(User).get(current_user.get_id())
        upd.login = form.login.data
        upd.fullname = form.fullname.data
        upd.email = form.email.data
        db.session.commit()

    return render_template('profile.html', form=form, groups=groups)
