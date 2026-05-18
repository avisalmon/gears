"""
E03-S1-03, E03-S1-04, E03-S1-05 — Unit tests for AnimationController.
Covers: start/pause state, speed clamping, step-frame, register items.
All tests must FAIL before animation.py is implemented.
"""
import pytest

from gearlab.canvas.animation import AnimationController
from gearlab.models import (
    Connection, ConnectionType, Direction,
    Gear, GearSystem, GearType,
)
from gearlab.engine.kinematics import solve


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _two_gear_system() -> GearSystem:
    gA = Gear(gear_type=GearType.SPUR, tooth_count=20, module=8.0,
              position=(0.0, 0.0), is_driver=True, rpm=100.0)
    gB = Gear(gear_type=GearType.SPUR, tooth_count=40, module=8.0,
              position=(240.0, 0.0))
    conn = Connection(conn_type=ConnectionType.MESH,
                      element_a=gA.id, element_b=gB.id)
    system = GearSystem(elements=[gA, gB], connections=[conn],
                        driver_rpm=100.0, driver_direction=Direction.CW)
    return solve(system)


# ---------------------------------------------------------------------------
# E03-S1-03 — start / pause state
# ---------------------------------------------------------------------------

def test_controller_starts_stopped(qtbot):
    ctrl = AnimationController(_two_gear_system())
    assert not ctrl.is_running


def test_controller_start(qtbot):
    ctrl = AnimationController(_two_gear_system())
    ctrl.start()
    assert ctrl.is_running
    ctrl.pause()   # cleanup


def test_controller_pause(qtbot):
    ctrl = AnimationController(_two_gear_system())
    ctrl.start()
    ctrl.pause()
    assert not ctrl.is_running


# ---------------------------------------------------------------------------
# E03-S1-04 — speed property
# ---------------------------------------------------------------------------

def test_controller_default_speed(qtbot):
    ctrl = AnimationController(_two_gear_system())
    assert ctrl.speed == pytest.approx(1.0)


def test_controller_set_speed(qtbot):
    ctrl = AnimationController(_two_gear_system())
    ctrl.set_speed(3.0)
    assert ctrl.speed == pytest.approx(3.0)


def test_controller_speed_clamped_low(qtbot):
    ctrl = AnimationController(_two_gear_system())
    ctrl.set_speed(0.0)
    assert ctrl.speed >= 0.1


def test_controller_speed_clamped_high(qtbot):
    ctrl = AnimationController(_two_gear_system())
    ctrl.set_speed(999.0)
    assert ctrl.speed <= 10.0


# ---------------------------------------------------------------------------
# E03-S1-05 — step-frame
# ---------------------------------------------------------------------------

def test_controller_step_frame_no_error(qtbot):
    """step_frame() must not raise, even without registered items."""
    ctrl = AnimationController(_two_gear_system())
    ctrl.step_frame()   # should not raise


def test_controller_step_advances_angle(qtbot):
    """step_frame() must advance the driver gear's internal angle."""
    system = _two_gear_system()
    ctrl = AnimationController(system)
    driver = next(g for g in system.elements if g.is_driver)
    before = ctrl.angle_for(driver.id)
    ctrl.step_frame()
    after = ctrl.angle_for(driver.id)
    assert after != before   # angle must change (driver has rpm > 0)


# ---------------------------------------------------------------------------
# Register API
# ---------------------------------------------------------------------------

def test_controller_register_item(qtbot):
    """register() must not raise for a valid gear UUID."""
    from gearlab.canvas.gear_item import GearItem
    system = _two_gear_system()
    ctrl = AnimationController(system)
    gear = system.elements[0]
    item = GearItem(gear)
    ctrl.register(gear.id, item)   # must not raise
