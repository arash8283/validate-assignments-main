"""List C Source Files"""

from pathlib import Path
from typing import Generator

from aiofiles import os as aioos

from app.config import settings


async def list_sources() -> Generator[Path, None]:
    return (
        Path(entry.path)
        for entry in await aioos.scandir(settings.assets_dir)
        if entry.is_file() and entry.name.lower().endswith(".c")
    )
