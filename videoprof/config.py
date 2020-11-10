import json
import os

from pathlib import Path
from typing import cast, Any, Dict, List

from .attribute import Attribute
from .preference import Preference
from .level import Level

Config = Dict[str, Any]


def get_default_config() -> Config:
    path = Path(__file__)
    config = path.parent.joinpath("default_config.json")
    return cast(Config, json.loads(config.read_text()))


def save_config(config: Config, path: Path) -> None:
    dir = path.parent
    if not dir.is_dir():
        os.makedirs(str(dir))
    config = get_default_config()
    path.write_text(json.dumps(config, indent=4))


def load_config(path: Path) -> Config:
    return cast(Config, json.loads(path.read_text()))


def make_attributes(config: Config = get_default_config()) -> List[Attribute]:
    levels = {}
    for name, options in config["levels"].items():
        levels[name] = Level(color=options["color"], flag=options["flag"])

    attributes = []

    for options in config["attributes"]:
        attribute = Attribute(
            title=options["title"],
            preferences=[],
            default_level=levels[options["default_level"]],
            track_type=options["track_type"],
            track_attribute=options["track_attribute"],
        )
        attribute.preferences = [
            Preference(
                title=x["title"],
                pattern=x.get("pattern", x["title"]),
                level=levels[x["level"]],
            )
            for x in options["preferences"]
        ]
        attributes.append(attribute)

    return attributes


def get_attributes(path: Path) -> List[Attribute]:
    if path.exists():
        config = load_config(path)
    else:
        config = get_default_config()
        save_config(config, path)

    return make_attributes(config)
