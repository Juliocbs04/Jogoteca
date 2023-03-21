import psycopg2
from psycopg2.sql import NULL


def cria_banco():
    conn = conecta_banco()
    cursor = conn.cursor()
    conn.autocommit = True
    cursor.execute('DROP DATABASE jogoteca')
    cursor.execute('CREATE DATABASE jogoteca')

    conn.autocommit = False
    cursor.close()
    conn.close()


def conecta_banco():
    print('Conectando...')
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='postgres'
        )
        return conn
    except Exception as err:
        print('Oops! An exception has occured:', err)
        print('Exception TYPE:', type(err))

    return NULL


def conecta_banco_criado():
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='postgres',
            database='jogoteca'
        )
        return conn
    except Exception as err:
        print('Oops! An exception has occured:', err)
        print('Exception TYPE:', type(err))

    return NULL
