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
    #ordemServico = relationship('OrdemServico', backref="funcionarios")
    usuario = relationship('Usuario', backref="funcionarios")

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

    def esta_ativo(funcionario):
        if funcionario.isActive == 1:
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
    cliente = relationship('Cliente', back_populates='veiculo')
    #orcamentos = relationship(Orcamento, backref="veiculo")
    #agendamento = relationship(Agendamento, backref='veiculo')

    def __init__(self, marca, modelo, cor, placa, cliente):
        self.marca = marca
        self.modelo = modelo
        self.cor = cor
        self.placa = placa
        self.cliente = cliente


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
    veiculo = relationship(Veiculo, back_populates='cliente')

    def __init__(self, nome, email, cpf, celular):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.celular = celular
