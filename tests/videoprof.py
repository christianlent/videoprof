import re

from pathlib import Path

from click.testing import CliRunner

from videoprof.videoprof import main


# https://stackoverflow.com/questions/14693701/how-can-i-remove-the-ansi-escape-sequences-from-a-string-in-python
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def test_videoprof_directories_empty_directory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("test").mkdir()

        result = runner.invoke(main, ["-d", "test"])

        assert result.exit_code == 0
        assert result.output == ""


def test_videoprof_files_empty_directory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("test").mkdir()

        result = runner.invoke(main, ["-f", "test"])

        assert result.exit_code == 0
        assert result.output == ""


def test_videoprof_summary_empty_directory():
    runner = CliRunner()
    with runner.isolated_filesystem():
        Path("test").mkdir()

        result = runner.invoke(main, ["test"])

        assert result.exit_code == 0
        for count in re.findall(":\t[0-9]+", ansi_escape.sub("", result.output)):
            assert count == ":\t0"
