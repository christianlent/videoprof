from dataclasses import dataclass

import colored
from colored import stylize


@dataclass(frozen=True)
class Level:
    color: str = ""
    flag: bool = False

    def render(self, input: str) -> str:
        if not self.color:
            return input
        return stylize(input, colored.fg(self.color))


DEFAULT_LEVEL = Level()
