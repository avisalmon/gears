"""
E05-S2 — Unit tests for PropertiesPanel and E05-S2 app features.
All tests must FAIL before implementation (TDD RED phase).
"""
import pytest

from gearlab.models import DefectType, Direction, Gear, GearType, ToothDefect


# ---------------------------------------------------------------------------
# Helper: create a test gear with direction set (post-solve state)
# ---------------------------------------------------------------------------

def _gear(tooth_count=20, module=8.0, rpm=100.0, is_driver=False,
          direction=Direction.CW, defects=None) -> Gear:
    g = Gear(gear_type=GearType.SPUR, tooth_count=tooth_count, module=module,
             position=(0.0, 0.0), is_driver=is_driver, rpm=rpm)
    g._direction = direction  # normally set by solve()
    if defects:
        g.defects = defects
    return g


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def panel(qtbot):
    from gearlab.ui.properties_panel import PropertiesPanel
    p = PropertiesPanel()
    qtbot.addWidget(p)
    p.show()
    return p


# ---------------------------------------------------------------------------
# E05-S2-02 Teeth populate
# ---------------------------------------------------------------------------

def test_panel_populates_teeth_spinbox(panel):
    """populate() sets the teeth spinbox to the gear's tooth count."""
    gear = _gear(tooth_count=30)
    panel.populate(gear)
    assert panel._teeth_spin.value() == 30


def test_panel_teeth_slider_syncs_with_spinbox(panel):
    """populate() syncs the slider to the same value as the spinbox."""
    gear = _gear(tooth_count=45)
    panel.populate(gear)
    assert panel._teeth_slider.value() == 45


# ---------------------------------------------------------------------------
# E05-S2-04 RPM and ratio display
# ---------------------------------------------------------------------------

def test_panel_shows_rpm_label(panel):
    """populate() writes the gear's RPM to the RPM label."""
    gear = _gear(rpm=75.0)
    panel.populate(gear)
    assert "75" in panel._rpm_label.text()


def test_panel_shows_ratio_when_provided(panel):
    """populate(gear, ratio=2.0) shows '2.00' in the ratio label."""
    gear = _gear()
    panel.populate(gear, ratio=2.0)
    assert "2.00" in panel._ratio_label.text()


def test_panel_shows_dash_ratio_when_not_provided(panel):
    """populate(gear) without ratio shows a dash."""
    gear = _gear()
    panel.populate(gear)
    assert panel._ratio_label.text() == "—"


# ---------------------------------------------------------------------------
# E05-S2-05 Direction indicator
# ---------------------------------------------------------------------------

def test_panel_shows_cw_direction(panel):
    """CW direction → label contains '↻'."""
    gear = _gear(direction=Direction.CW)
    panel.populate(gear)
    assert "↻" in panel._dir_label.text()


def test_panel_shows_ccw_direction(panel):
    """CCW direction → label contains '↺'."""
    gear = _gear(direction=Direction.CCW)
    panel.populate(gear)
    assert "↺" in panel._dir_label.text()


# ---------------------------------------------------------------------------
# E05-S2-02/03 Clear / no-selection state
# ---------------------------------------------------------------------------

def test_panel_clear_hides_form(panel):
    """clear() hides the properties form and shows the placeholder."""
    panel.populate(_gear())
    panel.clear()
    assert not panel._form_widget.isVisible()
    assert panel._no_sel_label.isVisible()


def test_panel_starts_in_clear_state(qtbot):
    """A fresh panel shows the 'no gear selected' placeholder."""
    from gearlab.ui.properties_panel import PropertiesPanel
    p = PropertiesPanel()
    qtbot.addWidget(p)
    p.show()
    assert panel_is_clear(p)


def panel_is_clear(p):
    return p._no_sel_label.isVisible() and not p._form_widget.isVisible()


# ---------------------------------------------------------------------------
# E05-S2-03 Module — Engineer-only
# ---------------------------------------------------------------------------

def test_module_hidden_in_student_mode(panel):
    """Module spin is hidden when not in engineer mode."""
    panel.set_engineer_mode(False)
    panel.populate(_gear())
    assert not panel._module_spin.isVisible()


