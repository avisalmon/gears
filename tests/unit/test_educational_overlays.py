"""
E06-S1 — Unit tests for educational overlays.
Covers: ratio badges, formula panel, direction explainer, expert data table.
All tests must FAIL before implementation (TDD RED phase).
"""
import pytest

from gearlab.models import Direction, Gear, GearSystem, GearType, Connection, ConnectionType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _spur(tooth_count=20, module=8.0, rpm=100.0, is_driver=False,
          pos=(0.0, 0.0), direction=Direction.CW) -> Gear:
    g = Gear(gear_type=GearType.SPUR, tooth_count=tooth_count, module=module,
             position=pos, is_driver=is_driver, rpm=rpm)
    g._direction = direction
    return g


# ---------------------------------------------------------------------------
# E06-S1-01 — Dynamic ratio badges
# ---------------------------------------------------------------------------

def test_badge_overlays_list_exists(qtbot):
    """App exposes _badge_overlays tracking ratio badges."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert hasattr(win, "_badge_overlays")


def test_ratio_badges_created_for_demo_connections(qtbot):
    """Demo has 2 connections → at least 2 ratio badges on canvas."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert len(win._badge_overlays) >= 2


def test_ratio_badges_hidden_in_presentation_mode(qtbot):
    """Ratio badges are hidden in Presentation mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.PRESENTATION)
    for badge in win._badge_overlays:
        assert not badge.isVisible()


def test_ratio_badges_visible_in_student_mode(qtbot):
    """Ratio badges are visible in Student mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    assert any(badge.isVisible() for badge in win._badge_overlays)


def test_ratio_badge_text_shows_ratio(qtbot):
    """Each badge label contains a colon (ratio notation like '2:1')."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    for badge in win._badge_overlays:
        assert ":" in badge.toPlainText() or ":" in badge.document().toPlainText()


# ---------------------------------------------------------------------------
# E06-S1-02 / E06-S1-03 — Formula panel
# ---------------------------------------------------------------------------

def test_formula_panel_exists(qtbot):
    """App has a _formula_panel attribute."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert hasattr(win, "_formula_panel")


def test_formula_panel_hidden_in_explorer_mode(qtbot):
    """Formula panel is hidden in Explorer mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.EXPLORER)
    assert not win._formula_panel.isVisibleTo(win)


def test_formula_panel_visible_in_student_mode(qtbot):
    """Formula panel is visible in Student mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    assert win._formula_panel.isVisibleTo(win)


def test_formula_panel_visible_in_engineer_mode(qtbot):
    """Formula panel is visible in Engineer mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    assert win._formula_panel.isVisibleTo(win)


def test_formula_panel_hidden_in_presentation_mode(qtbot):
    """Formula panel is hidden in Presentation mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.PRESENTATION)
    assert not win._formula_panel.isVisibleTo(win)


def test_formula_panel_shows_ratio_value(qtbot):
    """Formula panel content includes the numeric ratio for connected demo gears."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    text = win._formula_panel.get_text()
    # Demo has a 20T:40T pair → ratio 2.0
    assert "2" in text


def test_formula_panel_shows_tooth_counts(qtbot):
    """Formula panel mentions tooth counts of connected gears."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    text = win._formula_panel.get_text()
    assert "20" in text or "40" in text


# ---------------------------------------------------------------------------
# E06-S1-04 — Direction rule explainer
# ---------------------------------------------------------------------------

def test_formula_panel_mentions_direction_reversal(qtbot):
    """Formula panel text explains that direction reverses on meshing."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    text = win._formula_panel.get_text().lower()
    assert "revers" in text or "opposite" in text or "↺" in text or "↻" in text


# ---------------------------------------------------------------------------
# E06-S1-06 — Expert data table (Engineer mode only)
# ---------------------------------------------------------------------------

def test_formula_panel_has_expert_table(qtbot):
    """Formula panel exposes an expert data table widget."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert hasattr(win._formula_panel, "_expert_table")


def test_expert_table_hidden_in_student_mode(qtbot):
    """Expert table is explicitly hidden in Student mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.STUDENT)
    assert win._formula_panel._expert_table.isHidden()


def test_expert_table_visible_in_engineer_mode(qtbot):
    """Expert table is not hidden in Engineer mode."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    assert not win._formula_panel._expert_table.isHidden()


def test_expert_table_has_gear_rows(qtbot):
    """Expert table has one row per gear in the demo (3 demo gears)."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    assert win._formula_panel._expert_table.rowCount() >= 3


def test_expert_table_column_count(qtbot):
    """Expert table has at least 5 columns (name, teeth, ratio, RPM, velocity)."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert win._formula_panel._expert_table.columnCount() >= 5


# ---------------------------------------------------------------------------
# FormulaPanel unit tests (isolated)
# ---------------------------------------------------------------------------

def test_formula_panel_update_student(qtbot):
    """update() in student mode sets text with formula."""
    from gearlab.ui.formula_panel import FormulaPanel
    from gearlab.ui.mode import AppMode
    panel = FormulaPanel()
    qtbot.addWidget(panel)
    panel.show()
    panel.set_mode(AppMode.STUDENT)

    gA = _spur(tooth_count=20, rpm=100.0, is_driver=True)
    gB = _spur(tooth_count=40, rpm=50.0, pos=(240.0, 0.0), direction=Direction.CCW)
    conn = Connection(conn_type=ConnectionType.MESH, element_a=gA.id, element_b=gB.id)
    system = GearSystem(elements=[gA, gB], connections=[conn],
                        driver_rpm=100.0, driver_direction=Direction.CW)
    panel.update_for_system(system)
    text = panel.get_text()
    assert "40" in text or "20" in text


def test_formula_panel_clear(qtbot):
    """clear() sets the panel to an empty/placeholder state."""
    from gearlab.ui.formula_panel import FormulaPanel
    from gearlab.ui.mode import AppMode
    panel = FormulaPanel()
    qtbot.addWidget(panel)
    panel.show()
    panel.set_mode(AppMode.STUDENT)
    panel.clear()
    text = panel.get_text()
    assert text == "" or "no" in text.lower() or "connect" in text.lower()
