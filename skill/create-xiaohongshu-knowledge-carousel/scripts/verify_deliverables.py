#!/usr/bin/env python3
"""Verify that a carousel deliverable directory contains final PNG pages only."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required to verify image dimensions.") from exc


FINAL_PATTERN = re.compile(r"^\d{2}-.+-final\.png$")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1440)
    args = parser.parse_args()

    directory = args.directory.resolve()
    if not directory.is_dir():
        raise SystemExit(f"Not a directory: {directory}")
    entries = sorted(directory.iterdir())
    directories = [path.name for path in entries if path.is_dir()]
    if directories:
        raise SystemExit(f"Subdirectories found in final-only delivery: {directories}")
    files = [path for path in entries if path.is_file()]
    if not files:
        raise SystemExit("No final PNG pages found")
    extras = [path.name for path in files if not FINAL_PATTERN.match(path.name)]
    if extras:
        raise SystemExit(f"Non-final files found: {extras}")
    if args.expected_count is not None and len(files) != args.expected_count:
        raise SystemExit(f"Expected {args.expected_count} final pages, found {len(files)}")
    for path in files:
        with Image.open(path) as image:
            if image.format != "PNG":
                raise SystemExit(f"Not a PNG: {path.name}")
            if image.size != (args.width, args.height):
                raise SystemExit(f"Wrong size for {path.name}: {image.size}")
    print(f"Deliverables OK: {len(files)} final PNG page(s), {args.width}x{args.height}")
    for path in files:
        print(path.name)


if __name__ == "__main__":
    main()
