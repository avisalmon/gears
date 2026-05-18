"""
Gear kinematics engine (E04-S1).
Implements spec §5.2–§5.4: ratio, RPM, direction, BFS traversal,
center-distance validation, and circular-loop detection.

Public API
----------
solve(system)                       → GearSystem  (new copy, originals untouched)
gear_ratio(driver_teeth, driven_teeth) → float
rpm_out(rpm_in, driver_teeth, driven_teeth) → float
center_distance(t1, t2, module)     → float
validate_center_distance(ga, gb)    → (bool, str | None)
detect_circular_loops(system)       → list[list[uuid.UUID]]
"""
from __future__ import annotations

import copy
import math
import uuid
from collections import deque
from typing import Optional

from gearlab.models import (
    Connection, ConnectionType, Direction,
    Gear, GearSystem, GearType,
)

# ── Tolerance for position comparisons (canvas units) ───────────────────────
_CD_TOLERANCE = 1.0   # allow ±1 unit before flagging mismatch


class KinematicsError(Exception):
    """Raised when the system cannot be solved (e.g., no driver found)."""


# ── Pure calculation helpers ─────────────────────────────────────────────────

def gear_ratio(driver_teeth: int, driven_teeth: int) -> float:
    """ratio = N_driven / N_driver  (spec §5.2.1)."""
    return driven_teeth / driver_teeth


def rpm_out(rpm_in: float, driver_teeth: int, driven_teeth: int) -> float:
    """RPM_out = RPM_in × (N_driver / N_driven)  (spec §5.2.2)."""
    return rpm_in * (driver_teeth / driven_teeth)


def center_distance(t1: int, t2: int, module: float) -> float:
    """C = (d1 + d2) / 2 = (t1 + t2) × module / 2  (spec §5.2.4)."""
    return (t1 + t2) * module / 2.0


def validate_center_distance(ga: Gear, gb: Gear) -> tuple[bool, Optional[str]]:
    """
    Check whether two gears are positioned at the correct center distance.
    Returns (True, None) if valid, (False, error_message) if not.
    Error message always includes a suggested fix (spec §5.4.5).
    """
    expected = center_distance(ga.tooth_count, gb.tooth_count, ga.module)
    ax, ay = ga.position
    bx, by = gb.position
    actual = math.hypot(bx - ax, by - ay)
    if abs(actual - expected) <= _CD_TOLERANCE:
        return True, None
    msg = (
        f"Center distance mismatch: expected {expected:.1f}, "
        f"got {actual:.1f}. "
        f"To fix: snap the gear to mesh or move it to distance {expected:.1f}."
    )
    return False, msg


# ── Direction propagation helpers ────────────────────────────────────────────

def _flip(direction: Direction) -> Direction:
    return Direction.CCW if direction == Direction.CW else Direction.CW


def _driven_direction(driver_gear: Gear, driven_gear: Gear,
                      conn: Connection, driver_dir: Direction) -> Direction:
    """
    Compute the direction of the driven gear given its driver and connection.

    Rules (spec §5.2.3):
    - External mesh (spur↔spur):   reverses direction
    - Internal mesh (spur↔ring):   preserves direction
    - Belt uncrossed:               preserves direction
    - Belt crossed:                 reverses direction
    - Chain:                        preserves direction
    """
    if conn.conn_type == ConnectionType.MESH:
        if driven_gear.gear_type == GearType.RING:
            return driver_dir          # internal mesh — same direction
        return _flip(driver_dir)       # external mesh — reverses

    if conn.conn_type == ConnectionType.BELT:
        return _flip(driver_dir) if conn.crossed else driver_dir

    if conn.conn_type == ConnectionType.CHAIN:
        return driver_dir

    # RACK connection — not a rotational output, treat as same direction
    return driver_dir


# ── BFS solver ───────────────────────────────────────────────────────────────

