"""
Snap-to-mesh geometry — E03-S2-02.

Pure math; no Qt dependency.  The snap algorithm finds the nearest anchor
gear to the dragged gear and, if it is within the snap radius, returns the
exact center-distance position so the two pitch circles touch perfectly.
"""
from __future__ import annotations

import math

from gearlab.canvas.gear_geometry import pitch_radius


def snap_position(
    drag_pos: tuple[float, float],
    tooth_count: int,
    module: float,
    anchors: list[tuple[float, float, int, float]],
    snap_radius_frac: float = 0.5,
) -> tuple[float, float] | None:
    """
    Return the snapped (x, y) position or *None* if no anchor is close enough.

    Parameters
    ----------
    drag_pos        : current drag position (scene coords)
    tooth_count     : tooth count of the gear being dragged
    module          : module of the gear being dragged
    anchors         : list of (x, y, tooth_count, module) for all other gears
    snap_radius_frac: fraction of center distance used as the snap activation
                      radius (default 0.5 = snap when within half the CD)

    The function finds the *closest* anchor within snap range and returns
    the point at exact center distance from that anchor in the drag direction.
    """
    drag_r = pitch_radius(tooth_count, module)
    dx0, dy0 = drag_pos

    best_pos: tuple[float, float] | None = None
    best_dist = float("inf")

    for ax, ay, az, am in anchors:
        anchor_r = pitch_radius(az, am)
        cd = drag_r + anchor_r
        snap_radius = cd * snap_radius_frac

        dx = dx0 - ax
        dy = dy0 - ay
        dist = math.sqrt(dx * dx + dy * dy)

        if dist < snap_radius and dist < best_dist:
            best_dist = dist
            if dist > 0.0:
                nx, ny = dx / dist, dy / dist
            else:
                nx, ny = 1.0, 0.0
            best_pos = (ax + nx * cd, ay + ny * cd)

    return best_pos
