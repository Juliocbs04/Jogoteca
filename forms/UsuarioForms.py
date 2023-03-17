from flask_wtf import FlaskForm
from wtforms import StringField, validators, PasswordField, SubmitField


class FormularioUsuario(FlaskForm):
    nickname = StringField('Usuario', [validators.DataRequired(), validators.Length(min=1, max=8)])
    senha = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')
