from pathlib import Path

from videoprof.attribute import SingleAttribute
from videoprof.level import Level
from videoprof.preference import SinglePreference
from videoprof.quality import Quality
from videoprof.video import SingleVideo


def test_video_path():
    path = Path("./testpath.mkv")
    video = SingleVideo(path=path)
    assert video.get_path() == path


def test_video_default_not_flagged():
    video = SingleVideo(path=Path("./testpath.mkv"))
    assert not video.is_flagged()


def test_video_initial_get_qualities():
    video = SingleVideo(path=Path("./testpath.mkv"))
    assert len(video.get_qualities()) == 0


def test_video_get_qualities():
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )
    level = Level(flag=True)
    preference = SinglePreference(pattern="test", title="Test", level=level)
    quality = Quality(attribute=attribute, preference=preference)

    video = SingleVideo(path=Path("./testpath.mkv"), qualities=[quality])
    assert video.get_qualities()[0] == quality


def test_video_flagged_quality():
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )
    level = Level(flag=True)
    preference = SinglePreference(pattern="test", title="Test", level=level)
    quality = Quality(attribute=attribute, preference=preference)

    video = SingleVideo(path=Path("./testpath.mkv"), qualities=[quality])
    assert video.is_flagged()
