from datetime import date

from flask import render_template

import app.controllers.clientes
import app.controllers.funcionarios
import app.controllers.produtos
import app.controllers.servicos
import app.controllers.usuarios
import app.controllers.veiculos
from app import app


@app.route("/index")
@app.route("/")
def index():
    data_hoje = date.today()
    return render_template('index.html', data_hoje=data_hoje)
