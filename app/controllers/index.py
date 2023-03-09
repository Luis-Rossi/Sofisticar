from datetime import date

from flask import render_template

import app.controllers.funcionarios
import app.controllers.servicos
import app.controllers.usuarios
from app import app


@app.route("/index")
@app.route("/")
def index():
    data_hoje = date.today()
    return render_template('index.html', data_hoje=data_hoje)
