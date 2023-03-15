from sqlalchemy import Column, String
from jogoteca import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    nickname = Column(String(8), primary_key=True)
    senha = Column(String(20), nullable=False)
    nome = Column(String(100), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name

    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha
