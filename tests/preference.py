from videoprof.level import Level
from videoprof.preference import SinglePreference


def test_preference_title():
    preference = SinglePreference(pattern="test", title="Test")
    assert preference.get_title() == "Test"


def test_preference_string_match():
    preference = SinglePreference(pattern="test", title="Test")
    assert preference.match("test")


def test_preference_substring_start_no_match():
    preference = SinglePreference(pattern="test", title="Test")
    assert not preference.match("test2")


def test_preference_substring_end_no_match():
    preference = SinglePreference(pattern="test", title="Test")
    assert not preference.match("2test")


def test_preference_regex_match():
    preference = SinglePreference(pattern="test[3-8]", title="Test")
    assert preference.match("test3")


def test_preference_regex_no_match():
    preference = SinglePreference(pattern="test[3-8]", title="Test")
    assert not preference.match("test2")


def test_preference_default_level_not_flagged():
    preference = SinglePreference(pattern="test", title="Test")
    assert not preference.is_flagged()


def test_preference_default_level_flagged():
    level = Level(flag=True)
    preference = SinglePreference(pattern="test", title="Test", level=level)
    assert preference.is_flagged()


def test_preference_default_render_identical():
    preference = SinglePreference(pattern="test", title="Test")
    assert preference.render("test-value") == "test-value"


def test_preference_hash():
    preference1 = SinglePreference(pattern="test1", title="Test1")
    preference2 = SinglePreference(pattern="test2", title="Test2")
    preference3 = SinglePreference(pattern="test1", title="Test1")

    assert preference1.__hash__() != preference2.__hash__()
    assert preference1.__hash__() == preference3.__hash__()
