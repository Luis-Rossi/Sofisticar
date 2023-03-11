from flask import flash, redirect, render_template, request

from app import app, db, login_manager
from app.models.tables import Cliente, Usuario, Veiculo


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/veiculo_cadastrar', methods=['GET', 'POST'])
def veiculo_cadastrar():
    clientes = Cliente.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("veiculo_cadastrar.html", clientes=clientes, opcao=opcao, campo=campo)
    return render_template("veiculo_cadastrar.html", clientes=clientes, campo=campo)


@app.route('/veiculo_adiciona/<int:id>', methods=['GET', 'POST'])
def veiculo_adiciona(id):
    cliente = Cliente.query.get(id)
    todos_veiculos = Veiculo.query.all()
    if request.method == 'POST':
        for veic in todos_veiculos:
            if request.form['placa'] == veic.placa and veic.isActive == 1:
                mensagem_erro = f'Placa {veic.placa.upper()} já cadastrada no sistema!'
                return render_template('veiculo_cadastrar.html', mensagem_erro=mensagem_erro)
        veiculo = Veiculo(request.form['marca'], request.form['modelo'],
                          request.form['cor'], request.form['placa'], cliente)
        db.session.add(veiculo)
        db.session.commit()
        mensagem_sucesso = 'Veículo cadastrado COM SUCESSO!'
        flash(mensagem_sucesso, 'info')
        return redirect(f'/veiculo_adiciona/{cliente.id}')
    return render_template('veiculo_adiciona.html', cliente=cliente, veiculos=todos_veiculos)


@app.route('/veiculo_editar/<int:id>', methods=['GET', 'POST'])
def veiculo_editar(id):
    veiculo = Veiculo.query.get(id)
    cliente = Cliente.query.get(veiculo.cliente_id)
    if request.method == 'POST':
        veiculo.marca = request.form['marca']
        veiculo.modelo = request.form['modelo']
        veiculo.cor = request.form['cor']
        veiculo.placa = request.form['placa']
        veiculo.isActive = int(request.form['isActive'])
        db.session.commit()
        mensagem = 'Veículo editado COM SUCESSO!'
        flash(mensagem, 'info')
        return render_template("veiculo_adiciona.html", mensagem=mensagem, cliente=cliente, veiculo=veiculo)
    return render_template("veiculo_editar.html", cliente=cliente, veiculo=veiculo)


@app.route('/veiculo_deletar/<int:id>')
def veiculo_deletar(id):
    veiculo = Veiculo.query.get(id)
    veiculo.isActive = 0
    db.session.commit()
    mensagem_deletar = f"O veículo de placa {veiculo.placa.upper()} foi DELETADO(A)!"
    return render_template("veiculo_cadastrar.html", mensagem_deletar=mensagem_deletar)


'''
@app.route('/deletar_veiculo/<int:id>')
def deleta_veiculo(id):
    veiculo = Veiculo.query.get(id)
    id_cliente = veiculo.cliente_id
    cliente = Cliente.query.get(id_cliente)
    db.session.delete(veiculo)
    db.session.commit()
    mensagem = f"Veículo placa {veiculo.placa} foi DELETADO(A)!"  # validação
    flash(mensagem, 'error')
    return redirect(f'/veiculos/{cliente.id}')
    # return render_template("veiculos.html", cliente = cliente, mensagem_deletar = mensagem)
'''
