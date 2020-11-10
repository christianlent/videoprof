import json
import os

from dataclasses import dataclass
from pathlib import Path
from sqlite3 import Connection
from typing import List

from .attribute import Attribute
from .db import get_tracks
from .mediainfo import get_media_info_list, MediaInfoList
from .preference import Preference


@dataclass
class Quality:
    attribute: Attribute
    preference: Preference


class Video:
    path: Path
    filename: str
    qualities: List[Quality]

    def __init__(self, path: Path):
        self.path = path
        self.filename = str(path.absolute())
        self.qualities = []

    def get_media_info_list(self) -> MediaInfoList:
        return get_media_info_list(self.filename)

    def get_cached_media_info_list(self, connection: Connection) -> MediaInfoList:
        size = os.path.getsize(self.filename)
        modified = os.path.getmtime(self.filename)

        return get_tracks(connection, self.filename, size, modified, lambda: self.get_media_info_list())

    def analyze(self, attributes: List[Attribute], connection: Connection) -> None:
        tracks = self.get_cached_media_info_list(connection)

        for attribute in attributes:
            try:
                value = attribute.get_value(tracks)
            except Exception as e:
                print(json.dumps(tracks, indent=4))
                print(f"Error: {self.filename}", e)
                exit(1)

            if not value:
                continue

            preference = attribute.get_preference(value)
            self.qualities.append(Quality(attribute=attribute, preference=preference))
