#!/usr/bin/env python3
"""news-image-20261121 entry (Python 3.13, standard library only).

Copies the entry image beside this file to /output/entry.png (or
$MAKEFUN_OUTPUT_DIR/entry.png outside the grader's container).
The image itself is drawn by draw.py (Pillow) and stored in the repo.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
shutil.copyfile(
    os.path.join(HERE, "entry.png"),
    os.path.join(OUT_DIR, "entry.png"),
)
print("wrote entry.png", file=sys.stderr)
