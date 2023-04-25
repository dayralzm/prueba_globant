import pandas as pd
from flask import Flask, jsonify, request
import pyodbc
import json

server = 'DyA'
database = 'PruebaGlobant'
username = 'sa'
password = '123456'

# Conexión a la base de datos
app = Flask(__name__)

@app.route('/')
def hello():
    return '¡Hola, mundo!'

@app.route('/api/suma/<int:num1>/<int:num2>', methods=['GET'])
def suma(num1, num2):
    resultado = num1 + num2
    return f'La suma de {num1} y {num2} es: {resultado}'

@app.route('/api/data')
def get_data():
    # Conexión a la base de datos
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          f'SERVER={server};'
                          f'DATABASE={database};'
                          f'UID={username};'
                          f'PWD={password}')
    cursor = cnxn.cursor()

    # Ejecución de la consulta
    cursor.execute('SELECT * FROM jobs')

    # Creación de la lista de diccionarios
    data = {'data': []}

    # Agregación de los datos al diccionario
    for row in cursor:
        job = {'id': row[0], 'job': row[1]}
        data['data'].append({'jobs': job})

    # Cierre de la conexión y el objeto cursor
    cursor.close()
    cnxn.close()

    # Conversión de la lista de diccionarios a objeto JSON
    json_data = json.dumps(data)

    # Devolución de la respuesta como objeto JSON
    return jsonify(data), 200, {'Content-Type': 'application/json'}

@app.route('/cargar_csv', methods=['POST'])
def cargar_csv():
    if request.method == 'POST':
        archivo_csv = request.files['archivo_csv']
        nombre_tabla = request.form['nombre_tabla']
        # procesar el archivo_csv
        df = pd.read_csv(archivo_csv)
        # guardar los datos en la base de datos

        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              f'SERVER={server};'
                              f'DATABASE={database};'
                              f'UID={username};'
                              f'PWD={password}')

        cursor = cnxn.cursor()
        cursor.execute(f'CREATE TABLE {nombre_tabla} (id INT, job VARCHAR(50))')

        df.to_sql(nombre_tabla, cnxn, if_exists='append', index=False)
        cursor.close()
        cnxn.close()
        return f"update table {nombre_tabla}"
    return "Test"


@app.route('/create_table', methods=['POST'])
def crear_table():
    if request.method == 'POST':
        # guardar los datos en la base de datos

        cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              f'SERVER={server};'
                              f'DATABASE={database};'
                              f'UID={username};'
                              f'PWD={password}')

        # Ejecutar una consulta para recuperar los nombres de todas las tablas
        cursor = cnxn.cursor()
        cursor.execute("CREATE TABLE jobspost (id INT, job VARCHAR(50))")
        cnxn.commit()
        # tables = cursor.fetchall()
        #
        # # Imprimir los nombres de las tablas
        # for table in tables:
        #     print(table[0])

        # Cerrar la conexión
        cnxn.close()
        return "update table"
    return "Test"


if __name__ == '__main__':
    app.run()