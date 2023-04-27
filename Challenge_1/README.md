******
envcon.py
*********
Project Description
This project is designed to load data from CSV files into a SQL database using Python. The project uses the pandas library to read CSV files and the sqlalchemy library to interact with the SQL database. The data is loaded into SQL tables using classes defined in main.py.

Prerequisites
To use this project, you will need to have the following installed:

Python 3.5 or later
pandas library
sqlalchemy library

How to Use
1.Clone the repository to your local machine.
2.Create a SQL database with the appropriate tables. The classes used to define the tables are located in main.py.
3.Update the SQLConfig object in envcon.py with your server, database, username, and password.
4.Run envcon.py to load the CSV data into the SQL tables.


load_csv_data Function

.The load_csv_data function is used to load data from CSV files into the corresponding SQL tables. It takes two arguments: csv and dataclass. csv represents the CSV file to be loaded, and dataclass represents the corresponding SQL table.
The function starts by checking which CSV file is being loaded by checking the filename attribute of the csv argument. Depending on the file being loaded, the function will read in the CSV file with pandas and name the columns appropriately.
After loading the CSV data, the function will create instances of the dataclass for each row in the CSV file using a dictionary comprehension. The instances are created by passing the row data as keyword arguments to the dataclass constructor.
Finally, the function uses a Session object to bulk save the instances to the corresponding SQL table. If an error occurs during this process, the function will roll back the session and raise the exception.

Example Usage
To load the departments.csv file into the Department SQL table, you can use the following code:


    from main import Department, Base
    from envcon import load_csv_data
    
    # Create the SQL tables if they do not already exist
    Base.metadata.create_all(engine)
    
    # Load the data from the CSV file
    load_csv_data(open('departments.csv', 'r'), Department)

This code will read in the "departments.csv" file and create instances of the Department class for each row in the file. The instances will be bulk saved to the departments SQL table. The same process can be used to load the other CSV files into their corresponding SQL tables.

******
main.py
*********

Project Description
This project is a RESTful API that provides a way to interact with a SQL Server database by performing various CRUD operations. The API was developed using Flask and SQLAlchemy, and it provides endpoints for uploading data from CSV files or JSON objects to the database, backing up the database to an Avro file, and querying the data in the database.

Requirements
avro.schema
flask
json
sqlalchemy
cerberus
itertools
io
fastavro

Usage
* Setting up the Database
1.Ensure that SQL Server is installed and running.
2.Create a new database in SQL Server.
3.Update the envcon.py file with the connection details of the SQL Server database.
* Running the API
1.Clone the repository.
2.Start the Flask server by running python app.py.

* API Endpoints
POST /api/cargar_csv
This endpoint allows you to upload CSV files to the database. The endpoint expects a POST request with a file named archivo in the request body. The filename of the CSV file should be either departments.csv, hired_employees.csv, or jobs.csv, and the data will be loaded into the corresponding table in the database.

POST /api/insert_data_json
This endpoint allows you to upload JSON objects to the database. The endpoint expects a POST request with a file named file in the request body and a parameter named kind in the request form. The kind parameter should be set to either departments, hired_employees, or jobs, and the data will be inserted into the corresponding table in the database.

GET /api/backup/<table>
This endpoint allows you to backup the contents of a table in the database to an Avro file. The endpoint expects a GET request with the name of the table as a parameter. The Avro file will be generated and returned as a response.

GET /api/<table>
This endpoint allows you to retrieve the contents of a table in the database. The endpoint expects a GET request with the name of the table as a parameter. The contents of the table will be returned as a JSON response.


FUNCTION

backup_table(table): This function is used to backup the data from the specified table in AVRO format. To use this function, you can make a GET request to the endpoint /api/backup/<table> where <table> is the name of the table you want to backup. For example, to backup the data from the "departments" table, you would make a GET request to the endpoint /api/backup/departments. The function will then retrieve all records from the specified table, convert them to AVRO format, and save them to a file named <table>.avro in the current working directory.

restore_table(table, backup_name): This function is used to restore data from a backup file in AVRO format to the specified table. To use this function, you can make a POST request to the endpoint /api/restore/<table>/<backup> where <table> is the name of the table you want to restore data to, and <backup> is the name of the backup file in AVRO format. For example, to restore data from the "departments" table using a backup file named "departments_backup.avro", you would make a POST request to the endpoint /api/restore/departments/departments_backup.avro. The function will then read the data from the backup file, delete all existing data in the specified table, and insert the data from the backup file.

