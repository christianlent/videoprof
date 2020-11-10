import re

from dataclasses import dataclass
from .level import Level, DEFAULT_LEVEL


@dataclass
class Preference:
    title: str
    pattern: str
    level: Level = DEFAULT_LEVEL

    def match(self, target: str) -> bool:
        if self.pattern.isalnum():
            return target == self.pattern
        return bool(re.match(self.pattern, target))

    def __hash__(self) -> int:
        return hash(self.title)
