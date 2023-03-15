import psycopg2

print('Conectando...')
try:
      conn = psycopg2.connect(
            host='127.0.0.1',
            user='postgres',
            password='postgres'
      )
except Exception as err:
      print('Oops! An exception has occured:', err)
      print('Exception TYPE:', type(err))

cursor = conn.cursor()

cursor.close()
conn.close()