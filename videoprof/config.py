import json
import os

from pathlib import Path
from typing import cast, Any, Dict, Sequence

from .attribute import Attribute, SingleAttribute, CompositeAttribute
from .preference import Preference, SinglePreference
from .level import Level, DEFAULT_LEVEL

Config = Dict[str, Any]
ConfigAttribute = Dict[str, Any]
ConfigPreference = Dict[str, Any]
LevelMap = Dict[str, Level]


def get_preference(config_preference: ConfigPreference, level_map: LevelMap, render: str) -> Preference:
    return SinglePreference(
        title=render % (config_preference["title"]),
        pattern=config_preference.get("pattern", config_preference["title"]),
        level=level_map[config_preference["level"]],
    )


def get_single_attribute(config_attribute: ConfigAttribute, level_map: LevelMap) -> Attribute:
    default_level = (
        level_map[config_attribute["default_level"]] if "default_level" in config_attribute else DEFAULT_LEVEL
    )
    attribute = SingleAttribute(
        title=config_attribute["title"],
        render=config_attribute.get("render", "%s"),
        preferences=[],
        default_level=default_level,
        track_type=config_attribute["track_type"],
        track_attribute=config_attribute["track_attribute"],
    )
    attribute.preferences = [
        get_preference(x, level_map, attribute.render) for x in config_attribute.get("preferences", [])
    ]
    return attribute


def get_composite_attribute(config_attribute: ConfigAttribute, level_map: LevelMap) -> Attribute:
    default_level = (
        level_map[config_attribute["default_level"]] if "default_level" in config_attribute else DEFAULT_LEVEL
    )
    attribute = CompositeAttribute(
        title=config_attribute["title"],
        render=config_attribute.get("render", "%s"),
        attributes=[],
        preferences=[],
        default_level=default_level,
    )
    attribute.attributes = [get_attribute(x, level_map) for x in config_attribute.get("attributes", [])]
    attribute.preferences = [
        get_preference(x, level_map, attribute.render) for x in config_attribute.get("preferences", [])
    ]
    return attribute


def get_attribute(config_attribute: ConfigAttribute, level_map: LevelMap) -> Attribute:
    return (
        get_composite_attribute(config_attribute, level_map)
        if "attributes" in config_attribute
        else get_single_attribute(config_attribute, level_map)
    )


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


def make_attributes(config: Config = get_default_config()) -> Sequence[Attribute]:
    level_map = {}
    for name, options in config["levels"].items():
        level_map[name] = Level(color=options["color"], flag=options["flag"])

    attributes = []

    for config_attribute in config["attributes"]:
        attribute = get_attribute(config_attribute, level_map)
        attributes.append(attribute)

    return attributes


def get_attributes(path: Path) -> Sequence[Attribute]:
    if path.exists():
        config = load_config(path)
    else:
        config = get_default_config()
        save_config(config, path)

    return make_attributes(config)
