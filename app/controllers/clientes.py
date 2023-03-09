from flask import render_template, request

from app import app, db, login_manager
from app.models.tables import Cliente, Usuario, Veiculo


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/cliente_cadastrar', methods=['GET', 'POST'])
def cliente_cadastrar():
    if request.method == 'POST':
        todos_veiculos = Veiculo.query.all()
        todos_clientes = Cliente.query.all()

        for cli in todos_clientes:
            if request.form['email'] == cli.email and cli.isActive == 1:
                mensagem_erro = f'E-mail {cli.email.upper()} já cadastrado(a) no sistema!'
                return render_template('cliente_cadastrar.html', mensagem_erro=mensagem_erro)
            elif request.form['celular'] == cli.celular and cli.isActive == 1:
                mensagem_erro = f'Número de celular já cadastrado(a) no sistema!'
                return render_template('cliente_cadastrar.html', mensagem_erro=mensagem_erro)
            elif request.form['cpf'] == cli.cpf and cli.isActive == 1:
                mensagem_erro = f'CPF nº {cli.cpf} de celular já cadastrado(a) no sistema!'
                return render_template('cliente_cadastrar.html', mensagem_erro=mensagem_erro)

        for veic in todos_veiculos:
            if request.form['placa'] == veic.placa and veic.isActive == 1:
                mensagem_erro = f'Veículo de placa {veic.placa.upper()} já cadastrado(a) no sistema!'
                return render_template('cadastrar_clientes.html', mensagem_erro=mensagem_erro)

        cliente = Cliente(request.form['nome'], request.form['email'],
                          request.form['cpf'], request.form['celular'])
        veiculo = Veiculo(request.form['marca'], request.form['modelo'],
                          request.form['cor'], request.form['placa'], cliente)
        db.session.add(cliente)
        db.session.add(veiculo)
        db.session.commit()
        mensagem = f'Cliente {cliente.nome.upper()} foi cadastrado(a) COM SUCESSO!'
        return render_template('cliente_cadastrar.html', mensagem=mensagem)
    return render_template('cliente_cadastrar.html')


@app.route('/cliente_resultado', methods=['GET', 'POST'])
def cliente_resultado():
    clientes = Cliente.query.all()
    veiculos = Veiculo.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("cliente_resultado.html", clientes=clientes, veiculos=veiculos, opcao=opcao, campo=campo)
    return render_template("cliente_resultado.html", clientes=clientes, veiculos=veiculos, campo=campo)


@app.route('/cliente_editar/<int:id>', methods=['GET', 'POST'])
def cliente_editar(id):
    cliente = Cliente.query.get(id)
    veiculos = Veiculo.query.all()
    if request.method == 'POST':
        cliente.nome = request.form['nome']
        cliente.email = request.form['email']
        cliente.cpf = request.form['cpf']
        cliente.celular = request.form['celular']
        db.session.commit()
        mensagem_editar = f"Cliente {cliente.nome.upper()} foi editado(a) COM SUCESSO!"
        return render_template("cliente_resultado.html", mensagem_editar=mensagem_editar, veiculos=veiculos)
    return render_template("cliente_editar.html", cliente=cliente, veiculos=veiculos)


@app.route('/cliente_deletar/<int:id>')
def cliente_deletar(id):
    cliente = Cliente.query.get(id)
    cliente.isActive = 0
    db.session.commit()
    mensagem_deletar = f"O cliente {cliente.nome.upper()} foi DELETADO(A)!"
    return render_template("cliente_resultado.html", mensagem_deletar=mensagem_deletar)


'''
@app.route('/cliente_deletar2/<int:id>')
def cliente_deletar2(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    mensagem = f"{cliente.nome} foi DELETADO(A)!"
    return render_template("resultado_clientes.html", mensagem_deletar=mensagem)
'''
