import os
from contextlib import asynccontextmanager
from pathlib import Path

from aiofiles import open as aioopen

from app.config import settings


@asynccontextmanager
async def read_solution():
    async with aioopen(settings.solution_json, "r") as f:
        yield await f.read()
