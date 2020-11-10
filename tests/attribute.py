from typing import cast

from videoprof.attribute import Attribute
from videoprof.mediainfo import MediaInfoList


def test_attribute_basic():
    media_info = cast(
        MediaInfoList,
        [
            {
                "track_type": "test_type",
                "test_attribute": "test_value",
            }
        ],
    )
    attribute = Attribute(
        preferences=[], title="Test Title", track_type="test_type", track_attribute="test_attribute"
    )
    assert attribute.get_value(media_info) == "test_value"
