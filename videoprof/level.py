import colored
from colored import stylize
from dataclasses import dataclass
from typing import cast


@dataclass
class Level:
    color: str = ""
    flag: bool = False

    def render(self, input: str) -> str:
        if not self.color:
            return input
        return cast(str, stylize(input, colored.fg(self.color)))


DEFAULT_LEVEL = Level()
