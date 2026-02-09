Validate Assignments






A FastAPI-based system to automatically compile, run, and validate student C assignments and generate Markdown reports, with optional MySQL database integration for tracking student statuses and reports.

Table of Contents

Features

Project Structure

Installation

Usage

API Documentation

Database

Docker

Contributing

License

Features

Compile student C source code and detect compilation errors

Run executables with input from solution.json

Compare output to expected results and generate report.md

Async execution for faster batch processing

REST API using FastAPI with Swagger UI

Optional MySQL database for tracking student statuses and reports

Dockerized for easy deployment

Project Structure
validate-assignments/
├─ app/
│  ├─ __main__.py          # Main runner
│  ├─ comp_source.py       # Compile C source code
│  ├─ gen_report.py        # Generate Markdown reports
│  ├─ list_sources.py      # List student source files
│  ├─ parse_solution.py    # Parse solution.json
│  ├─ run_bin.py           # Run compiled binary
│  ├─ solution_file/
│  │   ├─ __init__.py
│  │   └─ reader.py        # Read solution.json
│  └─ config.py            # Configurations (tmpdir, assets_dir)
├─ assets/                 # Folder for uploaded source files
├─ test/                   # Unit tests
├─ api/                    # FastAPI endpoints
│  ├─ main.py
│  └─ runner.py
├─ Dockerfile
├─ requirements.txt
└─ README.md

Installation
1. Clone the repository
git clone https://github.com/arash8283/validate-assignments-main.git
cd validate-assignments

2. Create Python environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3. Install dependencies
pip install -r requirements.txt

4. Environment variables

Create .env or set the following:

ASSETS_DIR=/path/to/assets
SOLUTION_JSON=/path/to/solution.json
APP_NAME=validate_assignments
RUN_TIMEOUT_SEC=5

Usage
Run locally
uvicorn api.main:app --reload


Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Run main program manually
python -m app.__main__


This will:

Read solution.json

Compile all .c files in assets/

Execute each binary and compare output

Generate Report.md in the assets/ folder

API Documentation
POST /validate

Upload solution.json and a ZIP of C source files

Returns Report.md as a downloadable file

GET /students

Returns JSON list of all students and their last validation status

Example response:

[
  {
    "student_id": "12345",
    "last_status": "SUCCEEDED",
    "last_run": "2026-02-09T14:20:00"
  },
  {
    "student_id": "23456",
    "last_status": "COMPILATION_FAILED",
    "last_run": "2026-02-09T14:20:00"
  }
]

Database

Optional MySQL integration:

students table: tracks student_id, last_status, last_run

reports table: tracks run summaries and report paths

Example SQL:

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE,
    last_status ENUM('COMPILATION_FAILED','RUN_FAILED','INVALID_OUTPUT','SUCCEEDED'),
    last_run DATETIME
);

CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    run_time DATETIME,
    report_path VARCHAR(255),
    total INT,
    succeeded INT,
    compilation_failed INT,
    run_failed INT,
    invalid_output INT
);


Python async connection uses:

from databases import Database
database = Database("mysql+mysqlconnector://user:password@localhost:3306/validate_db")
await database.connect()

Docker

Build and run with Docker:

docker build -t validate-assignments .
docker run -p 8000:8000 -e ASSETS_DIR=/assets -e SOLUTION_JSON=/assets/solution.json validate-assignments


Swagger UI: http://localhost:8000/docs
