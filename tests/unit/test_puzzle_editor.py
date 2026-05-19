"""
E07-S2 — Puzzle Editor tests (TDD).

Tests are written before implementation and must fail until the feature is built.
"""
from __future__ import annotations

import json
import os
import tempfile

import pytest
from pytestqt.qt_compat import qt_api  # noqa: F401 — fixture dep

from gearlab.models import Direction, GearSystem, GearType, Gear


# ---------------------------------------------------------------------------
# Helper — import editor (will fail until implemented)
# ---------------------------------------------------------------------------

def _import_editor():
    from gearlab.ui.puzzle_editor import PuzzleEditorDialog
    return PuzzleEditorDialog


# ===========================================================================
# E07-S2-01  PuzzleEditorDialog — basic construction
# ===========================================================================

def test_editor_dialog_constructs(qtbot):
    """PuzzleEditorDialog can be instantiated without errors."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg is not None


def test_editor_has_title_field(qtbot):
    """Dialog exposes a title line-edit."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_title() == ""


def test_editor_has_description_field(qtbot):
    """Dialog exposes a description field."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_description() == ""


def test_editor_has_difficulty_selector(qtbot):
    """Dialog exposes difficulty ('easy'/'medium'/'hard')."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_difficulty() in ("easy", "medium", "hard")


# ===========================================================================
# E07-S2-02  Guided template — pre-filled starter layout
# ===========================================================================

def test_editor_new_puzzle_loads_template(qtbot):
    """new_puzzle() pre-fills two gears in the editor canvas."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    assert len(dlg.get_gear_list()) == 2


def test_editor_template_has_one_driver(qtbot):
    """Template has exactly one driver gear."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    drivers = [g for g in dlg.get_gear_list() if g.is_driver]
    assert len(drivers) == 1


def test_editor_template_title_empty(qtbot):
    """Template does not pre-fill the title — teacher must fill it in."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    assert dlg.get_title() == ""


# ===========================================================================
# E07-S2-03  Goal definition UI
# ===========================================================================

def test_editor_default_target_ratio_none(qtbot):
    """Target ratio is None by default (unchecked)."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_target_ratio() is None


def test_editor_set_target_ratio(qtbot):
    """Setting target ratio to 3.0 is reflected by getter."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.set_target_ratio(3.0)
    assert dlg.get_target_ratio() == pytest.approx(3.0)


def test_editor_default_target_direction_none(qtbot):
    """Target direction is None by default."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_target_direction() is None


def test_editor_set_target_direction_ccw(qtbot):
    """Setting direction to CCW is reflected by getter."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.set_target_direction(Direction.CCW)
    assert dlg.get_target_direction() == Direction.CCW


def test_editor_default_max_gears_none(qtbot):
    """Max gears is None by default."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_max_gears() is None


def test_editor_set_max_gears(qtbot):
    """Setting max gears to 4 is reflected by getter."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.set_max_gears(4)
    assert dlg.get_max_gears() == 4


# ===========================================================================
# E07-S2-04  Per-element lock / unlock
# ===========================================================================

def test_editor_gear_unlocked_by_default(qtbot):
    """All gears are unlocked when editor opens."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    locked = dlg.get_locked_ids()
    assert locked == []


def test_editor_lock_gear(qtbot):
    """Locking a gear by id appears in get_locked_ids()."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    gears = dlg.get_gear_list()
    driver_id = next(g.id for g in gears if g.is_driver)
    dlg.set_gear_locked(driver_id, True)
    assert driver_id in dlg.get_locked_ids()


def test_editor_unlock_gear(qtbot):
    """Unlocking a previously locked gear removes it from locked list."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    gears = dlg.get_gear_list()
    driver_id = next(g.id for g in gears if g.is_driver)
    dlg.set_gear_locked(driver_id, True)
    dlg.set_gear_locked(driver_id, False)
    assert driver_id not in dlg.get_locked_ids()


# ===========================================================================
# E07-S2-05  Hint authoring
# ===========================================================================

