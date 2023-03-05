from datetime import datetime

from flask import render_template, request

from app import app, db, login_manager
from app.models.tables import Funcionario, Usuario


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/cadastrar_funcionario', methods=['GET', 'POST'])
def adiciona_funcionario():
    if request.method == 'POST':
        todos_funcionarios = Funcionario.query.all()
        for func in todos_funcionarios:
            # VERIFICA SE JÁ HÁ CADASTRO
            if request.form['nome'] == func.nome and func.isActive == 1:
                mensagem_erro = f'Funcionário de nome {func.nome.upper()} já cadastrado(a) no sistema!'
                return render_template('funcionario_cadastrar.html', mensagem_erro=mensagem_erro)
            elif request.form['email'] == func.email and func.isActive == 1:
                mensagem_erro = f'Funcionário com e-mail {func.email.upper()} já cadastrado(a) no sistema!'
                return render_template('funcionario_cadastrar.html', mensagem_erro=mensagem_erro)
            elif request.form['celular'] == func.celular and func.isActive == 1:
                mensagem_erro = f'Funcionário com celular {func.celular} já cadastrado(a) no sistema!'
                return render_template('funcionario_cadastrar.html', mensagem_erro=mensagem_erro)
        # SE NÃO HOUVER, COMMITA NO BD
        funcionario = Funcionario(request.form['nome'], request.form['email'],
                                  request.form['celular'], request.form['dataNascimento'], request.form['dataContrato'], request.form['funcao'])
        db.session.add(funcionario)
        db.session.commit()
        mensagem = f'{funcionario.nome.upper()} foi cadastrado(a) com **SUCESSO!**'
        return render_template('funcionario_cadastrar.html', mensagem=mensagem)
    return render_template("funcionario_cadastrar.html")


@app.route('/funcionario_resultado', methods=['GET', 'POST'])
def resultado_funcionario():
    funcionarios = Funcionario.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("funcionario_resultado.html", funcionarios=funcionarios, opcao=opcao, campo=campo)
    return render_template("funcionario_resultado.html", funcionarios=funcionarios, campo=campo)


@app.route('/funcionario_editar/<int:id>', methods=['GET', 'POST'])
def edita_funcionario(id):
    funcionario = Funcionario.query.get(id)
    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        funcionario.email = request.form['email']
        funcionario.celular = request.form['celular']
        funcionario.dataNascimento = request.form['dataNascimento']
        funcionario.dataContrato = request.form['dataContrato']
        funcionario.funcao = request.form['funcao']
        funcionario.isActive = int(request.form['isActive'])
        db.session.commit()
        mensagem = f"O funcionário {funcionario.nome} foi editado(a) COM SUCESSO!"
        return render_template("funcionario_resultado.html", mensagem_editar=mensagem)
    return render_template('funcionario_editar.html', funcionario=funcionario)


@app.route('/deletar_funcionario2/<int:id>')
def deleta_funcionario2(id):
    funcionario = Funcionario.query.get(id)
    db.session.delete(funcionario)
    db.session.commit()
    mensagem = f"O funcionário {funcionario.nome} foi DELETADO(A)!"
    return render_template("funcionario_resultado.html", mensagem_deletar=mensagem)


@app.route('/deletar_funcionario/<int:id>')
def deleta_funcionario(id):
    funcionario = Funcionario.query.get(id)
    funcionario.isActive = 0
    db.session.commit()
    mensagem = f"O funcionário {funcionario.nome} foi DELETADO(A)!"
    return render_template("funcionario_resultado.html", mensagem_deletar=mensagem)
