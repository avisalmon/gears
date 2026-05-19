"""
E05-S1 — Unit tests for the application mode system.
Covers: AppMode enum, ModeController, adaptive UI visibility in GearLabApp.
All tests must FAIL before implementation.
"""
import pytest


# ---------------------------------------------------------------------------
# ModeController — pure Python, no Qt
# ---------------------------------------------------------------------------

def test_mode_default_is_explorer():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    assert mc.current == AppMode.EXPLORER


def test_set_mode_updates_current():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    result = mc.set_mode(AppMode.ENGINEER)
    assert result == AppMode.ENGINEER
    assert mc.current == AppMode.ENGINEER


def test_all_five_modes_defined():
    from gearlab.ui.mode import AppMode
    expected = {"explorer", "student", "engineer", "puzzle", "presentation"}
    assert {m.value for m in AppMode} == expected


def test_engineer_shows_edit_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.ENGINEER)
    assert mc.shows_edit_controls()


def test_explorer_hides_edit_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.EXPLORER)
    assert not mc.shows_edit_controls()


def test_student_hides_edit_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.STUDENT)
    assert not mc.shows_edit_controls()


def test_engineer_shows_defect_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.ENGINEER)
    assert mc.shows_defect_controls()


def test_explorer_hides_defect_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.EXPLORER)
    assert not mc.shows_defect_controls()


def test_student_hides_defect_controls():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.STUDENT)
    assert not mc.shows_defect_controls()


def test_ratio_badge_style_per_mode():
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.ENGINEER)
    assert mc.ratio_badge_style() == "full"
    mc.set_mode(AppMode.STUDENT)
    assert mc.ratio_badge_style() == "full"
    mc.set_mode(AppMode.EXPLORER)
    assert mc.ratio_badge_style() == "minimal"
    mc.set_mode(AppMode.PRESENTATION)
    assert mc.ratio_badge_style() == "presentation"


# ---------------------------------------------------------------------------
# GearLabApp — mode integration (requires Qt)
# ---------------------------------------------------------------------------

def test_app_has_mode_controller(qtbot):
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert hasattr(win, "_mode_ctrl")
    assert win._mode_ctrl is not None


def test_set_mode_changes_app_mode(qtbot):
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    assert win._mode_ctrl.current == AppMode.ENGINEER


def test_engineer_mode_shows_add_button(qtbot):
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    # isVisibleTo checks visibility relative to the ancestor window
    # without requiring the window to be physically shown
    assert win._btn_add_gear.isVisibleTo(win)


def test_explorer_mode_hides_add_button(qtbot):
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.EXPLORER)
    assert not win._btn_add_gear.isVisibleTo(win)
