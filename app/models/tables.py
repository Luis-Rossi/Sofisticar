# QUANDO HOUVER ALTERAÇÃO NA ESTRUTURA DO BD:
#   - DELETAR O STORAGE.DB E PASTA MIGRATIONS
#   - RODAR OS COMANDOS python run.py db init || python run.py db migrate || python .\run.py db upgrade

from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from app import db

######################################################################
##                        USER - LOGIN                              ##
######################################################################


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    isActive = db.Column(db.Boolean, default=1, nullable=False)

# esses property abaixo são necessários para o flask-login #
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, email, funcionario_id):
        self.username = username
        self.password = password
        self.email = email
        self.funcionario_id = funcionario_id

    def __repr__(self):  # é uma abreviação de representation (é a saida que terá o print quando puxar a info)
        return "<User %r>" % self.username

    def retorna_nome_funcionario(self, funcionario_id):
        funcionario = Funcionario.query.get(funcionario_id)
        return funcionario.nome

    def user_esta_ativo(usuario):
        if usuario.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                         FUNCIONÁRIO                              ##
######################################################################

class Funcionario(db.Model):
    __tablename__ = "funcionarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    celular = db.Column(db.String(150), nullable=False)
    dataNascimento = db.Column(db.String(10), nullable=False)
    dataContrato = db.Column(db.String(10), nullable=False)
    funcao = db.Column(db.String(150), nullable=False)
    isActive = db.Column(db.Boolean, default=1, nullable=False)
    ordemServico = relationship('OrdemServico', back_populates="funcionario")
    usuario = relationship(Usuario, backref="funcionarios")

    def __init__(self, nome, email, celular, dataNascimento, dataContrato, funcao):
        self.nome = nome
        self.email = email
        self.celular = celular
        self.dataNascimento = dataNascimento
        self.dataContrato = dataContrato
        self.funcao = funcao

    def formata_data_nascimento(funcionario):
        data_nasc_formatada = datetime.strptime(
            funcionario.dataNascimento, '%Y-%m-%d')
        return data_nasc_formatada

    def formata_data_contrato(funcionario):
        data_contr_formatada = datetime.strptime(
            funcionario.dataContrato, '%Y-%m-%d')
        return data_contr_formatada

    def func_esta_ativo(funcionario):
        if funcionario.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                           CLIENTE                                ##
######################################################################


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(150), primary_key=True)
    celular = db.Column(db.String(150), nullable=False)
    veiculo = relationship('Veiculo', back_populates='cliente')
    isActive = db.Column(db.Boolean, default=1, nullable=False)

    def __init__(self, nome, email, cpf, celular):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.celular = celular

    def cliente_esta_ativo(cliente):
        if cliente.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                           VEÍCULO                                ##
######################################################################


class Veiculo(db.Model):
    __tablename__ = "veiculos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(150), nullable=False)
    modelo = db.Column(db.String(150), nullable=False)
    cor = db.Column(db.String(150), nullable=False)
    placa = db.Column(db.String(150), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    cliente = relationship(Cliente, back_populates='veiculo')
    isActive = db.Column(db.Boolean, default=1, nullable=False)
    orcamentos = relationship('Orcamento', back_populates="veiculo")
    agendamento = relationship('Agendamento', back_populates='veiculo')

    def __init__(self, marca, modelo, cor, placa, cliente):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.placa = placa
        self.cliente = cliente

    def veiculo_esta_ativo(veiculo):
        if veiculo.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                           SERVIÇO                                ##
######################################################################


class Servico(db.Model):
    __tablename__ = 'servicos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, default=1, nullable=False)
    orcamentos = relationship('Orcamento', back_populates="servico")

    def __init__(self, nome, descricao, valor):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

    def servico_esta_ativo(servico):
        if servico.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                           PRODUTO                                ##
######################################################################


class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, default=1, nullable=False)
    orcamentos = relationship('Orcamento', back_populates="produto")

    def __init__(self, nome, descricao, valor):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor

    def produto_esta_ativo(produto):
        if produto.isActive == 1:
            return "SIM"
        else:
            return "NÃO"


######################################################################
##                           ORÇAMENTO                              ##
######################################################################


class Orcamento(db.Model):
    __tablename__ = "orcamento"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.JSON, nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'))
    veiculo = relationship(Veiculo, back_populates="orcamentos")
    servico_id = db.Column(db.JSON, db.ForeignKey('servicos.id'))
    servico = relationship(Servico, back_populates="orcamentos")
    produto_id = db.Column(db.JSON, db.ForeignKey('produtos.id'))
    produto = relationship(Produto, back_populates="orcamentos")
    agendamento = relationship('Agendamento', back_populates="orcamento")
    ordemServico = relationship('OrdemServico', back_populates="orcamento")

    def __init__(self, status, veiculo_id, servico_id, produto_id):
        self.status = status
        self.veiculo_id = veiculo_id
        self.servico_id = servico_id
        self.produto_id = produto_id

    def retorna_valor(self, servico_id, produto_id):
        valor_total = 0
        for serv in servico_id:
            for item in servico_id[serv]:
                servico = Servico.query.get(item)
                valor_total += servico.valor
        for prod in produto_id:
            for item in produto_id[prod]:
                produto = Produto.query.get(item)
                valor_total += produto.valor
        return valor_total

    def status_orc(self):
        status = {
            '1': 'Criado',
            '2': 'Aprovado',
            '3': 'Cancelado',
        }
        return status

    def retorna_status_orc(self, status_id):
        lista = self.status_orc()
        status = lista[status_id]
        return status


######################################################################
##                          AGENDAMENTO                             ##
######################################################################


class Agendamento(db.Model):
    __tablename__ = "agendamento"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    data_atual = db.Column(db.DateTime, default=datetime.now)
    data_agendamento = db.Column(db.DateTime, default=None)
    status = db.Column(db.JSON, nullable=False)
    veiculo_id = db.Column(db.Integer, db.ForeignKey('veiculos.id'))
    veiculo = relationship(Veiculo, back_populates="agendamento")
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'))
    orcamento = relationship(Orcamento, back_populates="agendamento")

    def __init__(self, data_agendamento, veiculo_id, orcamento_id, status):
        self.data_agendamento = data_agendamento
        self.veiculo_id = veiculo_id
        self.orcamento_id = orcamento_id
        self.status = status

    def status_agendamento(self):
        status = {
            '1': 'Criado',
            '2': 'Confirmado',
            '3': 'Cancelado',
            '4': 'Finalizado'
        }
        return status

    def retorna_status_agendamento(self, status_id):
        lista = self.status_agendamento()
        status = lista[status_id]
        return status


######################################################################
##                       ORDEM DE SERVIÇO                           ##
######################################################################


class OrdemServico(db.Model):
    __tablename__ = "ordemServico"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.JSON, nullable=False)
    orcamento_id = db.Column(db.Integer, db.ForeignKey('orcamento.id'))
    orcamento = relationship(Orcamento, back_populates="ordemServico")
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    funcionario = relationship(Funcionario, back_populates="ordemServico")
    descricao = db.Column(db.String(250), default=None)

    def __init__(self, status, orcamento_id, funcionario_id, descricao):
        self.status = status
        self.orcamento_id = orcamento_id
        self.funcionario_id = funcionario_id
        self.descricao = descricao

    def status_os(self):
        status = {
            '1': 'Criado',
            '2': 'Aprovado',
            '3': 'Cancelado',
            '4': 'Em execução',
            '5': 'Finalizado'
        }
        return status

    def retorna_status_os(self, status_id):
        lista = self.status_os()
        status = lista[status_id]
        return status
