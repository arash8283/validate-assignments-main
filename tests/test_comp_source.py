import os
from dataclasses import dataclass
from pathlib import Path

import pytest


@dataclass
class CompileState:
    returncode: int


def test_compsource_valid(mocker):
    input = Path("/home/sample/sample.c")
    output = Path(f"/tmp/{os.getenv("APP_NAME", "test")}/sample")
    mocker.patch("tempfile.gettempdir", return_value="/tmp")
    mocker.patch("subprocess.run", return_value=CompileState(returncode=0))

    from app.comp_source import comp_source

    outfile = comp_source(input)
    assert outfile == output


def test_compsource_invalid(mocker):
    student_id: str = "123456789"
    input = Path(f"/home/sample/{student_id}.c")
    mocker.patch("tempfile.gettempdir", return_value="/tmp")

    mocker.patch("subprocess.run", return_value=CompileState(returncode=1))

    from app.comp_source import SourceCompileError, comp_source

    with pytest.raises(
        expected_exception=SourceCompileError,
        check=lambda e: e.student_id == student_id,
    ):
        comp_source(input)
