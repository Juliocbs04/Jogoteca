import os

from wtforms import StringField, validators, SubmitField

from jogoteca import app
from flask_wtf import FlaskForm


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

    return 'padrao.jpg'


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)

    if arquivo != 'padrao.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')
