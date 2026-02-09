import tempfile
from os import getenv, makedirs
from pathlib import Path
import sys
from functools import cached_property


class Settings:
    @cached_property
    def assets_dir(self) -> str:
        _ASSETS_DIR = getenv("ASSETS_DIR")
        assert _ASSETS_DIR, "ASSERT_DIR env not defined!"
        return Path(_ASSETS_DIR).expanduser().as_posix()

    @cached_property
    def tmpdir(self) -> Path:
        _APP_NAME = getenv("APP_NAME")
        assert _APP_NAME, "APP_NAME env not defined"
        result = Path(tempfile.gettempdir()) / _APP_NAME
        makedirs(result)
        return result

    @cached_property
    def solution_json(self) -> str:
        _SOLUTION_JSON = getenv("SOLUTION_JSON")
        assert _SOLUTION_JSON, "SOLUTION_JSON env not defined!"
        return Path(_SOLUTION_JSON).expanduser().as_posix()

    @cached_property
    def run_timeout_sec(self) -> int:
        _RUN_TIMEOUT_SEC = getenv("RUN_TIMEOUT_SEC", "5")
        return int(_RUN_TIMEOUT_SEC)

    report_md: str = "Report.md"


class MockedSettings:
    assets_dir: str = "test"
    tmpdir: Path = Path(f"/tmp/test")
    solution_json: str = "sample.json"
    run_timeout_sec: int = 5
    report_md: str = "Report.md"


settings = Settings() if not "pytest" in sys.modules else MockedSettings()
