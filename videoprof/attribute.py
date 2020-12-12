import re

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List, Optional, Sequence

from .exceptions import MissingAttributeError
from .level import Level, DEFAULT_LEVEL
from .mediainfo import MediaInfoList
from .preference import Preference, SinglePreference


class Attribute(ABC):
    @abstractmethod
    def get_preference(self, media_info: MediaInfoList) -> Preference:
        raise NotImplementedError

    @abstractmethod
    def get_title(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_preferences(self) -> Sequence[Preference]:
        raise NotImplementedError


@dataclass
class SingleAttribute(Attribute):
    preferences: List[Preference]
    title: str
    track_type: str
    track_attribute: str
    default_level: Level = DEFAULT_LEVEL
    render: str = "%s"
    missing_value: Optional[str] = None

    def get_value(self, media_info: MediaInfoList) -> Optional[str]:
        for track in media_info:
            if track["track_type"] == self.track_type:
                value = track.get(self.track_attribute, None)
                return None if value is None else str(value)

        return None

    def get_preference(self, media_info: MediaInfoList) -> Preference:
        value = self.get_value(media_info) or self.missing_value

        if not value:
            raise MissingAttributeError(f"Value missing for {self.track_type}:{self.track_attribute}")

        for preference in self.preferences:
            if preference.match(value):
                return preference

        preference = SinglePreference(
            level=self.default_level, title=self.render % (value), pattern=re.escape(value)
        )
        self.preferences.append(preference)
        return preference

    def get_title(self) -> str:
        return self.title

    def get_preferences(self) -> Sequence[Preference]:
        return self.preferences


@dataclass
class CompositeAttribute(Attribute):
    preferences: List[Preference]
    attributes: List[Attribute]
    title: str
    default_level: Level = DEFAULT_LEVEL
    render: str = "%s"

    def get_preference(self, media_info: MediaInfoList) -> Preference:
        all_values_missing = True
        value_list = []
        for attribute in self.attributes:
            try:
                value_list.append(attribute.get_preference(media_info).get_title())
                all_values_missing = False
            except MissingAttributeError:
                pass

        if all_values_missing:
            raise MissingAttributeError(f"All values missing for composite attribute '{self.title}''")

        value = "".join(value_list)

        for preference in self.preferences:
            if preference.match(value):
                return preference

        preference = SinglePreference(
            level=self.default_level, title=self.render % (value), pattern=re.escape(value)
        )
        self.preferences.append(preference)
        return preference

    def get_title(self) -> str:
        return self.title

    def get_preferences(self) -> Sequence[Preference]:
        return self.preferences
