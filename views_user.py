from flask import render_template, request, redirect, session, flash, url_for

from forms.UsuarioForms import FormularioUsuario
from jogoteca import app
from models.usuario import Usuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    form = FormularioUsuario()
    return render_template('login.html', titulo='Login', form=form)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)
    if usuario and senha:
        session['usuario_logado'] = usuario.nickname
        flash('Usuario {} foi logado com sucesso!'.format(session['usuario_logado']))
        return redirect(url_for('index'))
    else:
        flash('Erro na autenticação usuário ou senha incorretos', session['usuario_logado'])
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))
