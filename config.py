import os.path  # importa o caminho do bd

# aqui relaciona o caminho exato do db
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
    os.path.join(basedir, 'storage.db')  # mostra o caminho do db
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'Sofisticar_Safe_Key'
