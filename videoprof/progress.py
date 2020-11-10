import math
import sys
from typing import Callable, Sequence, TypeVar

T = TypeVar("T")


def show_progress(items: Sequence[T], process: Callable[[T], None]) -> None:
    for x in range(0, len(items)):
        progress = math.trunc(10000 * (x + 1) / len(items)) / 100
        print(f"> {progress}%  ", end="\r", flush=True, file=sys.stderr)
        process(items[x])
