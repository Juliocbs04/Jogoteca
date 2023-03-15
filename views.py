import time

from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models.jogo import Jogo
from models.usuario import Usuario
from helpers import recupera_imagem, deleta_arquivo


@app.route('/')
def index():
    j = Jogo()
    list_games = j.query.order_by(j.id)
    return render_template('lista.html', titulo='Jogos', games=list_games)


@app.route('/novo')
def cadastro():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    jogo = Jogo.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo= capa_jogo)


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
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
    atualiza_jogo = Jogo.query.filter_by(id=request.form['id']).first()
    atualiza_jogo.nome = request.form['nome']
    atualiza_jogo.categoria = request.form['categoria']
    atualiza_jogo.console = request.form['console']
    # estava dando erro usando add com merge funcionou
    db.session.merge(atualiza_jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    if arquivo:
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        deleta_arquivo(atualiza_jogo.id)
        arquivo.save(f'{upload_path}/capa{atualiza_jogo.id}-{timestamp}.jpg')

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
    return render_template('login.html', titulo='Login')


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = Usuario.query.filter_by(nickname=request.form['usuario']).first()

    if usuario:
        if request.form['senha'] == usuario.senha:
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



