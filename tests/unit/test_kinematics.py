"""
E04-S1 kinematics engine tests.
Covers: ratio, RPM propagation, direction rules, BFS traversal,
        center-distance validation, circular loop detection.
All per spec §5.2–§5.4.
"""
import copy
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
SRC  = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gearlab.engine.kinematics import (
    KinematicsError,
    solve,
    gear_ratio,
    rpm_out,
    center_distance,
    validate_center_distance,
    detect_circular_loops,
)
from gearlab.models import (
    Connection, ConnectionType, Direction,
    Gear, GearSystem, GearType,
)


# ── helpers ──────────────────────────────────────────────────────────────────

M = 2  # module used throughout (keeps numbers small)


def spur(tooth_count, rpm=0.0, is_driver=False, pos=(0.0, 0.0)):
    return Gear(gear_type=GearType.SPUR, tooth_count=tooth_count,
                module=M, position=pos, rpm=rpm, is_driver=is_driver)


def ring(tooth_count, pos=(0.0, 0.0)):
    return Gear(gear_type=GearType.RING, tooth_count=tooth_count,
                module=M, position=pos)


def pulley(tooth_count, pos=(0.0, 0.0)):
    return Gear(gear_type=GearType.PULLEY, tooth_count=tooth_count,
                module=M, position=pos)


def idler(tooth_count, pos=(0.0, 0.0)):
    return Gear(gear_type=GearType.IDLER, tooth_count=tooth_count,
                module=M, position=pos)


def mesh(a, b):
    return Connection(conn_type=ConnectionType.MESH,
                      element_a=a.id, element_b=b.id)


def belt(a, b, crossed=False):
    return Connection(conn_type=ConnectionType.BELT,
                      element_a=a.id, element_b=b.id, crossed=crossed)


def chain(a, b):
    return Connection(conn_type=ConnectionType.CHAIN,
                      element_a=a.id, element_b=b.id)


def system(driver, others, connections, driver_rpm=100.0,
           driver_dir=Direction.CW):
    driver.is_driver = True
    driver.rpm = driver_rpm
    return GearSystem(
        elements=[driver] + others,
        connections=connections,
        driver_rpm=driver_rpm,
        driver_direction=driver_dir,
    )


# ── E04-S1-01 : gear_ratio() ─────────────────────────────────────────────────

def test_gear_ratio_2_to_1():
    assert gear_ratio(driver_teeth=20, driven_teeth=40) == 2.0


def test_gear_ratio_1_to_2():
    assert gear_ratio(driver_teeth=40, driven_teeth=20) == 0.5


def test_gear_ratio_equal():
    assert gear_ratio(driver_teeth=24, driven_teeth=24) == 1.0


# ── E04-S1-02 : rpm_out() ────────────────────────────────────────────────────

def test_rpm_out_halved_for_2_to_1():
    assert rpm_out(rpm_in=120.0, driver_teeth=20, driven_teeth=40) == 60.0


def test_rpm_out_doubled_for_1_to_2():
    assert rpm_out(rpm_in=100.0, driver_teeth=40, driven_teeth=20) == 200.0


def test_rpm_out_unchanged_for_equal_teeth():
    assert rpm_out(rpm_in=75.0, driver_teeth=30, driven_teeth=30) == 75.0


# ── E04-S1-03 : direction rules ──────────────────────────────────────────────

def test_external_mesh_reverses_direction():
    """Spur-to-spur mesh always reverses direction."""
    gA = spur(20, rpm=100.0, is_driver=True)
    gB = spur(40)
    sys_ = system(gA, [gB], [mesh(gA, gB)])
    result = solve(sys_)
    gB_out = next(g for g in result.elements if g.id == gB.id)
    assert gB_out.rpm == 50.0
    # driver is CW → driven must be CCW
    assert result.driver_direction == Direction.CW
    # direction stored per-element after solve
    assert gB_out._direction == Direction.CCW


def test_ring_gear_preserves_direction():
    """Internal (ring) mesh preserves direction (spec §5.2.3)."""
    gA = spur(20, rpm=100.0, is_driver=True)
    gR = ring(40)
    sys_ = system(gA, [gR], [mesh(gA, gR)])
    result = solve(sys_)
    gR_out = next(g for g in result.elements if g.id == gR.id)
    assert gR_out._direction == Direction.CW


def test_two_external_meshes_restore_direction():
    """Two external meshes: driver CW → intermediate CCW → output CW."""
    gA = spur(20, rpm=120.0, is_driver=True)
    gB = spur(20)
    gC = spur(20)
    sys_ = system(gA, [gB, gC], [mesh(gA, gB), mesh(gB, gC)])
    result = solve(sys_)
    gC_out = next(g for g in result.elements if g.id == gC.id)
    assert gC_out._direction == Direction.CW


def test_uncrossed_belt_preserves_direction():
    pA = pulley(20, pos=(0.0, 0.0))
    pB = pulley(40, pos=(120.0, 0.0))
    pA.is_driver = True
    pA.rpm = 100.0
    sys_ = GearSystem(elements=[pA, pB], connections=[belt(pA, pB)],
                      driver_rpm=100.0, driver_direction=Direction.CW)
    result = solve(sys_)
    pB_out = next(g for g in result.elements if g.id == pB.id)
    assert pB_out._direction == Direction.CW


