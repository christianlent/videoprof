import json
import os

from abc import abstractmethod, ABC
from pathlib import Path
from sqlite3 import Connection
from typing import List, Optional, Sequence

from .attribute import Attribute
from .db import get_tracks
from .exceptions import MissingAttributeError
from .mediainfo import get_media_info_list, MediaInfoList
from .quality import Quality


class Video(ABC):
    @abstractmethod
    def get_path(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def get_qualities(self) -> Sequence[Quality]:
        raise NotImplementedError

    @abstractmethod
    def get_cached_media_info_list(self, connection: Connection) -> MediaInfoList:
        raise NotImplementedError

    @abstractmethod
    def is_flagged(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def analyze(self, attributes: Sequence[Attribute], connection: Connection) -> None:
        raise NotImplementedError


class SingleVideo(Video):
    path: Path
    filename: str
    qualities: List[Quality]

    def __init__(self, path: Path, qualities: Optional[List[Quality]] = None):
        self.path = path
        self.filename = str(path.absolute())
        self.qualities = qualities or []

    def get_path(self) -> Path:
        return self.path

    def get_qualities(self) -> Sequence[Quality]:
        return self.qualities

    def is_flagged(self) -> bool:
        for quality in self.qualities:
            if quality.preference.is_flagged():
                return True

        return False

    def get_media_info_list(self) -> MediaInfoList:
        return get_media_info_list(self.filename)

    def get_cached_media_info_list(self, connection: Connection) -> MediaInfoList:
        size = os.path.getsize(self.filename)
        modified = os.path.getmtime(self.filename)

        return get_tracks(connection, self.filename, size, modified, lambda: self.get_media_info_list())

    def analyze(self, attributes: Sequence[Attribute], connection: Connection) -> None:
        tracks = self.get_cached_media_info_list(connection)

        for attribute in attributes:
            try:
                self.qualities.append(
                    Quality(attribute=attribute, preference=attribute.get_preference(tracks))
                )
            except MissingAttributeError:
                continue
            except Exception as e:
                print(json.dumps(tracks, indent=4))
                raise (e)
