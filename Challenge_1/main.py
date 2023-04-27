import avro.schema
from flask import Flask, jsonify, request
import json
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from Challenge_1 import envcon as db
from cerberus import Validator
from sqlalchemy.exc import SQLAlchemyError
from itertools import zip_longest
import io
import fastavro

app = Flask(__name__)


def startServer():
    print("test")


# Definir schema AVRO para cada tabla
departments_schema = avro.schema.parse('''
    {
        "type": "record",
        "name": "Department",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "department", "type": "string"}
        ]
    }
''')

hired_employees_schema = avro.schema.parse('''
    {
        "type": "record",
        "name": "Employee",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "name", "type": "string"},
            {"name": "datetime", "type": "string"},
            {"name": "department_id", "type": "int"},
            {"name": "job_id", "type": "int"}
        ]
    }
''')

jobs_schema = avro.schema.parse('''
    {
        "type": "record",
        "name": "Job",
        "fields": [
            {"name": "id", "type": "int"},
            {"name": "job", "type": "string"}
        ]
    }
''')

# schema_departments = {
#     'id': {'type': 'integer', 'required': True},
#     'department': {'type': 'string', 'required': True},
# }
#
# schema_hired_employees = {
#     'id': {'type': 'integer', 'required': True},
#     'name': {'type': 'string', 'required': True},
#     'datetime': {'type': 'string', 'required': True},
#     'department_id': {'type': 'integer', 'required': True},
#     'job_id': {'type': 'integer', 'required': True},
# }
#
# schema_jobs = {
#     'id': {'type': 'integer', 'required': True},
#     'job': {'type': 'string', 'required': True},
# }

Base = declarative_base()


class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    department = Column(String)


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer , primary_key=True)
    job = Column(String)


class HiredEmployee(Base):
    __tablename__ = 'hired_employees'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer)  # ForeignKey('departments.id'))
    job_id = Column(Integer)  # ForeignKey('jobs.id'))

    # department = relationship('Department', backref='hired_employees')
    # job = relationship('Job', backref='hired_employees')


@app.route('/api/cargar_csv', methods=['POST'])
def cargar_csv():
    file = request.files["archivo"]
    if file.filename == "departments.csv":
        dataclass = Department
    elif file.filename == "hired_employees.csv":
        dataclass = HiredEmployee
    elif file.filename == "jobs.csv":
        dataclass = Job
    else:
        return "Archivo CSV no válido"
    db.load_csv_data(file, dataclass)
    return "Datos cargados exitosamente"


@app.route('/api/insert_data_json', methods=['POST'])
def insert_data_json():
    file = request.files['file']
    kind = request.form.get("kind")

    # Load JSON data from uploaded file
    data = json.load(file)

    # Determine which table to insert data into based on "kind" parameter
    table_map = {
        'departments': Department,
        'hired_employees': HiredEmployee,
        'jobs': Job,
    }
    table = table_map.get(kind)
    print(table)
    if table is None:
        return jsonify({'message': 'Invalid kind.'}), 400

        # Validate data against schema
        schema_map = {
            'departments': schema_departments,
            'hired_employees': schema_hired_employees,
            'jobs': schema_jobs}

        schema = schema_map.get(kind)
        v = Validator(schema)
        if not v.validate(data):
            return jsonify({'message': 'Invalid data.', 'errors': v.errors}), 400

    # Insert data into table
    try:
        # Group data into batches of 1000 rows
        batch_size = 1000
        batches = list(zip_longest(*[iter(data)] * batch_size))

        for batch in batches:
            # Remove any None values (if the last batch is shorter than 1000 rows)
            batch = [item for item in batch if item is not None]

            # Insert batch into table
            db.session.add_all([table(**item) for item in batch])
            db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500

    finally:
        db.session.close()

    return jsonify({'message': 'Data inserted successfully.'})


@app.route('/api/backup/<table>', methods=['GET'])
def backup_table(table):
    # Determine which table to backup
    if table == 'departments':
        model = Department
        schema = departments_schema
    elif table == 'jobs':
        model = Job
        schema = jobs_schema
    elif table == 'hired_employees':
        model = HiredEmployee
        schema = hired_employees_schema
    else:
        return jsonify({'message': 'Invalid table name.'}), 400

    # Query database to retrieve all records
    records = db.session.query(model).all()

    # Convert records to AVRO format
    avro_bytes = io.BytesIO()
    fastavro.writer(avro_bytes, schema, records)

    # Save AVRO records to file
    filename = f'{table}.avro'
    with open(filename, 'wb') as f:
        f.write(avro_bytes.getvalue())

    return jsonify({'message': f'{table.capitalize()} backed up to file {filename}.'})


@app.route('/api/restore/<table>/<backup>', methods=['POST'])
def restore_table(table, backup_name):
    # Determine which model to restore
    if table == 'departments':
        model = Department
        schema = departments_schema
    elif table == 'jobs':
        model = Job
        schema = jobs_schema
    elif table == 'hired_employees':
        model = HiredEmployee
        schema = hired_employees_schema
    else:
        return jsonify({'message': 'Invalid table name.'}), 400

    # Read data from backup file in AVRO format
    with open(backup_name, 'rb') as f:
        avro_bytes = f.read()
        records = list(fastavro.reader(io.BytesIO(avro_bytes), schema))

    # Delete existing data in table
    db.session.query(model).delete()

    # Insert data from backup file
    for record in records:
        db.session.add(model(**record))

    # Commit changes to database
    db.session.commit()

    return jsonify({'message': f'{table.capitalize()} restored from backup {backup_name}.'})


if __name__ == '__main__':
    app.run()