def test_crossed_belt_reverses_direction():
    pA = pulley(20, pos=(0.0, 0.0))
    pB = pulley(40, pos=(120.0, 0.0))
    pA.is_driver = True
    pA.rpm = 100.0
    sys_ = GearSystem(elements=[pA, pB], connections=[belt(pA, pB, crossed=True)],
                      driver_rpm=100.0, driver_direction=Direction.CW)
    result = solve(sys_)
    pB_out = next(g for g in result.elements if g.id == pB.id)
    assert pB_out._direction == Direction.CCW


def test_chain_preserves_direction():
    sA = pulley(16, pos=(0.0, 0.0))
    sB = pulley(32, pos=(96.0, 0.0))
    sA.is_driver = True
    sA.rpm = 90.0
    sys_ = GearSystem(elements=[sA, sB], connections=[chain(sA, sB)],
                      driver_rpm=90.0, driver_direction=Direction.CW)
    result = solve(sys_)
    sB_out = next(g for g in result.elements if g.id == sB.id)
    assert sB_out._direction == Direction.CW
    assert sB_out.rpm == 45.0


# ── E04-S1-04 : BFS traversal ────────────────────────────────────────────────

def test_bfs_propagates_through_three_gear_chain():
    """Driver → B → C: RPM and direction propagate correctly."""
    gA = spur(10, rpm=120.0, is_driver=True)
    gB = spur(20)   # rpm should be 60
    gC = spur(10)   # rpm should be 120 again (60 × 20/10)
    sys_ = system(gA, [gB, gC], [mesh(gA, gB), mesh(gB, gC)],
                  driver_rpm=120.0)
    result = solve(sys_)
    gB_out = next(g for g in result.elements if g.id == gB.id)
    gC_out = next(g for g in result.elements if g.id == gC.id)
    assert gB_out.rpm == pytest.approx(60.0)
    assert gC_out.rpm == pytest.approx(120.0)


def test_bfs_unreachable_gear_stays_zero_rpm():
    """A gear with no connection path from driver keeps rpm=0."""
    gA = spur(20, rpm=100.0, is_driver=True)
    gB = spur(20)  # connected
    gX = spur(20)  # disconnected — no connection involving gX
    sys_ = GearSystem(
        elements=[gA, gB, gX],
        connections=[mesh(gA, gB)],
        driver_rpm=100.0, driver_direction=Direction.CW,
    )
    result = solve(sys_)
    gX_out = next(g for g in result.elements if g.id == gX.id)
    assert gX_out.rpm == 0.0


def test_idler_reverses_direction_without_changing_ratio():
    """Idler gear: changes direction of downstream gear, does not affect ratio."""
    gA   = spur(20,  rpm=100.0, is_driver=True)
    gIdle = idler(15)                          # tooth count irrelevant for ratio
    gC   = spur(20)
    sys_ = system(gA, [gIdle, gC],
                  [mesh(gA, gIdle), mesh(gIdle, gC)])
    result = solve(sys_)
    gC_out  = next(g for g in result.elements if g.id == gC.id)
    gA_driver = next(g for g in result.elements if g.id == gA.id)
    # RPM of C should equal driver RPM (same tooth count, idler in between)
    assert gC_out.rpm == pytest.approx(100.0)
    # But direction should be same as driver (two reversals = CW → CCW → CW)
    assert gC_out._direction == Direction.CW


def test_solve_returns_new_gearsystem_not_mutated_in_place():
    """solve() must return a new GearSystem; original must be unchanged."""
    gA = spur(20, rpm=100.0, is_driver=True)
    gB = spur(40)
    original_rpm = gB.rpm
    sys_ = system(gA, [gB], [mesh(gA, gB)])
    result = solve(sys_)
    assert gB.rpm == original_rpm  # original unchanged


# ── E04-S1-07 : center distance validation ───────────────────────────────────

def test_center_distance_correct():
    """C = (d1 + d2) / 2 = (N1 + N2) × module / 2."""
    assert center_distance(20, 40, module=2) == 60.0


def test_validate_center_distance_ok():
    gA = spur(20, pos=(0.0, 0.0))
    gB = spur(40, pos=(60.0, 0.0))   # correct center distance = 60
    ok, err = validate_center_distance(gA, gB)
    assert ok is True
    assert err is None


def test_validate_center_distance_mismatch_returns_error():
    gA = spur(20, pos=(0.0, 0.0))
    gB = spur(40, pos=(99.0, 0.0))   # wrong — should be 60
    ok, err = validate_center_distance(gA, gB)
    assert ok is False
    assert err is not None
    assert "center distance" in err.lower()
    assert "fix" in err.lower() or "move" in err.lower() or "snap" in err.lower()


# ── E04-S1-08 : circular loop detection ─────────────────────────────────────

def test_no_loop_detected_in_simple_chain():
    gA = spur(20, is_driver=True)
    gB = spur(40)
    sys_ = system(gA, [gB], [mesh(gA, gB)])
    loops = detect_circular_loops(sys_)
    assert loops == []


def test_circular_loop_detected():
    """A→B→C→A forms a loop and must be flagged."""
    gA = spur(20, is_driver=True)
    gB = spur(20)
    gC = spur(20)
    sys_ = system(gA, [gB, gC],
                  [mesh(gA, gB), mesh(gB, gC), mesh(gC, gA)])
    loops = detect_circular_loops(sys_)
    assert len(loops) > 0


import pytest  # needed for approx — import after test definitions is fine
