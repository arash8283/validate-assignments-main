"""Compile Sources Into Temp Files"""

import subprocess
from pathlib import Path

from app.config import settings


def comp_source(src_path: Path) -> Path:
    """
    Compile Sources To Binaries

    :param src_path: Path To C Source File
    :type src_path: str
    :raise SourceCompileError: Error containing student id
    :return: Exe Path
    :rtype: str
    """

    outfile = settings.tmpdir / src_path.stem

    process = subprocess.run(
        ["gcc", src_path.as_posix(), "-o", outfile], encoding="utf-8"
    )
    if process.returncode != 0:
        raise SourceCompileError(s_id=src_path.stem)

    return outfile


class SourceCompileError(Exception):
    """Unable To Compile Source Code"""

    student_id: str

    def __init__(self, s_id: str):
        super().__init__(self)
        self.student_id = s_id
