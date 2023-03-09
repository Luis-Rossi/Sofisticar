from flask import render_template, request

from app import app, db, login_manager
from app.models.tables import Servico, Usuario


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/servico_cadastrar', methods=['GET', 'POST'])
def servico_cadastrar():
    if request.method == 'POST':
        todos_servicos = Servico.query.all()
        for serv in todos_servicos:
            if request.form['nome'] == serv.nome and serv.isActive == 1:
                mensagem_erro = f'Serviço {serv.nome.upper()} já cadastrado(a) no sistema!'
                return render_template('servico_cadastrar.html', mensagem_erro=mensagem_erro)
        servico = Servico(
            request.form['nome'], request.form['descricao'], request.form['valor'])
        db.session.add(servico)
        db.session.commit()
        mensagem = f'Serviço {servico.nome.upper()} foi cadastrado(a) COM SUCESSO!'
        return render_template('servico_cadastrar.html', mensagem=mensagem)
    return render_template('servico_cadastrar.html')


@app.route('/servico_resultado', methods=['GET', 'POST'])
def servico_resultado():
    servicos = Servico.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("servico_resultado.html", servicos=servicos, opcao=opcao, campo=campo)
    return render_template("servico_resultado.html", servicos=servicos, campo=campo)


@app.route('/servico_editar/<int:id>', methods=['GET', 'POST'])
def servico_editar(id):
    servico = Servico.query.get(id)
    if request.method == 'POST':
        servico.nome = request.form['nome']
        servico.descricao = request.form['descricao']
        servico.valor = request.form['valor']
        servico.isActive = int(request.form['isActive'])
        db.session.commit()
        mensagem_editar = f"Serviço {servico.nome.upper()} foi editado(a) COM SUCESSO!"
        return render_template("servico_resultado.html", mensagem_editar=mensagem_editar)
    return render_template('servico_editar.html', servico=servico)


@app.route('/servico_deletar/<int:id>')
def servico_deletar(id):
    servico = Servico.query.get(id)
    servico.isActive = 0
    db.session.commit()
    mensagem_deletar = f"O serviço {servico.nome.upper()} foi DELETADO(A)!"
    return render_template("servico_resultado.html", mensagem_deletar=mensagem_deletar)


'''
#   PARA DELETAR DEFINITIVAMENTE O SERVIÇO DO BD
@app.route('/deletar_servico2/<int:id>')
def deleta_servico2(id):
    servico = Servico.query.get(id)
    db.session.delete(servico)
    db.session.commit()
    mensagem = f"{servico.nome} foi DELETADO(A)!"
    return render_template("resultado_servico.html", mensagem_deletar=mensagem)
'''
