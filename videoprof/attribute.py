from dataclasses import dataclass
from typing import List, Optional

from .mediainfo import MediaInfoList
from .level import Level, DEFAULT_LEVEL
from .preference import Preference


@dataclass
class Attribute:
    preferences: List[Preference]
    title: str
    track_type: str
    track_attribute: str
    default_level: Level = DEFAULT_LEVEL

    def get_value(self, media_info: MediaInfoList) -> Optional[str]:
        for track in media_info:
            if track["track_type"] == self.track_type:
                return str(track.get(self.track_attribute, ""))

        return None

    def get_preference(self, value: str) -> Preference:
        for preference in self.preferences:
            if preference.match(value):
                return preference

        preference = Preference(level=self.default_level, title=value, pattern=value)
        self.preferences.append(preference)
        return preference
