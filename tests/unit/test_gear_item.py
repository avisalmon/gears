"""
E03-S1-02, E03-S1-07 — Unit tests for GearItem (QGraphicsItem subclass).
Covers: construction, bounding rect, rotation, direction color.
All tests must FAIL before GearItem is implemented.
"""
import pytest

from gearlab.canvas.gear_item import GearItem
from gearlab.canvas.gear_geometry import addendum_radius
from gearlab.models import Direction, Gear, GearType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _spur_gear(**kwargs) -> Gear:
    defaults = dict(gear_type=GearType.SPUR, tooth_count=20,
                    module=8.0, position=(0.0, 0.0))
    defaults.update(kwargs)
    return Gear(**defaults)


# ---------------------------------------------------------------------------
# E03-S1-02 — GearItem construction
# ---------------------------------------------------------------------------

def test_gear_item_creates(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    assert item is not None


def test_gear_item_bounding_rect_at_least_addendum(qtbot):
    """BoundingRect must encompass the full addendum circle."""
    gear = _spur_gear(tooth_count=20, module=8.0)
    item = GearItem(gear)
    r_a = addendum_radius(20, 8.0)
    br = item.boundingRect()
    assert br.width() >= 2 * r_a
    assert br.height() >= 2 * r_a


def test_gear_item_positioned_at_gear_position(qtbot):
    """Item pos() must match gear.position."""
    gear = _spur_gear(position=(120.0, -80.0))
    item = GearItem(gear)
    assert abs(item.x() - 120.0) < 0.001
    assert abs(item.y() - (-80.0)) < 0.001


# ---------------------------------------------------------------------------
# E03-S1-02 — set_angle
# ---------------------------------------------------------------------------

def test_gear_item_set_angle(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    item.set_angle(45.0)
    assert abs(item.rotation() - 45.0) < 0.001


def test_gear_item_set_angle_wraps(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    item.set_angle(720.0)
    # set_angle stores the value passed; Qt normalizes internally
    assert item.rotation() == pytest.approx(720.0)


# ---------------------------------------------------------------------------
# E03-S1-07 — direction color (smoke test — no visual comparison, just no crash)
# ---------------------------------------------------------------------------

def test_gear_item_set_direction_cw(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    item.set_direction(Direction.CW)   # must not raise


def test_gear_item_set_direction_ccw(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    item.set_direction(Direction.CCW)  # must not raise


def test_gear_item_set_direction_none(qtbot):
    gear = _spur_gear()
    item = GearItem(gear)
    item.set_direction(None)           # must not raise
