from typing import cast

from videoprof.attribute import SingleAttribute
from videoprof.mediainfo import MediaInfoList
from videoprof.preference import SinglePreference


def test_attribute_get_title():
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )
    assert attribute.get_title() == "Test Title"


def test_attribute_get_preferences():
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )
    assert attribute.get_preferences() == []


def test_attribute_get_value():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test_value",
            }
        ],
    )
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )
    assert attribute.get_value(media_info) == "test_value"


def test_attribute_get_missing_value():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test_value",
            }
        ],
    )
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="missing_attribute",
    )
    assert attribute.get_value(media_info) is None


def test_attribute_get_missing_type():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test_value",
            }
        ],
    )
    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="missing_type",
        track_attribute="test_attribute",
    )
    assert attribute.get_value(media_info) is None


def test_attribute_get_preference_create_default():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test",
            }
        ],
    )

    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )

    preference = attribute.get_preference(media_info)
    assert preference.get_title() == "test"


def test_attribute_get_preference_create_added():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test",
            }
        ],
    )

    attribute = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )

    preference = attribute.get_preference(media_info)
    assert preference == attribute.get_preferences()[0]


def test_attribute_get_preference_find_existing():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test",
            }
        ],
    )

    existing_preference = SinglePreference(pattern="test", title="Test")

    attribute = SingleAttribute(
        preferences=[existing_preference],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute",
    )

    preference = attribute.get_preference(media_info)
    assert preference == existing_preference
