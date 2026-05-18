"""
MVP behavioral contract — add-gear → snap → correct rotation.

Three behaviors that MUST work for the core interaction loop.
All three FAIL before the fixes; all three must PASS after.
"""
import math
import pytest


# ---------------------------------------------------------------------------
# MVP-1  Snap activates when pitch circles are touching (1 × CD away)
# ---------------------------------------------------------------------------

def test_snap_activates_when_pitch_circles_touch():
    """
    Dragging a gear to exactly 1 × center-distance from an anchor (pitch
    circles just touching) must trigger snap.

    Old default snap_radius_frac=0.5:
        snap_radius = 0.5 × 240 = 120  →  dist 240 > 120  →  NO SNAP  (bug)
    Required default snap_radius_frac≥1.0:
        snap_radius ≥ 240              →  dist 240 ≤ radius →  SNAP    (pass)
    """
    from gearlab.canvas.snap import snap_position

    # 20T + 40T, M=8 → CD = pitch_radius(20,8) + pitch_radius(40,8) = 80+160 = 240
    result = snap_position((240.0, 0.0), 20, 8.0, [(0.0, 0.0, 40, 8.0)])
    assert result is not None, (
        "Gear placed at exactly 1×CD (pitch circles touching) must snap. "
        "Increase snap_radius_frac default so the snap range covers 1×CD."
    )
    # Result should be at (240, 0) — already at CD, so no movement needed
    assert abs(result[0] - 240.0) < 0.5
    assert abs(result[1] - 0.0) < 0.5


# ---------------------------------------------------------------------------
# MVP-2  New gear spawns in empty space (no overlap with existing gears)
# ---------------------------------------------------------------------------

def test_new_gear_spawns_without_overlap(qtbot):
    """
    Clicking 'Add Gear' (Engineer mode) must place the new gear in an area
    that does not visually overlap any existing gear.

    Current bug: gear spawns at mapToScene(viewport.center()) which lands
    approximately on top of the 40T demo gear after fitInView.
    """
    from gearlab.app import GearLabApp
    from gearlab.canvas.gear_geometry import addendum_radius
    from gearlab.canvas.gear_item import GearItem
    from gearlab.ui.mode import AppMode

    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)
    win._add_gear()

    items = [it for it in win._scene.items() if isinstance(it, GearItem)]
    for i, a in enumerate(items):
        for j, b in enumerate(items):
            if j <= i:
                continue
            dx = a.pos().x() - b.pos().x()
            dy = a.pos().y() - b.pos().y()
            dist = math.sqrt(dx * dx + dy * dy)
            r_a = addendum_radius(a._gear.tooth_count, a._gear.module)
            r_b = addendum_radius(b._gear.tooth_count, b._gear.module)
            # Require center-distance > 50 % of combined addendum radii
            assert dist > (r_a + r_b) * 0.5, (
                f"{a._gear.tooth_count}T @ ({a.pos().x():.0f},{a.pos().y():.0f}) "
                f"overlaps "
                f"{b._gear.tooth_count}T @ ({b.pos().x():.0f},{b.pos().y():.0f}) "
                f"— dist={dist:.0f}, threshold={(r_a + r_b) * 0.5:.0f}"
            )


# ---------------------------------------------------------------------------
# MVP-3  After drag-to-snap, new gear rotates opposite its neighbour
# ---------------------------------------------------------------------------

def test_snapped_gear_gets_opposite_direction(qtbot):
    """
    Drag a newly added gear to 0.8 × CD from gC (which is CW).
    After snap + rebuild the new gear must be CCW.

    Old snap_radius_frac=0.5:
        0.8×CD > 0.5×CD  →  no snap  →  gear disconnected  →  default CW  (bug)
    New snap_radius_frac≥1.0:
        0.8×CD < radius  →  snaps    →  mesh detected      →  CCW         (pass)
    """
    from gearlab.app import GearLabApp
    from gearlab.canvas.gear_geometry import pitch_radius
    from gearlab.canvas.gear_item import GearItem
    from gearlab.models import Direction
    from gearlab.ui.mode import AppMode

    win = GearLabApp()
    qtbot.addWidget(win)
    win._set_mode(AppMode.ENGINEER)

    # Capture item IDs before add so we can find the new one
    before_ids = set(win._items.keys())
    win._add_gear()
    new_id = (set(win._items.keys()) - before_ids).pop()
    new_item = win._items[new_id]

    # gC is the 20T demo gear at x ≈ 480, y = 0
    gC_item = next(
        it for it in win._scene.items()
        if isinstance(it, GearItem)
        and abs(it.pos().x() - 480.0) < 5
        and it._gear.id != new_id
    )

    # Place new gear at 0.8 × CD from gC
    # (outside old 0.5×CD snap range, inside new 1.5×CD snap range)
    cd = (pitch_radius(new_item._gear.tooth_count, new_item._gear.module)
          + pitch_radius(gC_item._gear.tooth_count, gC_item._gear.module))
    new_item.setPos(gC_item.pos().x() + cd * 0.8, gC_item.pos().y())
    win._try_snap(new_item)

    direction = getattr(new_item._gear, "_direction", None)
    assert direction == Direction.CCW, (
        f"Expected CCW (opposite to gC=CW), got {direction}. "
        "Gear snapped to a CW gear must rotate CCW."
    )
