import json

import pytest

from app.parse_solution import UnsupportedSolutionFormat, parse_solution

valid_cases: list[tuple[str, dict]] = [
    ("Simple", {"input": ["in"], "output": ["out"]}),
    ("Complex", {"input": ["one", "two", "three"], "output": ["line1", "line2"]}),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input", ids=(c[0] for c in valid_cases), argvalues=(c[1] for c in valid_cases)
)
async def test_parsesolution_valid(input: dict):
    solution = await parse_solution(json.dumps(input))
    assert solution.input == input.get("input")
    assert solution.output == input.get("output")


invalid_cases: list[tuple[str, dict]] = [
    ("Simple", {"input": [2, 4], "output": [3]}),
    ("Complex", {"input": ["2", "4"], "output": [dict()]}),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input",
    ids=(c[0] for c in invalid_cases),
    argvalues=(c[1] for c in invalid_cases),
)
async def test_parsesolution_invalid(input: dict):
    with pytest.raises(expected_exception=UnsupportedSolutionFormat):
        await parse_solution(json.dumps(input))
