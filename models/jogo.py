from sqlalchemy import Column, Integer, String
from jogoteca import db


class Jogo(db.Model):
    __tablename__ = 'jogos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    categoria = Column(String(40), nullable=False)
    console = Column(String(20), nullable=False)

    def __repr__(self):
        return '<Name %r>' % self.name
