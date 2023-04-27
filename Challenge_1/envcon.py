# Importamos las librerías necesarias
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Department, HiredEmployee, Job, Base


# Clase para definir los parametros de SQL
class SQLConfig:
    def __init__(self, server, database, username, password):
        self.server = server
        self.database = database
        self.username = username
        self.password = password


# Recolecta datos de servidor SQL
sql_data = SQLConfig(server='DyA',
                     database='PruebaGlobant',
                     username='sa',
                     password='123456')


def sql_connect():
    # # conexion de data
    return create_engine(
        f'mssql+pyodbc://{sql_data.username}:{sql_data.password}@{sql_data.server}/{sql_data.database}?driver=ODBC Driver 17 for SQL Server')


engine = sql_connect()

# Crear una sesión a partir del objeto Engine
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def load_csv_data(csv, dataclass):
    if csv.filename == "departments.csv":
        df = pd.read_csv(csv, header=None, names=["id", "department"])
    elif csv.filename == "hired_employees.csv":
        df = pd.read_csv(csv, header=None, names=["id", "name", "datetime", "department_id", "job_id"])
    elif csv.filename == "jobs.csv":
        df = pd.read_csv(csv, header=None, names=["id", "job"])
    else:
        print("Invalid CSV file")

    dataclass_instances = [dataclass(**row) for row in df.to_dict(orient='records')]
    print("pase por aqui")
    table_name = dataclass.__tablename__
    print("same here")
    print(table_name)
    with Session() as ss:
        try:
            print("estas aqui?")
            ss.bulk_save_objects(dataclass_instances)
            print("todo mal")
            ss.commit()
        except Exception as e:
            ss.rollback()
            raise e
        print("me mori")
    print(f"Datos cargados en la tabla {table_name} exitosamente.")
