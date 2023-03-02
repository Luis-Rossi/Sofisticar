from datetime import date

from flask import render_template

from app import app
from app.controllers.funcionarios import adiciona_funcionario


@app.route("/index")
@app.route("/")
def index():
    data_hoje = date.today()
    return render_template('index.html', data_hoje=data_hoje)
