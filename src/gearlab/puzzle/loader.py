"""
puzzle/loader.py — Save and load .gearlab puzzle files (JSON).
"""
from __future__ import annotations

import json
import os

from gearlab.models import PuzzleFile

# Directory containing built-in puzzles (relative to this file's package root)
_PUZZLES_DIR = os.path.join(
    os.path.dirname(__file__),       # src/gearlab/puzzle/
    "..", "..", "..", "puzzles"      # → project_root/puzzles/
)


def save_puzzle(puzzle: PuzzleFile, path: str) -> None:
    """Serialise *puzzle* to a .gearlab JSON file at *path*."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(puzzle.to_dict(), f, indent=2)


def load_puzzle(path: str) -> PuzzleFile:
    """
    Load a .gearlab JSON file from *path*.
    Raises FileNotFoundError if the file is missing.
    Raises ValueError if the content is not valid JSON.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Puzzle file not found: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid puzzle file '{path}': {exc}") from exc
    return PuzzleFile.from_dict(data)


def builtin_puzzle_path(name: str) -> str:
    """Return the absolute path to a built-in puzzle by base name (no extension)."""
    return os.path.normpath(os.path.join(_PUZZLES_DIR, f"{name}.gearlab"))
