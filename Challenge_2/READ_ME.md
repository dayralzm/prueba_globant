Employee Management System API
This API provides two endpoints to retrieve information about the employees and departments:

* /api/hires_by_dept_job_quarter: Retrieves the number of hires by department, job, and quarter of the year 2021.
* /api/hired_more_than_mean: Retrieves the departments that hired more employees than the mean of employees hired in 2021 for all the departments.

Installation

Clone this repository to your local machine.
Create a virtual environment and activate it:

    python -m venv venv
    source venv/bin/activate

Install the required packages:

    pip install -r requirements.txt

Start the application:

    python app.py

The application will start on port 800.

Endpoints
/api/hires_by_dept_job_quarter
Retrieves the number of hires by department, job, and quarter of the year 2021.

Request
Method: GET
URL: http://localhost:800/api/hires_by_dept_job_quarter
Response
Content-Type: application/json
Body: List of dictionaries containing the following fields:
Department (string): Name of the department.
Job (string): Name of the job.
Q1 (integer): Number of hires in the first quarter of 2021.
Q2 (integer): Number of hires in the second quarter of 2021.
Q3 (integer): Number of hires in the third quarter of 2021.
Q4 (integer): Number of hires in the fourth quarter of 2021.
Example:


    [    {        "Department": "Finance",        "Job": "Accountant",        "Q1": 5,        "Q2": 6,        "Q3": 8,        "Q4": 4    },    {        "Department": "HR",        "Job": "Recruiter",        "Q1": 2,        "Q2": 3,        "Q3": 1,        "Q4": 4    },    ...]

/api/hired_more_than_mean:
Retrieves the departments that hired more employees than the mean of employees hired in 2021 for all the departments.

Request
Method: GET
URL: http://localhost:800/api/hired_more_than_mean
Response
Content-Type: application/json
Body: List of dictionaries containing the following fields:
id (integer): ID of the department.
department (string): Name of the department.
hired (integer): Number of employees hired in 2021.
Example:


    [    {        "id": 7,        "department": "Staff",        "hired": 45    }

Connecting with Power BI
To use this API in Power BI, follow these steps:

Open Power BI and go to the "Home" tab.
Click "Get Data" in the "External Data" section.
Select "Web" and click "Connect".
In the "From Web" dialog box, enter the URL for the API endpoint you want to use (e.g. http://localhost:8000/api/hires_by_dept_job_quarter or http://localhost:8000/api/hired_more_than_mean).
Click "OK" and wait for Power BI to connect to the API and retrieve the data.
Once the data is loaded, you can use it to create reports and dashboards in Power BI.
Please note that you may need to adjust the URL for the API endpoint depending on the host and port of the API server.