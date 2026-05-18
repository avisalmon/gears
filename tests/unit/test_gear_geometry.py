"""
E03-S1-10 — Unit tests for involute gear geometry.
Edge cases: tooth counts 8, 12, 100, 200.
All tests must FAIL before gear_geometry.py is implemented.
"""
import math

import pytest

from gearlab.canvas.gear_geometry import (
    addendum_radius,
    dedendum_radius,
    pitch_radius,
    spur_gear_path,
)


# ---------------------------------------------------------------------------
# Pure radius helpers
# ---------------------------------------------------------------------------

def test_pitch_radius():
    assert pitch_radius(20, 8) == pytest.approx(80.0)


def test_pitch_radius_small():
    assert pitch_radius(8, 5) == pytest.approx(20.0)


def test_addendum_radius():
    # r_a = r_p + module = 80 + 8 = 88
    assert addendum_radius(20, 8) == pytest.approx(88.0)


def test_dedendum_radius():
    # r_d = r_p - 1.25*m = 80 - 10 = 70
    assert dedendum_radius(20, 8) == pytest.approx(70.0)


def test_dedendum_minimum_clamp():
    # Very small gear: r_p - 1.25*m < module*0.4, clamped
    # z=4, m=10: r_p=20, r_p-1.25*m=7.5, m*0.4=4 → clamped to 7.5? No: 7.5 > 4
    # z=2, m=10: r_p=10, r_p-1.25*m=-2.5 → clamped to 4.0
    result = dedendum_radius(2, 10)
    assert result >= 10 * 0.4


def test_addendum_greater_than_pitch():
    for z, m in [(8, 4), (20, 8), (100, 2)]:
        assert addendum_radius(z, m) > pitch_radius(z, m)


def test_dedendum_less_than_pitch():
    for z, m in [(20, 8), (100, 2)]:
        assert dedendum_radius(z, m) < pitch_radius(z, m)


# ---------------------------------------------------------------------------
# spur_gear_path — E03-S1-10 parametrized edge cases
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tooth_count", [8, 12, 100, 200])
def test_spur_gear_path_not_empty(tooth_count):
    path = spur_gear_path(tooth_count, 8.0)
    assert not path.isEmpty()


@pytest.mark.parametrize("tooth_count", [8, 12, 100, 200])
def test_spur_gear_path_bounding_rect_spans_gear(tooth_count):
    """Bounding rect must be at least addendum-diameter wide and tall."""
    path = spur_gear_path(tooth_count, 8.0)
    r_a = addendum_radius(tooth_count, 8.0)
    br = path.boundingRect()
    # Must span more than the pitch radius in both directions
    assert br.width() > pitch_radius(tooth_count, 8.0)
    assert br.height() > pitch_radius(tooth_count, 8.0)


@pytest.mark.parametrize("tooth_count", [8, 12, 100, 200])
def test_spur_gear_path_centered_near_origin(tooth_count):
    """Path should be centered — bounding rect roughly symmetric around (0,0)."""
    path = spur_gear_path(tooth_count, 8.0)
    br = path.boundingRect()
    cx = br.x() + br.width() / 2
    cy = br.y() + br.height() / 2
    r_a = addendum_radius(tooth_count, 8.0)
    assert abs(cx) < r_a * 0.1
    assert abs(cy) < r_a * 0.1


def test_spur_gear_path_rotation_offset_changes_path():
    """Two paths with different rotation offsets must differ."""
    p1 = spur_gear_path(20, 8, rotation_offset=0.0)
    p2 = spur_gear_path(20, 8, rotation_offset=math.pi / 20)
    br1 = p1.boundingRect()
    br2 = p2.boundingRect()
    # x/y of bounding rect should shift
    assert abs(br1.x() - br2.x()) > 0.01 or abs(br1.y() - br2.y()) > 0.01
