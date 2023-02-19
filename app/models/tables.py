from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

from app import db

######################################################################
##                        USER - LOGIN                              ##
######################################################################
# A classe User é para o cadastro de funcionários, para que acessem o sistema #


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))

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

    def __init__(self, username, password, email, funcionario):
        self.username = username
        self.password = password
        self.email = email
        self.funcionario = funcionario

    def __repr__(self):  # é uma abreviação de representation (é a saida que terá o print quando puxar a info)
        return "<User %r>" % self.username


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
    #ordemServico = relationship('OrdemServico', backref="funcionarios")
    usuario = relationship('Usuario', backref="funcionarios")

    def __init__(self, nome, email, celular, dataNascimento, dataContrato, funcao):
        self.nome = nome
        self.email = email
        self.celular = celular
        self.dataNascimento = dataNascimento
        self.dataContrato = dataContrato
        self.funcao = funcao


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
    cliente = relationship('Cliente')
    #orcamentos = relationship(Orcamento, backref="veiculos")
    #agendamento = relationship(Agendamento, backref='veiculos')

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
    veiculos = relationship(Veiculo, backref="clientes")

    def __init__(self, nome, email, cpf, celular):
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.celular = celular
