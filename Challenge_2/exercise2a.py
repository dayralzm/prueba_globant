import pyodbc
from flask import jsonify, Flask


server = 'DyA'
database = 'PruebaGlobant'
username = 'sa'
password = '123456'

app = Flask(__name__)

@app.route('/api/hires_by_dept_job_quarter', methods=['GET'])
def hires_by_dept_job_quarter():
    try:
        conexi = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER=' + server + ';DATABASE='
                                + database + ';UID=' + username + ';PWD=' + password)

    except:
        print("unsuccessful connection")

    # Consulta la base de datos

    cursor = conexi.cursor()
    cursor.execute("SELECT d.department,j.job,COUNT(CASE WHEN DATEPART(QUARTER, e.datetime) = 1 THEN e.id END) AS Q1, "
                   "COUNT(CASE WHEN DATEPART(QUARTER, e.datetime) = 2 THEN e.id END) AS Q2,COUNT(CASE WHEN DATEPART("
                   "QUARTER, e.datetime) = 3 THEN e.id END) AS Q3, COUNT(CASE WHEN DATEPART(QUARTER, e.datetime) = 4 THEN "
                   "e.id END) AS Q4 FROM hired_employees e JOIN departments d ON e.department_id = d.id JOIN jobs j ON "
                   "e.job_id = j.id WHERE YEAR(e.datetime) = 2021 GROUP BY d.department, j.job ORDER BY d.department, "
                   "j.job;")

    result = cursor.fetchall()

    cursor.close()
    conexi.close()

    # creación de la respuesta como un JSON
    data = []
    for row in result:
        data.append({
            'Department': row[0],
            'Job': row[1],
            'Q1': row[2],
            'Q2': row[3],
            'Q3': row[4],
            'Q4': row[5]
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run()