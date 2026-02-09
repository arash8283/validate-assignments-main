import json
from dataclasses import dataclass


@dataclass
class SolutionModel:
    input: list[str]
    output: list[str]

    @staticmethod
    def model_validate(arg: dict) -> SolutionModel:
        instance = SolutionModel(**arg)
        if (
            list(instance.__dict__.keys()) == ["input", "output"]
            and isinstance(instance.input, list)
            and isinstance(instance.output, list)
            and all([isinstance(x, str) for x in instance.input])
            and all([isinstance(x, str) for x in instance.output])
        ):
            return instance
        raise UnsupportedSolutionFormat()


async def parse_solution(src: str) -> SolutionModel:
    """
    Parse Solution And Returns According Model

    :raise UnsupportedSolutionFormat:
    :return: Serialized
    :rtype: SolutionModel
    """
    value = json.loads(src)
    if isinstance(value, dict):
        return SolutionModel.model_validate(value)

    raise UnsupportedSolutionFormat()


class UnsupportedSolutionFormat(RuntimeError):
    """Unsupported Solution Format Error For Solution File Provided To Application"""

    def __init__(self):
        super().__init__(
            self,
            "solution must contain an object with two attributes: output & input which are lists of strings",
        )
