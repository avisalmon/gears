"""
Animation controller — E03-S1-03/04/05.

AnimationController drives GearItem rotations in real time using a QTimer.
Each tick, it computes the angular delta for every gear based on its RPM,
direction, elapsed time, and the current speed multiplier.
"""
from __future__ import annotations

import math
from typing import Callable
from uuid import UUID

from PyQt6.QtCore import QObject, QTimer

from gearlab.models import DefectType, Direction, GearSystem


# ---------------------------------------------------------------------------
# Pure-math helpers (module-level for easy unit testing)
# ---------------------------------------------------------------------------

def defect_at_contact(
    tooth_index: int,
    rotation_deg: float,
    tooth_count: int,
    contact_angle_deg: float,
) -> bool:
    """
    Return True if the defective tooth at *tooth_index* is within half a tooth
    pitch of *contact_angle_deg* given the gear's current *rotation_deg*.
    """
    pitch_deg   = 360.0 / tooth_count
    tooth_angle = (rotation_deg + tooth_index * pitch_deg) % 360.0
    delta       = abs(tooth_angle - contact_angle_deg) % 360.0
    delta       = min(delta, 360.0 - delta)   # handle wrap-around
    return delta < pitch_deg * 0.5


def _contact_angle(pos_a: tuple[float, float], pos_b: tuple[float, float]) -> float:
    """Bearing angle (degrees) from pos_a toward pos_b in scene coordinates."""
    dx = pos_b[0] - pos_a[0]
    dy = pos_b[1] - pos_a[1]
    return math.degrees(math.atan2(dy, dx))

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_TICK_MS: int   = 16      # ~60 fps
_MIN_SPEED: float = 0.1
_MAX_SPEED: float = 10.0


# ---------------------------------------------------------------------------
# AnimationController
# ---------------------------------------------------------------------------

class AnimationController(QObject):
    """
    Drives rotation of GearItem instances at correct relative speeds.

    Usage
    -----
    ctrl = AnimationController(solved_system)
    for gear in system.elements:
        ctrl.register(gear.id, gear_item)
    ctrl.start()
    """

    def __init__(
        self,
        system: GearSystem,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._system: GearSystem = system
        self._speed: float       = 1.0
        self._angles: dict[UUID, float] = {
            g.id: 0.0 for g in system.elements
        }
        self._items: dict[UUID, object] = {}   # UUID → GearItem
        self._defect_callback: Callable[[UUID], None] | None = None

        self._timer = QTimer(self)
        self._timer.setInterval(_TICK_MS)
        self._timer.timeout.connect(self._tick)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_running(self) -> bool:
        return self._timer.isActive()

    @property
    def speed(self) -> float:
        return self._speed

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def register(self, gear_id: UUID, item: object) -> None:
        """Associate a gear UUID with its GearItem for angle updates.

        The item's current rotation() is used as the starting angle so that
        any initial phase offset applied before registration is preserved.
        This is what keeps meshing teeth in phase from the first tick onward.
        """
        self._items[gear_id] = item
        # Read the item's current rotation so the accumulated angle starts
        # at the same value — not at zero, which would lose the meshing offset.
        if callable(getattr(item, "rotation", None)):
            self._angles[gear_id] = item.rotation()  # type: ignore[union-attr]

    def set_defect_callback(
        self, callback: Callable[[UUID], None] | None
    ) -> None:
        """Register a callable fired when a defective tooth engages.

        The callback receives the gear UUID whose defective tooth caused
        the engagement event (typically used to trigger a visual flash).
        """
        self._defect_callback = callback

    def set_speed(self, value: float) -> None:
        """Set animation speed multiplier, clamped to [0.1, 10.0]."""
        self._speed = max(_MIN_SPEED, min(_MAX_SPEED, float(value)))

    def angle_for(self, gear_id: UUID) -> float:
        """Return the current accumulated angle (degrees) for a gear."""
        return self._angles.get(gear_id, 0.0)

    def start(self) -> None:
        """Start real-time animation."""
        self._timer.start()

    def pause(self) -> None:
        """Pause animation (preserves current angles)."""
        self._timer.stop()

    def step_frame(self) -> None:
        """Advance one tick manually (useful when paused)."""
        self._tick()

    # ------------------------------------------------------------------
    # Internal tick
    # ------------------------------------------------------------------

    def _tick(self) -> None:
        dt_sec = _TICK_MS / 1000.0 * self._speed

        # ---- Defect engagement detection --------------------------------
        # For each connection, check whether the driver's defective tooth
        # is at the contact point.  If so, fire the callback and skip the
        # driven gear's advance this tick (simulates a slip event).
        slipped: set[UUID] = set()
        if self._defect_callback is not None or self._system.connections:
            for conn in self._system.connections:
                for driver_id, driven_id in [
                    (conn.element_a, conn.element_b),
                    (conn.element_b, conn.element_a),
                ]:
                    driver = next(
                        (g for g in self._system.elements if g.id == driver_id), None
                    )
                    driven = next(
                        (g for g in self._system.elements if g.id == driven_id), None
                    )
                    if driver is None or driven is None or not driver.defects:
                        continue
                    contact = _contact_angle(driver.position, driven.position)
                    for defect in driver.defects:
                        if defect.defect_type != DefectType.MISSING:
                            continue
                        if defect_at_contact(
                            defect.tooth_index,
                            self._angles[driver.id],
                            driver.tooth_count,
                            contact,
                        ):
                            slipped.add(driven.id)
                            if self._defect_callback is not None:
                                self._defect_callback(driver.id)

        for g in self._system.elements:
            if g.rpm == 0.0:
                continue

            direction: Direction = getattr(g, "_direction", Direction.CW)
            deg_per_sec = g.rpm * 6.0          # rpm → degrees/second
            delta = deg_per_sec * dt_sec
            if direction == Direction.CCW:
                delta = -delta

            if g.id not in slipped:
                self._angles[g.id] = (self._angles[g.id] + delta) % 360.0

            item = self._items.get(g.id)
            if item is not None:
                item.set_angle(self._angles[g.id])  # type: ignore[attr-defined]
