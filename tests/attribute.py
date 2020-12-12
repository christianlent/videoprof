import pytest

from typing import cast

from videoprof.attribute import SingleAttribute, CompositeAttribute
from videoprof.exceptions import MissingAttributeError
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


def test_composite_attribute_get_title():
    attribute = CompositeAttribute(
        attributes=[],
        preferences=[],
        title="Test Title",
    )
    assert attribute.get_title() == "Test Title"


def test_composite_attribute_get_preferences():
    attribute = CompositeAttribute(
        attributes=[],
        preferences=[],
        title="Test Title",
    )
    assert attribute.get_preferences() == []


def test_composite_attribute_concat_no_existing_preference():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute1": "good",
                "test_attribute2": "test",
            }
        ],
    )

    attribute1 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute1",
    )

    attribute2 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute2",
    )

    composite = CompositeAttribute(
        attributes=[attribute1, attribute2], preferences=[], title="Composite Test"
    )

    preference = composite.get_preference(media_info)
    assert preference.title == "goodtest"


def test_composite_attribute_concat_existing_preference():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute1": "good",
                "test_attribute2": "test",
            }
        ],
    )

    attribute1 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute1",
    )

    attribute2 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute2",
    )

    existing_preference = SinglePreference(pattern="goodtest", title="GoodTest")

    composite = CompositeAttribute(
        attributes=[attribute1, attribute2], preferences=[existing_preference], title="Composite Test"
    )

    preference = composite.get_preference(media_info)
    assert preference == existing_preference


def test_composite_attribute_one_missing():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute2": "test",
            }
        ],
    )

    attribute1 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute1",
    )

    attribute2 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute2",
    )

    composite = CompositeAttribute(
        attributes=[attribute1, attribute2], preferences=[], title="Composite Test"
    )

    preference = composite.get_preference(media_info)
    assert preference.title == "test"


def test_composite_attribute_all_missing():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
            }
        ],
    )

    attribute1 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute1",
    )

    attribute2 = SingleAttribute(
        preferences=[],
        title="Test Title",
        track_type="test_type",
        track_attribute="test_attribute2",
    )

    composite = CompositeAttribute(
        attributes=[attribute1, attribute2], preferences=[], title="Composite Test"
    )

    with pytest.raises(MissingAttributeError):
        composite.get_preference(media_info)
