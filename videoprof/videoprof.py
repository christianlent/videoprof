import click
import json
import os

from appdirs import user_config_dir
from pathlib import Path
from typing import Dict, List

from .attribute import Attribute
from .config import get_attributes
from .db import get_connection
from .preference import Preference
from .progress import show_progress
from .video import Video

APP_NAME = "videoprof"
TAB = "\t"


def show_summary(attributes: List[Attribute], videos: List[Video]) -> None:
    preference_counts: Dict[Preference, int] = {}

    def preference_summary(preference: Preference) -> str:
        count = preference_counts.get(preference, 0)
        return f"{preference.title}:{TAB}{preference.level.render(str(count))}"

    def attribute_summary(attribute: Attribute) -> str:
        counts = "\t".join([preference_summary(preference) for preference in attribute.preferences])
        return f"{attribute.title}{TAB}{counts}"

    for video in videos:
        for quality in video.qualities:
            preference_counts[quality.preference] = preference_counts.get(quality.preference, 0) + 1

    for attribute in attributes:
        print(attribute_summary(attribute))


def show_flags(videos: List[Video]) -> None:
    for video in sorted(videos, key=lambda item: item.path):
        for quality in video.qualities:
            preference = quality.preference
            level = preference.level
            attribute = quality.attribute
            if level.flag:
                print(f"'{str(video.path)}':{TAB}{attribute.title}:{TAB}'{level.render(preference.title)}'")


def show_dir_badges(directories: Dict[Path, List[Video]]) -> None:
    def render(pref: Preference, count: int) -> str:
        prefix = "\u2612 " if pref.level.flag else "\u2713 "
        return pref.level.render(prefix + pref.title)

    badge_counts: Dict[Path, Dict[Preference, int]] = {}
    for directory, videos in directories.items():
        for video in videos:
            badge_counts[directory] = badge_counts.get(directory, {})
            badges = badge_counts[directory]
            for quality in video.qualities:
                badges[quality.preference] = badges.get(quality.preference, 0) + 1

    for directory, badges in sorted(badge_counts.items(), key=lambda item: item[0]):
        badge_text = [render(pref, count) for pref, count in badges.items()]
        print(f"'{directory}':{TAB}{' '.join(badge_text)}")


def show_dir_flags(directories: Dict[Path, List[Video]]) -> None:
    flags: Dict[Path, int] = {}
    for directory, videos in directories.items():
        for video in videos:
            for quality in video.qualities:
                if quality.preference.level.flag:
                    flags[directory] = flags.get(directory, 0) + 1

    for directory, flag_count in sorted(flags.items(), key=lambda item: item[1]):
        print(f"'{directory}':{TAB}{flag_count}")


@click.command()
@click.argument("sources", nargs=-1)
@click.option(
    "--config",
    default=os.path.join(user_config_dir(), APP_NAME, "config.json"),
    help="Show individual flags",
)
@click.option(
    "--db",
    default=os.path.join(user_config_dir(), APP_NAME, "cache.db"),
    help="Show individual flags",
)
@click.option("--flags/--no-flags", default=False, help="Show individual video flags")
@click.option("--summary/--no-summary", default=True, help="Show attribute summary")
@click.option("--dir-badges/--no-dir-badges", default=True, help="Show directory badge summary")
@click.option("--dir-flags/--no-dir-flags", default=True, help="Show directory flag summary")
@click.option("--dir-depth", default=1, help="Directory depth for summaries")
@click.option("--mi/--no-mi", default=False, help="Show media info for the first found video and exit")
def main(
    sources: List[str],
    config: str,
    db: str,
    flags: bool,
    summary: bool,
    dir_badges: bool,
    dir_flags: bool,
    dir_depth: int,
    mi: bool,
) -> None:
    attributes = get_attributes(Path(config))
    connection = get_connection(Path(db))
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
                    video = Video(path=path)
                    if mi:
                        print(json.dumps(video.get_cached_media_info_list(connection), indent=4))
                        exit(0)
                    videos.append(video)
                    directories[dir].append(video)

    show_progress(videos, lambda video: video.analyze(attributes, connection))

    if flags:
        show_flags(videos)
        print("")

    if dir_flags:
        show_dir_flags(directories)
        print("")

    if dir_badges:
        show_dir_badges(directories)
        print("")

    if summary:
        show_summary(attributes, videos)
        print("")
