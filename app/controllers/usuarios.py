from flask import render_template, request

from app import app, db, login_manager
from app.models.tables import Funcionario, Usuario


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/usuario_cadastrar', methods=['GET', 'POST'])
def usuario_cadastrar():
    todos_funcionarios = Funcionario.query.all()
    todos_usuarios = Usuario.query.all()

    # LISTAS PARA RETORNAR DROPDOWN DE OPÇÕES PARA CADASTRO
    # DESSA FORMA, ELE JÁ LINKA O EMAIL DO FUNCIONARIO COM O USUARIO
    # AMARRANDO COM O ID NO BANCO

    email_func_ativos = []
    email_usuarios_ativos = []

    for func in todos_funcionarios:
        if func.isActive == 1:
            email_func_ativos.append(func.email)

    for user in todos_usuarios:
        if user.isActive == 1:
            email_usuarios_ativos.append(user.email)

    # CRIA UMA LISTA COM OS EMAILS DE FUNCIONARIOS ATIVOS QUE AINDA NÃO TÊM USUÁRIO CADASTRADO
    lista_emails = [
        elemento for elemento in email_func_ativos if elemento not in email_usuarios_ativos]

    # CADASTRO NO BANCO DO USUÁRIO
    if request.method == 'POST':
        todos_usuarios = Usuario.query.all()
        for user in todos_usuarios:
            # VERIFICA SE JÁ HÁ CADASTRO DO MESMO USERNAME
            if request.form['username'] == user.username and user.isActive == 1:
                mensagem_erro = f'Username {user.username.upper()} já cadastrado(a) no sistema!'
                return render_template('usuario_cadastrar.html', mensagem_erro=mensagem_erro, todos_funcionarios=todos_funcionarios, lista_emails=lista_emails)
        # SE NÃO HOUVER, COMMITA NO BD
        for func in todos_funcionarios:
            if func.email == request.form['email']:
                usuario = Usuario(
                    request.form['username'], request.form['password'], func.email, func.id)
        db.session.add(usuario)
        db.session.commit()
        mensagem = f'O usuário {usuario.username.upper()} foi cadastrado(a) COM SUCESSO!'
        return render_template('usuario_resultado.html', mensagem=mensagem, todos_funcionarios=todos_funcionarios, lista_emails=lista_emails)
    return render_template("usuario_cadastrar.html", todos_funcionarios=todos_funcionarios, lista_emails=lista_emails)


@app.route('/usuario_resultado', methods=['GET', 'POST'])
def usuario_resultado():
    funcionarios = Funcionario.query.all()
    usuarios = Usuario.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("usuario_resultado.html", funcionarios=funcionarios, usuarios=usuarios, opcao=opcao, campo=campo)
    return render_template("usuario_resultado.html", funcionarios=funcionarios, usuarios=usuarios, campo=campo)


@app.route('/usuario_editar/<int:id>', methods=['GET', 'POST'])
def usuario_editar(id):
    usuario = Usuario.query.get(id)
    funcionario = Funcionario.query.get(usuario.funcionario_id)
    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.isActive = int(request.form['isActive'])
        db.session.commit()
        mensagem = f"O usuário {usuario.username} foi editado(a) COM SUCESSO!"
        return render_template("usuario_resultado.html", mensagem_editar=mensagem)
    return render_template('usuario_editar.html', usuario=usuario, funcionario=funcionario)


@app.route('/usuario_redefinir_senha/<int:id>', methods=['GET', 'POST'])
def usuario_redefinir_senha(id):
    usuario = Usuario.query.get(id)
    funcionario = Funcionario.query.get(usuario.funcionario_id)
    if request.method == 'POST':
        usuario.password = request.form['novo_password']
        db.session.commit()
        mensagem = f"A senha do usuário {usuario.username} foi alterada COM SUCESSO!"
        return render_template("usuario_resultado.html", mensagem_editar=mensagem)
    return render_template('usuario_redefinir_senha.html', usuario=usuario, funcionario=funcionario)


@app.route('/usuario_deletar/<int:id>')
def usuario_deletar(id):
    usuario = Usuario.query.get(id)
    usuario.isActive = 0
    db.session.commit()
    mensagem = f"O usuário {usuario.username} foi DELETADO(A)!"
    return render_template("usuario_resultado.html", mensagem_deletar=mensagem)
