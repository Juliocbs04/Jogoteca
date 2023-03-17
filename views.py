import time

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory

from forms.UsuarioForms import FormularioUsuario
from jogoteca import app, db
from models.jogo import Jogo
from models.usuario import Usuario
from helpers import recupera_imagem, deleta_arquivo, FormularioJogo


@app.route('/')
def index():
    j = Jogo()
    list_games = j.query.order_by(j.id)
    return render_template('lista.html', titulo='Jogos', games=list_games)


@app.route('/novo')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    form = FormularioJogo()
    return render_template('novo.html', titulo='Novo Jogo', form=form)


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    jogo = Jogo.query.filter_by(id=id).first()
    form = FormularioJogo()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console

    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', id=id, capa_jogo=capa_jogo, form=form)


@app.route('/criar', methods=['POST', ])
def criar():
    form = FormularioJogo(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
    jogo = Jogo.query.filter_by(nome=nome).first()

    if jogo:
        flash('O jogo já existe na base de dados')
        return redirect(url_for('index'))

    novo_jogo = Jogo(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    if arquivo:
        upload_path = app.config['UPLOAD_PATH']
        time_stamp = time.time()
        arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{time_stamp}.jpg')

    return redirect(url_for('index'))


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    form = FormularioJogo(request.form)

    if form.validate_on_submit():
        novo_jogo = Jogo.query.filter_by(id=request.form['id']).first()
        novo_jogo.nome = form.nome.data
        novo_jogo.categoria = form.categoria.data
        novo_jogo.console = form.console.data
        # estava dando erro usando add com merge funcionou
        db.session.add(novo_jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        if arquivo:
            upload_path = app.config['UPLOAD_PATH']
            timestamp = time.time()
            deleta_arquivo(novo_jogo.id)
            arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.jpg')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    jogo = Jogo.query.filter_by(id=id).first()
    db.session.delete(jogo)
    db.session.commit()
    flash('Jogo foi excluido com Sucesso!!')

    return redirect(url_for('index'))


@app.route('/login')
def login():
    form = FormularioUsuario()
    return render_template('login.html', titulo='Login', form=form)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    form = FormularioUsuario(request.form)
    usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()

    if usuario:
        if form.senha.data == usuario.senha:
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


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)
