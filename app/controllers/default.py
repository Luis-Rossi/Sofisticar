from datetime import date

from flask import flash, redirect, render_template, url_for
from flask_login import login_user, logout_user

from app import app, login_manager
from app.models.forms import LoginForm
from app.models.tables import User


@login_manager.user_loader
def load_user(session_token):
    return User.query.filter_by(id=session_token).first()


@app.route("/index")
@app.route("/")
def index():
    data_hoje = date.today()
    return render_template('index.html', data_hoje=data_hoje)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():       # valida se tem todos os campos obrigatórios preenchidos
        # faz um select no bd para ver se encontra um usuário igual ao inserido
        user = User.query.filter_by(username=form.username.data).first()
        # se o usuário existe E se o password for igual ao inserido
        if user and user.password == form.password.data:
            login_user(user)
            flash("Logged in!")
            return redirect(url_for("index"))
        else:
            flash("Invalid Login!")
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Logged out!")
    return redirect(url_for("index"))


@app.route("/teste")
def teste():
    pass
