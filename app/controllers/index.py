from datetime import date

from flask import render_template

from app import app, login_manager
#from app.models.forms import LoginForm
from app.models.tables import Usuario


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route("/index")
@app.route("/")
def index():
    data_hoje = date.today()
    return render_template('index.html', data_hoje=data_hoje)
