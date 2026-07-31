# videoprof - A CLI Video Profiler for Python

Profile various attributes of local videos like resolution, codec, container, audio channels, and more!

## Installation

To install, you can add the "videoprof" package from pip:

```bash
pip3 install --user --upgrade videoprof
```

## Requirements

### libmediainfo

`videoprof` depends on [pymediainfo](https://pypi.org/project/pymediainfo/), which ships a bundled copy of libmediainfo in its wheels for Linux (x86-64/ARM64), macOS (x86-64/ARM64), and Windows (x86-64/x86) — so on those platforms nothing extra needs to be installed.

If you're on an unsupported platform, or installed with `--no-binary pymediainfo`, you'll need to install libmediainfo yourself. On Debian or Ubuntu:

```bash
apt-get install libmediainfo0v5
```

If you see a message like the following, it must not be installed (and no bundled copy was available):

```
Could not analyze videos: make sure libmediainfo is installed!
```

### A Compatible Python version:

- 3.9
- 3.10
- 3.11
- 3.12
- 3.13
- 3.14
- 3.15 (pre-release)

## Usage

```
Usage: videoprof [OPTIONS] [SOURCES]...

Options:
  --version                      Show the version and exit.
  -c, --config TEXT              JSON configuration file
  -s, --sqlite-cache TEXT        SQLite cache file
  -f, --files                    Show individual file badges and exit
  -d, --directories              Show directory badges and exit
  -p, --directory-depth INTEGER  Directory depth for summaries
  -o, --only-flagged             Only show individual files or directories on
                                 flagged entries

  -m, --media-info               Show media info for the first found file and
                                 exit

  --help                         Show this message and exit.
```

## Screenshots

Summary view:

![videoprof summary view](images/summary.png)

Directory view:

![videoprof directory view](images/directories.png)

Flaged directory view:

![videoprof flagged directory view](images/flagged.png)

## Configuration

Videoprof is very configurable - any attribute that is returned by mediainfo can be profiled. When videoprof is first run, it will generate a default configuration in `~/.config/videoprof/config.json` (on POSIX/Linux systems).

The [default configuration](videoprof/default_config.json) mostly codifies Blu-Ray specs as "success", DVD specs as "warning", and everything else as an error. While simple, it does contain most features useable within the configuration and can be used as a reference.
