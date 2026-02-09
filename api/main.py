import tempfile
import uuid
import zipfile
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse

from api.runner import run_validator
from db.db import database, students

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(title="Validate Assignments API", lifespan=lifespan)


@app.post("/validate")
async def validate_assignment(
    solution: UploadFile = File(...),
    sources: UploadFile = File(...),  # zip of .c files
):
    run_id = str(uuid.uuid4())

    base_dir = Path(tempfile.gettempdir()) / f"run_{run_id}"
    assets_dir = base_dir / "assets"
    assets_dir.mkdir(parents=True)

    solution_path = base_dir / "solution.json"
    solution_path.write_bytes(await solution.read())

    zip_path = base_dir / "sources.zip"
    zip_path.write_bytes(await sources.read())

    with zipfile.ZipFile(zip_path) as z:
        z.extractall(assets_dir)

    try:
        report_path = await run_validator(
            assets_dir=assets_dir,
            solution_path=solution_path,
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return FileResponse(
        report_path,
        media_type="text/markdown",
        filename="Report.md",
    )


@app.get("/students", response_model=list[dict])
async def get_students_status():
    query = students.select()
    rows = await database.fetch_all(query)

    # تبدیل هر رکورد به دیکشنری ساده
    result = [
        {
            "student_id": row["student_id"],
            "last_status": row["last_status"],
            "last_run": row["last_run"].isoformat(),  # datetime -> string
        }
        for row in rows
    ]
    return result
