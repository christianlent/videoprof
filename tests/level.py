from videoprof.level import Level


def test_level_no_color():
    level = Level()
    assert level.render("test") == "test"


def test_level_color():
    level = Level(color="red")
    assert level.render("test") == "\x1b[38;5;1mtest\x1b[0m"
