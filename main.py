#!/usr/bin/env python3
"""Hand the finished poster over to the grader.

The poster itself is drawn elsewhere and already sits in this repo as
entry.png. All this script does is place an exact copy of it where the
grading harness expects to find it. Nothing is drawn, decoded or
re-encoded here, so the output bytes are always identical to the input.
"""

import os
import shutil
from pathlib import Path

POSTER_NAME = "entry.png"
FALLBACK_DIR = "/output"


def poster_path():
    """Locate entry.png next to this script, whatever the cwd is."""
    return Path(__file__).resolve().parent / POSTER_NAME


def output_dir():
    """Pick the destination folder from the environment, with fallback."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(chosen) if chosen else Path(FALLBACK_DIR)


def main():
    source = poster_path()
    target_folder = output_dir()
    target_folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target_folder / POSTER_NAME)


if __name__ == "__main__":
    main()
