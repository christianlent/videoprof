from videoprof.level import Level


def test_level_no_color():
    level = Level()
    assert level.render("test") == "test"


def test_level_color(monkeypatch):
    # `colored` only emits ANSI codes when it thinks it's writing to a TTY;
    # force it on so this test is deterministic under pytest's captured output.
    monkeypatch.setenv("FORCE_COLOR", "1")
    level = Level(color="red")
    assert level.render("test") == "\x1b[38;5;1mtest\x1b[0m"
