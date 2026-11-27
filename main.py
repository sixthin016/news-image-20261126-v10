#!/usr/bin/env python3
"""Entry point for the news-image-20261126 v10 entry.

The page is pre-rendered by tools/generate.py (stdlib + Pillow only,
deterministic, no network, no clock). This script just places the
finished 1024x1024 PNG where the grader expects it. Run
`python3 tools/generate.py` first to rebuild assets/entry.png.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "assets", "entry.png")
TARGET_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(TARGET_DIR, exist_ok=True)
shutil.copyfile(SOURCE, os.path.join(TARGET_DIR, "entry.png"))
print("copied entry.png to", TARGET_DIR)
