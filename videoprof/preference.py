import re

from abc import abstractmethod, ABC
from dataclasses import dataclass
from .level import Level, DEFAULT_LEVEL


class Preference(ABC):
    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def match(self, target: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_flagged(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def render(self, input: str) -> str:
        raise NotImplementedError


@dataclass
class SinglePreference(Preference):
    title: str
    pattern: str
    level: Level = DEFAULT_LEVEL

    def get_title(self) -> str:
        return self.title

    def match(self, target: str) -> bool:
        if self.pattern.isalnum():
            return target == self.pattern
        return bool(re.match(self.pattern, target))

    def __hash__(self) -> int:
        return hash(self.title)

    def is_flagged(self) -> bool:
        return self.level.flag

    def render(self, input: str) -> str:
        return self.level.render(input)
