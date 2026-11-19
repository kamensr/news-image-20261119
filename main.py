#!/usr/bin/env python3
"""news-image-20261119: write the poster to /output/entry.png.

The entry is the poster itself (entry.png, drawn with PIL at build time).
This program just copies it to the output directory, deterministically.
Standard library only; no network.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SOURCE):
        print(f"missing image: {SOURCE}", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    # Verify the copy: same size as the source, within the 1 MiB gate.
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        print("copy size mismatch", file=sys.stderr)
        return 1
    if os.path.getsize(target) > 1048576:
        print("image exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
