from videoprof.preference import Preference


def test_preference_string_match():
    preference = Preference(pattern="test", title="Test")
    assert preference.match("test")


def test_preference_substring_start_no_match():
    preference = Preference(pattern="test", title="Test")
    assert not preference.match("test2")


def test_preference_substring_end_no_match():
    preference = Preference(pattern="test", title="Test")
    assert not preference.match("2test")


def test_preference_regex_match():
    preference = Preference(pattern="test[3-8]", title="Test")
    assert preference.match("test3")


def test_preference_regex_no_match():
    preference = Preference(pattern="test[3-8]", title="Test")
    assert not preference.match("test2")
