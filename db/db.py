from databases import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, Enum, DateTime
import enum
import datetime

DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3306/validate_db"

database = Database(DATABASE_URL)
metadata = MetaData()


class ValidationStatusEnum(str, enum.Enum):
    COMPILATION_FAILED = "COMPILATION_FAILED"
    RUN_FAILED = "RUN_FAILED"
    INVALID_OUTPUT = "INVALID_OUTPUT"
    SUCCEEDED = "SUCCEEDED"


students = Table(
    "students",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("student_id", String(20), unique=True),
    Column("last_status", Enum(ValidationStatusEnum)),
    Column("last_run", DateTime, default=datetime.datetime.utcnow),
)

reports = Table(
    "reports",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("run_time", DateTime, default=datetime.datetime.utcnow),
    Column("report_path", String(255)),
    Column("total", Integer),
    Column("succeeded", Integer),
    Column("compilation_failed", Integer),
    Column("run_failed", Integer),
    Column("invalid_output", Integer),
)
