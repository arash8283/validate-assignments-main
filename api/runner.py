import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.__main__ import ReportItem
from app.__main__ import main as app_main
from db.db import ValidationStatusEnum, database, reports, students


class Runner:
    _assets_dir: Path
    _solution_dir: Path
    _report_record: Optional[list[ReportItem]]
    _report_path: Path

    def __init__(
        self,
        assets_dir: Path,
        solution_dir: Path,
    ) -> None:
        self._assets_dir = assets_dir
        self._solution_dir = solution_dir
        self._report_path = assets_dir / "Report.md"

    @property
    def report_path(self) -> Path:
        return self._report_path

    def _setup_env(self):
        os.environ["ASSETS_DIR"] = self._assets_dir.as_posix()
        os.environ["SOLUTION_JSON"] = self._solution_dir.as_posix()
        os.environ["APP_NAME"] = "validate_assignments"
        os.environ["RUN_TIMEOUT_SEC"] = "5"

    async def run(self):
        self._setup_env()
        self._report_record = await app_main()
        if not self._report_path.exists():
            raise RuntimeError("Report.md not generated")

    async def save(self):
        assert self._report_record, "did you forgot to call run first?"

        total = len(self._report_record)
        succeeded = sum(
            1 for r in self._report_record if r[1] == ValidationStatusEnum.SUCCEEDED
        )
        compilation_failed = sum(
            1
            for r in self._report_record
            if r[1] == ValidationStatusEnum.COMPILATION_FAILED
        )
        run_failed = sum(
            1 for r in self._report_record if r[1] == ValidationStatusEnum.RUN_FAILED
        )
        invalid_output = sum(
            1
            for r in self._report_record
            if r[1] == ValidationStatusEnum.INVALID_OUTPUT
        )

        query = reports.insert().values(
            run_time=datetime.utcnow(),
            report_path=self._report_path,
            total=total,
            succeeded=succeeded,
            compilation_failed=compilation_failed,
            run_failed=run_failed,
            invalid_output=invalid_output,
        )
        await database.execute(query)

        for student_id, status in self._report_record:
            query = (
                students.insert()
                .values(
                    student_id=student_id,
                    last_status=status,
                    last_run=datetime.utcnow(),
                )
                .prefix_with(
                    "ON DUPLICATE KEY UPDATE last_status=VALUES(last_status), last_run=VALUES(last_run)"
                )
            )
            await database.execute(query)
