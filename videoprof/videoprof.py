import click
import json
import os

from appdirs import user_config_dir, user_cache_dir
from pathlib import Path
from typing import Dict, List, Sequence

from .attribute import Attribute
from .config import get_attributes
from .db import get_connection
from .preference import Preference
from .progress import show_progress
from .quality import Quality
from .video import SingleVideo, Video

APP_NAME = "videoprof"
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


def show_flags(videos: Sequence[Video]) -> None:
    for video in sorted(videos, key=lambda item: item.get_path()):
        if video.is_flagged():
            print(f"{video.get_path()}:{TAB}{render_cluster(video.get_qualities())}")


def show_directory_summary(directories: Dict[Path, List[Video]], only_flagged: bool) -> None:
    for directory, videos in sorted(directories.items(), key=lambda item: item[0]):
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
            print(f"{directory}:{TAB}{flag_count}/{video_count}{TAB}{render_cluster(qualities)}")


@click.command()
@click.argument("sources", nargs=-1)
@click.option(
    "--config",
    default=os.path.join(user_config_dir(), APP_NAME, "config.json"),
    help="JSON configuration file",
)
@click.option(
    "--cache",
    default=os.path.join(user_cache_dir(), APP_NAME, "cache.db"),
    help="SQLite cache file",
)
@click.option("-s", "--summary", is_flag=True, default=True, help="Turn off attribute summary")
@click.option("-f", "--flags", is_flag=True, default=False, help="Show individual video flags")
@click.option("-d", "--dir-summaries", is_flag=True, default=False, help="Show directory summary")
@click.option(
    "-o",
    "--only-flagged",
    is_flag=True,
    default=False,
    help="Show directory summary for only flagged directories",
)
@click.option(
    "-m",
    "--media-info",
    is_flag=True,
    default=False,
    help="Show media info for the first found video and exit",
)
@click.option("-p", "--dir-depth", default=1, help="Directory depth for summaries")
def main(
    sources: Sequence[str],
    config: str,
    cache: str,
    summary: bool,
    flags: bool,
    dir_summaries: bool,
    only_flagged: bool,
    media_info: bool,
    dir_depth: int,
) -> None:
    attributes = get_attributes(Path(config))
    connection = get_connection(Path(cache))
    videos: List[Video] = []
    directories: Dict[Path, List[Video]] = {}

    for src in sources:
        origin = Path(src)
        dir_paths = origin.glob("/".join(["*" for x in range(dir_depth)]))

        for dir in dir_paths:
            directories[dir] = []
            src_paths = dir.glob("**/*")
            for path in src_paths:
                if path.is_file():
                    video = SingleVideo(path=path)
                    if media_info:
                        print(json.dumps(video.get_cached_media_info_list(connection), indent=4))
                        exit(0)
                    videos.append(video)
                    directories[dir].append(video)

    show_progress(videos, lambda video: video.analyze(attributes, connection))

    if flags:
        show_flags(videos)
        print("")

    if dir_summaries:
        show_directory_summary(directories, only_flagged)
        print("")

    if summary:
        show_summary(attributes, videos)
        print("")
