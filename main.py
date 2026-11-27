#!/usr/bin/env python3
"""Deliver the finished broadsheet PNG to the grader output folder.

The picture is baked ahead of time by tools/generate.py; this module
only carries the baked file across. Nothing here reaches the network,
reads the clock, or depends on the machine it runs on.
"""
from os import environ as _env, makedirs as _makedirs
from os import path as _path
from shutil import copyfile as _copyfile


def _baked_png():
    folder = _path.dirname(_path.abspath(__file__))
    return _path.join(folder, "assets", "entry.png")


def _out_folder():
    return _env.get("MAKEFUN_OUTPUT_DIR", "/output")


def ship():
    """Copy the baked PNG into the output folder and say where it went."""
    dest = _out_folder()
    _makedirs(dest, exist_ok=True)
    _copyfile(_baked_png(), _path.join(dest, "entry.png"))
    print("entry.png delivered to", dest)


ship()
