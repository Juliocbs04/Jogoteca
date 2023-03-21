import psycopg2
from flask_bcrypt import generate_password_hash

from banco import conecta_banco_criado, cria_banco

cria_banco()
conn = conecta_banco_criado()

cursor = conn.cursor()
create_table_jogos = """CREATE TABLE IF NOT EXISTS jogos(
    id SERIAL,
    nome character varying(50) NOT NULL,
    categoria character varying(40) NOT NULL,
    console character varying(20) NOT NULL,
    CONSTRAINT jogos_pkey PRIMARY KEY (id))"""
create_table_usuarios = """CREATE TABLE IF NOT EXISTS usuarios(id_usuario SERIAL,nome character varying(20) NOT NULL,nickname character varying(8) UNIQUE NOT NULL, 
senha character varying(100) NOT NULL, CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario)) """
# create_table_usuarios = "".join(create_table_usuarios.splitlines())
print('Query', create_table_usuarios)
# print('Query', create_table_jogos)
try:
    cursor.execute(create_table_jogos)
except Exception as err:
    print('Oops! An exception has occured:', err)

try:
    cursor.execute(create_table_usuarios)
except Exception as err:
    print('Oops! An exception has occured:', err)

# inserindo usuarios
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) VALUES (%s, %s, %s)'
usuarios = [
      ("Julio Belenke", "julio", generate_password_hash("123").decode('utf-8')),
      ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
      ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
      ("Guilherme Louro", "Cake", generate_password_hash("python_eh_vida").decode('utf-8'))
]
cursor.executemany(usuario_sql, usuarios)

# inserindo jogos
jogos_sql = 'INSERT INTO jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Luta', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Need for Speed', 'Corrida', 'PS2'),
]
cursor.executemany(jogos_sql, jogos)

conn.commit()
cursor.close()
conn.close()
