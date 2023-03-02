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
            if request.form['nome'] == func.nome:
                mensagem_erro = f'Funcionário de nome {func.nome.upper()} já cadastrado(a) no sistema!'
                return render_template('cadastrar_funcionario.html', mensagem_erro=mensagem_erro)
            elif request.form['email'] == func.email:
                mensagem_erro = f'Funcionário com e-mail {func.email.upper()} já cadastrado(a) no sistema!'
                return render_template('cadastrar_funcionario.html', mensagem_erro=mensagem_erro)
            elif request.form['celular'] == func.celular:
                mensagem_erro = f'Funcionário com celular {func.celular} já cadastrado(a) no sistema!'
                return render_template('cadastrar_funcionario.html', mensagem_erro=mensagem_erro)
        funcionario = Funcionario(request.form['nome'], request.form['email'],
                                  request.form['celular'], request.form['dataNascimento'], request.form['dataContrato'], request.form['funcao'])
        db.session.add(funcionario)
        db.session.commit()
        mensagem = f'{funcionario.nome.upper()} foi cadastrado(a) com **SUCESSO!**'
        return render_template('cadastrar_funcionario.html', mensagem=mensagem)
    return render_template("cadastrar_funcionario.html")