def test_editor_hints_empty_by_default(qtbot):
    """All three hint fields start empty."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    assert dlg.get_hints() == ["", "", ""]


def test_editor_set_hints(qtbot):
    """Setting hints is reflected by get_hints()."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.set_hints(["Count teeth", "Try 40T", "Driver is locked"])
    assert dlg.get_hints() == ["Count teeth", "Try 40T", "Driver is locked"]


def test_editor_hints_stripped_of_empties_in_puzzle(qtbot, tmp_path):
    """Empty hint strings are excluded when building the PuzzleFile."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    dlg.set_title("T1")
    dlg.set_hints(["First hint", "", ""])
    pf = dlg.build_puzzle_file()
    assert pf.hints == ["First hint"]


# ===========================================================================
# E07-S2-07  Duplicate existing puzzle
# ===========================================================================

def test_editor_load_existing_fills_fields(qtbot, tmp_path):
    """load_puzzle_file() pre-fills all fields from a PuzzleFile."""
    from gearlab.puzzle.loader import builtin_puzzle_path, load_puzzle
    PuzzleEditorDialog = _import_editor()
    pf = load_puzzle(builtin_puzzle_path("easy_01"))
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.load_puzzle_file(pf)
    assert dlg.get_title() == pf.title
    assert dlg.get_description() == pf.description


def test_editor_load_existing_fills_goal(qtbot):
    """load_puzzle_file() fills goal ratio."""
    from gearlab.puzzle.loader import builtin_puzzle_path, load_puzzle
    PuzzleEditorDialog = _import_editor()
    pf = load_puzzle(builtin_puzzle_path("easy_01"))
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.load_puzzle_file(pf)
    assert dlg.get_target_ratio() == pytest.approx(pf.goal.target_ratio)


def test_editor_load_existing_fills_hints(qtbot):
    """load_puzzle_file() fills hints (padded to 3 with empty strings)."""
    from gearlab.puzzle.loader import builtin_puzzle_path, load_puzzle
    PuzzleEditorDialog = _import_editor()
    pf = load_puzzle(builtin_puzzle_path("easy_01"))
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.load_puzzle_file(pf)
    hints = dlg.get_hints()
    assert len(hints) == 3


# ===========================================================================
# E07-S2-08  build_puzzle_file() → PuzzleFile
# ===========================================================================

def test_editor_build_puzzle_file(qtbot):
    """build_puzzle_file() returns a valid PuzzleFile with all fields set."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    dlg.set_title("My Puzzle")
    dlg.set_target_ratio(2.0)
    dlg.set_hints(["Hint A", "Hint B", ""])
    pf = dlg.build_puzzle_file()
    assert pf.title == "My Puzzle"
    assert pf.goal.target_ratio == pytest.approx(2.0)
    assert "Hint A" in pf.hints
    assert len(pf.initial_state.elements) == 2


def test_editor_build_requires_title(qtbot):
    """build_puzzle_file() raises ValueError if title is empty."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    with pytest.raises(ValueError, match="title"):
        dlg.build_puzzle_file()


# ===========================================================================
# E07-S2-09  Save to .gearlab file
# ===========================================================================

def test_editor_save_writes_file(qtbot, tmp_path):
    """save_to_path() serialises the puzzle to a .gearlab JSON file."""
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    dlg.set_title("Save Test")
    out = str(tmp_path / "test.gearlab")
    dlg.save_to_path(out)
    assert os.path.exists(out)
    with open(out) as f:
        data = json.load(f)
    assert data["title"] == "Save Test"


def test_editor_save_then_load_round_trip(qtbot, tmp_path):
    """Saved file can be loaded back into a PuzzleFile unchanged."""
    from gearlab.puzzle.loader import load_puzzle
    PuzzleEditorDialog = _import_editor()
    dlg = PuzzleEditorDialog()
    qtbot.addWidget(dlg)
    dlg.new_puzzle()
    dlg.set_title("Round Trip")
    dlg.set_target_ratio(3.0)
    out = str(tmp_path / "rt.gearlab")
    dlg.save_to_path(out)
    pf = load_puzzle(out)
    assert pf.title == "Round Trip"
    assert pf.goal.target_ratio == pytest.approx(3.0)
