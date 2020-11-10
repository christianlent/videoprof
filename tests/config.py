from videoprof.config import make_attributes


def test_config_make_attributes_empty():
    attributes = make_attributes({"levels": {}, "attributes": []})

    assert len(attributes) == 0


def test_config_make_attributes_one():
    attributes = make_attributes(
        {
            "levels": {},
            "attributes": [
                {"title": "Test Attribute", "track_type": "test_type", "track_attribute": "test_attribute"},
            ],
        }
    )

    assert len(attributes) == 1
