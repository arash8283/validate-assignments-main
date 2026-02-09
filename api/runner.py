import os
from pathlib import Path
import asyncio

from app.__main__ import main as app_main
from datetime import datetime
from db.db import database, students, reports, ValidationStatusEnum

async def save_results(report_record, report_path):
    total = len(report_record)
    succeeded = sum(1 for r in report_record if r[1] == ValidationStatusEnum.SUCCEEDED)
    compilation_failed = sum(1 for r in report_record if r[1] == ValidationStatusEnum.COMPILATION_FAILED)
    run_failed = sum(1 for r in report_record if r[1] == ValidationStatusEnum.RUN_FAILED)
    invalid_output = sum(1 for r in report_record if r[1] == ValidationStatusEnum.INVALID_OUTPUT)

    query = reports.insert().values(
        run_time=datetime.utcnow(),
        report_path=report_path,
        total=total,
        succeeded=succeeded,
        compilation_failed=compilation_failed,
        run_failed=run_failed,
        invalid_output=invalid_output,
    )
    await database.execute(query)

    for student_id, status in report_record:
        query = students.insert().values(
            student_id=student_id,
            last_status=status,
            last_run=datetime.utcnow()
        ).prefix_with("ON DUPLICATE KEY UPDATE last_status=VALUES(last_status), last_run=VALUES(last_run)")
        await database.execute(query)

async def run_validator(
    assets_dir: Path,
    solution_path: Path,
):
    os.environ["ASSETS_DIR"] = assets_dir.as_posix()
    os.environ["SOLUTION_JSON"] = solution_path.as_posix()
    os.environ["APP_NAME"] = "validate_assignments"
    os.environ["RUN_TIMEOUT_SEC"] = "5"

    await app_main()

    report_path = assets_dir / "Report.md"
    if not report_path.exists():
        raise RuntimeError("Report.md not generated")

    return report_path
