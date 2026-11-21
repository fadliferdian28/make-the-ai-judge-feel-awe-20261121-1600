#!/usr/bin/env python3
"""Copy the entry text to the make.fun output directory.

Stdlib only, no network, no randomness, no clock. The written file is
verified byte-for-byte against the source before exiting.
"""

import hashlib
import os
import shutil
import sys

ENTRY_NAME = "entry.txt"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_entry(path):
    """The judged file must be 1-280 Unicode code points, not only whitespace."""
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    if not text.strip():
        return "entry is empty or only whitespace"
    if len(text) > 280:
        return "entry is %d characters, over the 280 limit" % len(text)
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, ENTRY_NAME)
    problem = check_entry(source)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, ENTRY_NAME)

    if os.path.abspath(source) == os.path.abspath(dest):
        print("source and destination are the same file", file=sys.stderr)
        return 1

    shutil.copyfile(source, dest)

    if sha256_of(source) != sha256_of(dest):
        print("checksum mismatch after copy", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
