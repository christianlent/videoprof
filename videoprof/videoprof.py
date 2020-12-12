import click
import json
import os

from appdirs import user_config_dir, user_cache_dir
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from .attribute import Attribute
from .config import get_attributes
from .db import get_connection
from .preference import Preference
from .progress import show_progress
from .quality import Quality
from .video import SingleVideo, Video

APP_NAME = "videoprof"
DEFAULT_CONFIG = os.path.join(user_config_dir(), APP_NAME, "config.json")
DEFAULT_CACHE = os.path.join(user_cache_dir(), APP_NAME, "cache.db")
TAB = "\t"


def render_badge(preference: Preference) -> str:
    prefix = "\u2612 " if preference.is_flagged() else "\u2713 "
    return preference.render(prefix + preference.get_title())


def render_cluster(qualities: Sequence[Quality]) -> str:
    cluster = [
        render_badge(quality.preference)
        for quality in sorted(qualities, key=lambda x: x.attribute.get_title())
    ]
    return f"{' '.join(cluster)}"


def show_summary(attributes: Sequence[Attribute], videos: Sequence[Video]) -> None:
    preference_counts: Dict[Preference, int] = {}

    def preference_summary(preference: Preference) -> str:
        count = preference_counts.get(preference, 0)
        return f"{preference.get_title()}:{TAB}{preference.render(str(count))}"

    def attribute_summary(attribute: Attribute) -> str:
        counts = "\t".join([preference_summary(preference) for preference in attribute.get_preferences()])
        return f"{attribute.get_title()}{TAB}{counts}"

    for video in videos:
        for quality in video.get_qualities():
            preference_counts[quality.preference] = preference_counts.get(quality.preference, 0) + 1

    for attribute in attributes:
        print(attribute_summary(attribute))


def show_files(videos: Sequence[Video], only_flagged: bool) -> None:
    for video in sorted(videos, key=lambda item: item.get_path()):
        if not only_flagged or video.is_flagged():
            print(f"{video.get_path()}:{TAB}{render_cluster(video.get_qualities())}")


def show_directories(dir_videos: Dict[Path, List[Video]], only_flagged: bool) -> None:
    for directory, videos in sorted(dir_videos.items(), key=lambda item: item[0]):
        flag_count = 0
        video_count = 0
        qualities: List[Quality] = []

        for video in videos:
            video_count += 1
            if video.is_flagged():
                flag_count += 1

            for quality in video.get_qualities():
                if quality not in qualities:
                    qualities.append(quality)

        if not only_flagged or flag_count:
            print(f"{directory}:{TAB}\u2690 {flag_count}/{video_count}{TAB}{render_cluster(qualities)}")


@click.command()
@click.argument("sources", nargs=-1)
@click.option("-c", "--config", default=DEFAULT_CONFIG, help="JSON configuration file")
@click.option("-s", "--sqlite-cache", default=DEFAULT_CACHE, help="SQLite cache file")
@click.option("-f", "--files", is_flag=True, default=False, help="Show individual file badges and exit")
@click.option("-d", "--directories", is_flag=True, default=False, help="Show directory badges and exit")
@click.option("-p", "--directory-depth", default=1, help="Directory depth for summaries")
@click.option(
    "-o",
    "--only-flagged",
    is_flag=True,
    default=False,
    help="Only show individual files or directories on flagged entries",
)
@click.option(
    "-m",
    "--media-info",
    is_flag=True,
    default=False,
    help="Show media info for the first found file and exit",
)
def main(
    sources: Sequence[str],
    config: str,
    sqlite_cache: str,
    files: bool,
    directories: bool,
    only_flagged: bool,
    media_info: bool,
    directory_depth: int,
) -> None:
    attributes = get_attributes(Path(config))
    connection = get_connection(Path(sqlite_cache))
    videos: List[Video] = []
    dir_videos: Dict[Path, List[Video]] = {}

    def add_video(path: Path) -> Optional[Video]:
        if not path.is_file():
            return None

        video = SingleVideo(path=path)
        if media_info:
            print(json.dumps(video.get_cached_media_info_list(connection), indent=4))
            exit(0)
        videos.append(video)
        return video

    for src in sources:
        origin = Path(src)
        add_video(origin)

        file_paths = origin.glob("*")
        for file in file_paths:
            add_video(file)

        dir_paths = origin.glob("/".join(["*" for x in range(directory_depth)]))
        for dir in dir_paths:
            dir_videos[dir] = []
            src_paths = dir.glob("**/*")
            for path in src_paths:
                video = add_video(path)
                if video:
                    dir_videos[dir].append(video)

    try:
        show_progress(videos, lambda video: video.analyze(attributes, connection))
    except OSError:
        print("Could not analyze videos: make sure libmediainfo is installed!")
        exit(1)

    if files:
        show_files(videos, only_flagged)
        exit(0)

    if directories:
        show_directories(dir_videos, only_flagged)
        exit(0)

    show_summary(attributes, videos)
