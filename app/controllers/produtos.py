from flask import render_template, request

from app import app, db, login_manager
from app.models.tables import Produto, Usuario


@login_manager.user_loader
def load_user(session_token):
    return Usuario.query.filter_by(id=session_token).first()


@app.route('/produto_cadastrar', methods=['GET', 'POST'])
def produto_cadastrar():
    if request.method == 'POST':
        todos_produtos = Produto.query.all()
        for prod in todos_produtos:
            if request.form['nome'] == prod.nome and prod.isActive == 1:
                mensagem_erro = f'Produto {prod.nome.upper()} já cadastrado(a) no sistema!'
                return render_template('produto_cadastrar.html', mensagem_erro=mensagem_erro)
        produto = Produto(
            request.form['nome'], request.form['descricao'], request.form['valor'])
        db.session.add(produto)
        db.session.commit()
        mensagem = f'Produto {produto.nome.upper()} foi cadastrado(a) COM SUCESSO!'
        return render_template('produto_cadastrar.html', mensagem=mensagem)
    return render_template('produto_cadastrar.html')


@app.route('/produto_resultado', methods=['GET', 'POST'])
def produto_resultado():
    produtos = Produto.query.all()
    campo = ''
    if request.method == 'POST':
        opcao = request.form['opcao']
        campo = request.form['campo']
        return render_template("produto_resultado.html", produtos=produtos, opcao=opcao, campo=campo)
    return render_template("produto_resultado.html", produtos=produtos, campo=campo)


@app.route('/produto_editar/<int:id>', methods=['GET', 'POST'])
def produto_editar(id):
    produto = Produto.query.get(id)
    if request.method == 'POST':
        produto.nome = request.form['nome']
        produto.descricao = request.form['descricao']
        produto.valor = request.form['valor']
        produto.isActive = int(request.form['isActive'])
        db.session.commit()
        mensagem_editar = f"Produto {produto.nome.upper()} foi editado(a) COM SUCESSO!"
        return render_template("produto_resultado.html", mensagem_editar=mensagem_editar)
    return render_template('produto_editar.html', produto=produto)


@app.route('/produto_deletar/<int:id>')
def produto_deletar(id):
    produto = Produto.query.get(id)
    produto.isActive = 0
    db.session.commit()
    mensagem_deletar = f"O produto {produto.nome.upper()} foi DELETADO(A)!"
    return render_template("produto_resultado.html", mensagem_deletar=mensagem_deletar)


'''
#   PARA DELETAR DEFINITIVAMENTE O PRODUTO DO BD
@app.route('/produto_deletar2/<int:id>')
def produto_deletar2(id):
    produto = Produto.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    mensagem = f"{produto.nome} foi DELETADO(A)!"
    return render_template("produto_resultado.html", mensagem_deletar=mensagem)
'''
