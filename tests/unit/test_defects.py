"""
E04-S2 — Unit tests for defect simulation.
Covers: defect geometry (missing/chipped), engagement detection, flash callback.
All tests must FAIL before implementation.
"""
import pytest
from unittest.mock import MagicMock

from gearlab.canvas.gear_geometry import spur_gear_path
from gearlab.canvas.animation import defect_at_contact
from gearlab.models import (
    Connection, ConnectionType, DefectType, Direction,
    Gear, GearSystem, GearType, ToothDefect,
)
from gearlab.engine.kinematics import solve


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _spur(tooth_count=20, module=8.0, **kw) -> Gear:
    return Gear(gear_type=GearType.SPUR, tooth_count=tooth_count,
                module=module, position=(0.0, 0.0), **kw)


def _system_with_defect(driver_defects=None) -> GearSystem:
    """Two-gear system; driver (20T) has the given defects if provided."""
    gA = Gear(gear_type=GearType.SPUR, tooth_count=20, module=8.0,
              position=(0.0, 0.0), is_driver=True, rpm=100.0)
    if driver_defects:
        gA.defects = driver_defects
    gB = Gear(gear_type=GearType.SPUR, tooth_count=40, module=8.0,
              position=(240.0, 0.0))
    conn = Connection(conn_type=ConnectionType.MESH,
                      element_a=gA.id, element_b=gB.id)
    system = GearSystem(elements=[gA, gB], connections=[conn],
                        driver_rpm=100.0, driver_direction=Direction.CW)
    return solve(system)


# ---------------------------------------------------------------------------
# E04-S2-01 — Missing tooth geometry
# ---------------------------------------------------------------------------

def test_missing_tooth_path_differs_from_normal():
    """A gear with a missing tooth must produce a different path."""
    p_normal = spur_gear_path(20, 8.0)
    p_defect = spur_gear_path(20, 8.0, defect_map={0: DefectType.MISSING})
    assert p_normal.boundingRect() != p_defect.boundingRect() or \
           p_normal.elementCount() != p_defect.elementCount()


def test_missing_tooth_path_not_empty():
    p = spur_gear_path(20, 8.0, defect_map={0: DefectType.MISSING})
    assert not p.isEmpty()


def test_missing_tooth_has_smaller_bounding_rect():
    """Missing tooth reduces the outer extent."""
    p_normal = spur_gear_path(20, 8.0)
    p_defect = spur_gear_path(20, 8.0, defect_map={0: DefectType.MISSING})
    # Defective path must be smaller in at least one dimension
    n_area = p_normal.boundingRect().width() * p_normal.boundingRect().height()
    d_area = p_defect.boundingRect().width() * p_defect.boundingRect().height()
    assert d_area < n_area


# ---------------------------------------------------------------------------
# E04-S2-02 — Chipped tooth geometry
# ---------------------------------------------------------------------------

def test_chipped_tooth_path_differs_from_normal():
    p_normal = spur_gear_path(20, 8.0)
    p_defect = spur_gear_path(20, 8.0, defect_map={5: DefectType.CHIPPED})
    assert p_normal.elementCount() != p_defect.elementCount() or \
           p_normal.boundingRect() != p_defect.boundingRect()


def test_chipped_tooth_path_not_empty():
    p = spur_gear_path(20, 8.0, defect_map={5: DefectType.CHIPPED})
    assert not p.isEmpty()


def test_multiple_defects_path_not_empty():
    dm = {0: DefectType.MISSING, 5: DefectType.CHIPPED, 10: DefectType.MISSING}
    p = spur_gear_path(20, 8.0, defect_map=dm)
    assert not p.isEmpty()


def test_empty_defect_map_same_as_none():
    """Passing an empty defect_map must produce the same path as no defects."""
    p_none = spur_gear_path(20, 8.0)
    p_empty = spur_gear_path(20, 8.0, defect_map={})
    assert p_none.elementCount() == p_empty.elementCount()


# ---------------------------------------------------------------------------
# E04-S2-04 / E04-S2-08 — defect_at_contact geometry (pure math)
# ---------------------------------------------------------------------------

def test_defect_at_contact_tooth0_at_0_contact0():
    """Tooth 0 at rotation=0°, 20T gear, contact at 0° — must detect."""
    assert defect_at_contact(0, 0.0, 20, 0.0)


def test_defect_at_contact_within_threshold():
    """Tooth 0 at rotation=8° (< half-pitch=9°) — still detected."""
    assert defect_at_contact(0, 8.0, 20, 0.0)


def test_defect_at_contact_beyond_threshold():
    """Tooth 0 at rotation=10° (> half-pitch=9°) — not detected."""
    assert not defect_at_contact(0, 10.0, 20, 0.0)


def test_defect_at_contact_wrong_tooth():
    """Tooth 1 of 20T gear at rotation=0° is at 18° — not near 0° contact."""
    assert not defect_at_contact(1, 0.0, 20, 0.0)


@pytest.mark.parametrize("tooth_count", [8, 12, 20])
def test_defect_at_contact_tooth0_center_for_various_sizes(tooth_count):
    """Tooth 0 at exact contact angle must always be detected."""
    assert defect_at_contact(0, 0.0, tooth_count, 0.0)


def test_defect_at_contact_wraparound():
    """Tooth at 359° should be detected at contact=0° (wraparound)."""
    # 20T: pitch=18°, tooth 0 at rotation=359° → 359° from 0° = 1° delta < 9°
    assert defect_at_contact(0, 359.0, 20, 0.0)


# ---------------------------------------------------------------------------
# E04-S2-05 — GearItem flash (visual; smoke-test only)
# ---------------------------------------------------------------------------

def test_gear_item_with_missing_tooth_renders(qtbot):
    from gearlab.canvas.gear_item import GearItem
    gear = _spur()
    gear.defects = [ToothDefect(tooth_index=0, defect_type=DefectType.MISSING)]
    item = GearItem(gear)
    assert not item.boundingRect().isEmpty()


def test_gear_item_flash_no_crash(qtbot):
    from gearlab.canvas.gear_item import GearItem
    gear = _spur()
    item = GearItem(gear)
    item.flash()   # must not raise


# ---------------------------------------------------------------------------
# E04-S2-05 — AnimationController defect callback
# ---------------------------------------------------------------------------

def test_defect_callback_fires_when_tooth_at_contact(qtbot):
    """Callback must fire when driver's missing tooth is at the contact point."""
    from gearlab.canvas.animation import AnimationController
    defects = [ToothDefect(tooth_index=0, defect_type=DefectType.MISSING)]
    system = _system_with_defect(driver_defects=defects)
    ctrl = AnimationController(system)
    cb = MagicMock()
    ctrl.set_defect_callback(cb)
    # At rotation=0 tooth 0 of driver is at 0° = contact direction toward B
    ctrl.step_frame()
    cb.assert_called()


def test_defect_callback_not_fired_without_defect(qtbot):
    """Callback must not fire for a system with no defects."""
    from gearlab.canvas.animation import AnimationController
    system = _system_with_defect()   # no defects
    ctrl = AnimationController(system)
    cb = MagicMock()
    ctrl.set_defect_callback(cb)
    ctrl.step_frame()
    cb.assert_not_called()
