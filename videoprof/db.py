import json
import os
import sqlite3

from pathlib import Path
from typing import Callable

from .mediainfo import MediaInfoList


def get_connection(path: Path) -> sqlite3.Connection:
    dir = path.parent
    if not dir.is_dir():
        os.makedirs(str(dir))

    connection = sqlite3.connect(str(path))
    cursor = connection.cursor()
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='videos'")

    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "CREATE TABLE videos (filename varchar primary key, size integer, modified real, tracks text)"
        )

    cursor.close()
    return connection


def get_tracks(
    connection: sqlite3.Connection,
    filename: str,
    size: int,
    modified: float,
    tracks_generator: Callable[[], MediaInfoList],
) -> MediaInfoList:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM videos WHERE filename=?", [filename])
    record = cursor.fetchone()

    if not record:
        tracks = tracks_generator()
        with connection:
            cursor.execute(
                "INSERT INTO videos VALUES (?,?,?,?)",
                [filename, size, modified, json.dumps(tracks)],
            )
    elif record[1] != size or record[2] != modified:
        tracks = tracks_generator()
        with connection:
            cursor.execute(
                "UPDATE videos SET size = ?, modified = ?, tracks = ? WHERE filename = ?",
                [size, modified, json.dumps(tracks), filename],
            )
    else:
        tracks = json.loads(record[3])

    cursor.close()

    return tracks
