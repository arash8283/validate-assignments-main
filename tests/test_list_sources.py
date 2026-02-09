import pytest

from app.list_sources import list_sources


class DirEntryMock:
    name: str

    def __init__(self, name: str):
        self.name = name

    def is_file(self):
        return True

    @property
    def path(self):
        return f"/home/sample/{self.name}"


@pytest.mark.asyncio
async def test_listsources(mocker):
    valid_entries = ["123456789.c", "987654321.c"]
    dir_entries = [*valid_entries, "sample.h", "sample.u", "sample.cpp"]
    mocker.patch(
        "aiofiles.os.scandir",
        return_value=[DirEntryMock(entry) for entry in dir_entries],
    )
    assert (
        [p.name for p in await list_sources()]
    ) == valid_entries, "C Files Are Not The Only Ones Selected!"