def solve(system: GearSystem) -> GearSystem:
    """
    Propagate RPM and direction from the driver to every reachable element.

    Returns a deep copy of the GearSystem with updated `rpm` and `_direction`
    fields on each Gear.  The original system is never mutated.

    Raises KinematicsError if no driver gear is found.
    """
    result: GearSystem = copy.deepcopy(system)

    # Index elements by id for O(1) lookup
    by_id: dict[uuid.UUID, Gear] = {g.id: g for g in result.elements}

    # Build adjacency: gear_id → list of (neighbour_id, Connection)
    adj: dict[uuid.UUID, list[tuple[uuid.UUID, Connection]]] = {
        g.id: [] for g in result.elements
    }
    for conn in result.connections:
        adj[conn.element_a].append((conn.element_b, conn))
        adj[conn.element_b].append((conn.element_a, conn))

    # Find driver
    drivers = [g for g in result.elements if g.is_driver]
    if not drivers:
        raise KinematicsError("No driver gear found in GearSystem.")
    driver = drivers[0]

    # Initialise driver
    driver._direction = result.driver_direction  # type: ignore[attr-defined]
    driver.rpm = result.driver_rpm

    # BFS
    visited: set[uuid.UUID] = {driver.id}
    queue: deque[uuid.UUID] = deque([driver.id])

    while queue:
        current_id = queue.popleft()
        current = by_id[current_id]

        for neighbour_id, conn in adj[current_id]:
            if neighbour_id in visited:
                continue
            visited.add(neighbour_id)
            neighbour = by_id[neighbour_id]

            # Determine which end is driver vs driven for this connection
            if conn.element_a == current_id:
                driver_teeth  = current.tooth_count
                driven_teeth  = neighbour.tooth_count
                driver_node   = current
                driven_node   = neighbour
            else:
                driver_teeth  = current.tooth_count
                driven_teeth  = neighbour.tooth_count
                driver_node   = current
                driven_node   = neighbour

            neighbour.rpm = rpm_out(current.rpm, driver_teeth, driven_teeth)
            neighbour._direction = _driven_direction(  # type: ignore[attr-defined]
                driver_node, driven_node, conn, current._direction  # type: ignore[attr-defined]
            )
            queue.append(neighbour_id)

    # Gears never reached by BFS: zero their RPM so they don't spin.
    for g in result.elements:
        if g.id not in visited:
            g.rpm = 0.0
        if not hasattr(g, "_direction"):
            g._direction = Direction.CW  # type: ignore[attr-defined]

    return result


def has_direction_conflict(system: GearSystem) -> bool:
    """
    Return True if any connection in the *solved* system has contradictory
    gear directions (e.g. a gear caught between two gears that demand it spin
    in opposite directions simultaneously).

    Must be called on the result of solve(), not the raw system.
    """
    by_id: dict[uuid.UUID, Gear] = {g.id: g for g in system.elements}
    for conn in system.connections:
        ga = by_id.get(conn.element_a)
        gb = by_id.get(conn.element_b)
        if ga is None or gb is None:
            continue
        dir_a = getattr(ga, "_direction", None)
        dir_b = getattr(gb, "_direction", None)
        if dir_a is None or dir_b is None:
            continue
        # Skip pairs where neither gear is actually spinning
        if ga.rpm == 0.0 and gb.rpm == 0.0:
            continue
        expected_b = _driven_direction(ga, gb, conn, dir_a)
        if expected_b != dir_b:
            return True
    return False


# ── Loop detection ───────────────────────────────────────────────────────────

def detect_circular_loops(system: GearSystem) -> list[list[uuid.UUID]]:
    """
    Return a list of cycles found in the gear graph.
    Each cycle is a list of gear UUIDs forming a closed loop.
    Returns [] if no loops exist.
    Uses DFS with colouring (white/grey/black).
    """
    adj: dict[uuid.UUID, list[uuid.UUID]] = {
        g.id: [] for g in system.elements
    }
    for conn in system.connections:
        adj[conn.element_a].append(conn.element_b)
        adj[conn.element_b].append(conn.element_a)

    WHITE, GREY, BLACK = 0, 1, 2
    colour: dict[uuid.UUID, int] = {g.id: WHITE for g in system.elements}
    parent: dict[uuid.UUID, Optional[uuid.UUID]] = {g.id: None for g in system.elements}
    loops: list[list[uuid.UUID]] = []

    def dfs(node: uuid.UUID) -> None:
        colour[node] = GREY
        for neighbour in adj[node]:
            if colour[neighbour] == GREY and parent[node] != neighbour:
                # Back-edge found — record the loop
                loops.append([node, neighbour])
            elif colour[neighbour] == WHITE:
                parent[neighbour] = node
                dfs(neighbour)
        colour[node] = BLACK

    for g in system.elements:
        if colour[g.id] == WHITE:
            dfs(g.id)

    return loops