def test_module_visible_in_engineer_mode(panel):
    """Module spin is visible in engineer mode."""
    panel.set_engineer_mode(True)
    panel.populate(_gear())
    assert panel._module_spin.isVisible()


# ---------------------------------------------------------------------------
# E05-S2-06 Defect toggle grid — Engineer-only
# ---------------------------------------------------------------------------

def test_defect_grid_hidden_in_student_mode(panel):
    """Defect grid is hidden when not in engineer mode."""
    panel.set_engineer_mode(False)
    panel.populate(_gear())
    assert not panel._defect_grid_widget.isVisible()


def test_defect_grid_visible_in_engineer_mode(panel):
    """Defect grid is visible in engineer mode."""
    panel.set_engineer_mode(True)
    panel.populate(_gear())
    assert panel._defect_grid_widget.isVisible()


def test_defect_grid_one_button_per_tooth(panel):
    """Engineer mode: defect grid has exactly tooth_count buttons."""
    panel.set_engineer_mode(True)
    panel.populate(_gear(tooth_count=15))
    assert len(panel._defect_buttons) == 15


def test_defect_grid_marks_existing_defects(panel):
    """Buttons for defective teeth are checked after populate()."""
    panel.set_engineer_mode(True)
    defect = ToothDefect(tooth_index=3, defect_type=DefectType.MISSING)
    gear = _gear(tooth_count=10, defects=[defect])
    panel.populate(gear)
    assert panel._defect_buttons[3].isChecked()
    assert not panel._defect_buttons[0].isChecked()


# ---------------------------------------------------------------------------
# E05-S2-07 Driver toggle
# ---------------------------------------------------------------------------

def test_driver_rpm_hidden_when_not_driver(panel):
    """Driver RPM spin is hidden for a non-driver gear."""
    panel.populate(_gear(is_driver=False))
    assert not panel._driver_rpm_spin.isVisible()


def test_driver_rpm_visible_for_driver(panel):
    """Driver RPM spin is visible for the driver gear."""
    panel.populate(_gear(is_driver=True, rpm=120.0))
    assert panel._driver_rpm_spin.isVisible()


# ---------------------------------------------------------------------------
# Signal emission
# ---------------------------------------------------------------------------

def test_tooth_count_signal_fires(panel, qtbot):
    """Changing the spinbox emits tooth_count_changed with the new value."""
    panel.populate(_gear(tooth_count=20))
    with qtbot.waitSignal(panel.tooth_count_changed, timeout=500) as blocker:
        panel._teeth_spin.setValue(25)
    assert blocker.args[0] == 25


def test_defect_signal_fires_on_toggle(panel, qtbot):
    """Clicking a defect button emits defect_toggled(index, True)."""
    panel.set_engineer_mode(True)
    panel.populate(_gear(tooth_count=8))
    with qtbot.waitSignal(panel.defect_toggled, timeout=500) as blocker:
        panel._defect_buttons[2].setChecked(True)
    assert blocker.args[0] == 2
    assert blocker.args[1] is True


# ---------------------------------------------------------------------------
# E05-S2-08 Status bar (app-level)
# ---------------------------------------------------------------------------

def test_status_bar_shows_mode(qtbot):
    """Status bar contains the current mode name after app initialises."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    msg = win.statusBar().currentMessage()
    assert "Explorer" in msg or "explorer" in msg.lower()


def test_status_bar_updates_on_mode_switch(qtbot):
    """Switching to Engineer mode updates the status bar."""
    from gearlab.app import GearLabApp
    from gearlab.ui.mode import AppMode
    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    msg = win.statusBar().currentMessage()
    assert "Engineer" in msg or "engineer" in msg.lower()


# ---------------------------------------------------------------------------
# E05-S2-09 "Why?" tooltip
# ---------------------------------------------------------------------------

def test_gear_items_have_nonempty_tooltip(qtbot):
    """Every GearItem in the demo scene has a non-empty tooltip after init."""
    from gearlab.app import GearLabApp
    from gearlab.canvas.gear_item import GearItem
    win = GearLabApp()
    qtbot.addWidget(win)
    items = [i for i in win._scene.items() if isinstance(i, GearItem)]
    assert len(items) > 0
    for item in items:
        assert item.toolTip(), f"GearItem has empty tooltip: {item}"
