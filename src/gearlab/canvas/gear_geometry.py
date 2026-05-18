"""
Involute spur gear tooth profile geometry.

Uses the standard 20-degree pressure angle.  No Qt widget dependencies —
only QPainterPath is imported for the path output.
"""
import math
from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainterPath

if TYPE_CHECKING:
    from gearlab.models import DefectType

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PRESSURE_ANGLE_DEG: float = 20.0
_ALPHA: float = math.radians(PRESSURE_ANGLE_DEG)
_FLANK_POINTS: int = 8      # involute sample points per tooth flank
_TIP_SEGS: int = 2          # extra points across the flat tip
_CHIP_TIP_FRAC: float = 0.30  # chipped tooth addendum fraction of normal


# ---------------------------------------------------------------------------
# Radius helpers
# ---------------------------------------------------------------------------

def pitch_radius(tooth_count: int, module: float) -> float:
    """Pitch circle radius: r_p = m·z / 2."""
    return tooth_count * module / 2.0


def addendum_radius(tooth_count: int, module: float) -> float:
    """Outer (addendum) circle radius: r_a = r_p + m."""
    return pitch_radius(tooth_count, module) + module


def dedendum_radius(tooth_count: int, module: float) -> float:
    """Root (dedendum) circle radius, clamped to a sensible minimum."""
    return max(pitch_radius(tooth_count, module) - 1.25 * module, module * 0.4)


# ---------------------------------------------------------------------------
# Internal geometry helpers
# ---------------------------------------------------------------------------

def _inv(t: float) -> float:
    """Involute function: inv(t) = t − atan(t)."""
    return t - math.atan(t)


def _t_at_radius(r: float, r_b: float) -> float:
    """Involute parameter at radius r (returns 0 when r ≤ r_b)."""
    if r <= r_b:
        return 0.0
    return math.sqrt((r / r_b) ** 2 - 1.0)


# ---------------------------------------------------------------------------
# Public path builder
# ---------------------------------------------------------------------------

def spur_gear_path(
    tooth_count: int,
    module: float,
    rotation_offset: float = 0.0,
    defect_map: "dict[int, DefectType] | None" = None,
) -> QPainterPath:
    """
    Return a QPainterPath for a spur gear centered at origin.

    Parameters
    ----------
    tooth_count     : number of teeth
    module          : gear module (determines physical scale)
    rotation_offset : angular offset in radians (CCW positive)
    defect_map      : optional {tooth_index: DefectType} for defect visuals

    The path uses the even-odd fill rule so the hub bore renders
    as a transparent hole when drawn with a solid brush.
    """
    # Import here to avoid a hard dependency at module import time
    from gearlab.models import DefectType as _DT  # noqa: PLC0415

    z = tooth_count
    m = module

    r_p = pitch_radius(z, m)
    r_a = addendum_radius(z, m)
    r_d = dedendum_radius(z, m)
    r_b = r_p * math.cos(_ALPHA)          # base circle radius
    hub_r = max(r_d * 0.22, 5.0)

    # Involute parameters at key radii
    t_root = _t_at_radius(r_d, r_b)
    t_tip  = _t_at_radius(r_a, r_b)

    # inv(α) at pitch circle, for tooth centering
    t_p = math.tan(_ALPHA)
    inv_alpha = _inv(t_p)

    half_tooth  = math.pi / (2.0 * z)
    pitch_angle = 2.0 * math.pi / z

    dm = defect_map or {}

    def _right_angle(t: float, center: float) -> float:
        return center + half_tooth - inv_alpha + _inv(t)

    def _left_angle(t: float, center: float) -> float:
        return center - half_tooth + inv_alpha - _inv(t)

    def _flank(t_lo: float, t_hi: float, angle_fn, reverse=False):
        """Generate _FLANK_POINTS along an involute flank."""
        result = []
        for k in range(_FLANK_POINTS):
            frac = k / (_FLANK_POINTS - 1)
            t = t_lo + (t_hi - t_lo) * frac
            r = max(r_d, min(r_a, r_b * math.sqrt(1.0 + t * t)))
            result.append((r * math.cos(angle_fn(t)), r * math.sin(angle_fn(t))))
        return result if not reverse else result[::-1]

    pts: list[tuple[float, float]] = []

    for i in range(z):
        tooth_center = rotation_offset + i * pitch_angle
        defect = dm.get(i)

        if defect is _DT.MISSING:
            # ---- Missing tooth: concave gap replacing the tooth ----------
            a_L = _right_angle(t_root, tooth_center)   # where right flank would start
            a_R = _left_angle(t_root, tooth_center)    # where left flank would end
            gap_r = max(r_d * 0.78, hub_r + 2.0)      # dips below root
            pts.append((r_d * math.cos(a_L),          r_d * math.sin(a_L)))
            pts.append((gap_r * math.cos(tooth_center), gap_r * math.sin(tooth_center)))
            pts.append((r_d * math.cos(a_R),          r_d * math.sin(a_R)))

        elif defect is _DT.CHIPPED:
            # ---- Chipped tooth: very short addendum + jagged tip ---------
            t_chip = max(t_root + 1e-4, t_tip * _CHIP_TIP_FRAC)
            r_chip = r_b * math.sqrt(1.0 + t_chip * t_chip)

            right_fn = lambda t, c=tooth_center: _right_angle(t, c)  # noqa: E731
            left_fn  = lambda t, c=tooth_center: _left_angle(t, c)   # noqa: E731

            # right flank root → chip tip
            for k in range(_FLANK_POINTS):
                frac = k / (_FLANK_POINTS - 1)
                t = t_root + (t_chip - t_root) * frac
                r = max(r_d, min(r_a, r_b * math.sqrt(1.0 + t * t)))
                a = right_fn(t)
                pts.append((r * math.cos(a), r * math.sin(a)))
            # Jagged chipped tip
            a_rt = right_fn(t_chip)
            a_lt = left_fn(t_chip)
            a_mid = (a_rt + a_lt) / 2.0
            pts.append((r_chip * math.cos(a_rt),          r_chip * math.sin(a_rt)))
            pts.append(((r_chip - m * 0.5) * math.cos(a_mid),
                        (r_chip - m * 0.5) * math.sin(a_mid)))   # dip at chip
            pts.append((r_chip * math.cos(a_lt),          r_chip * math.sin(a_lt)))
            # left flank chip tip → root
            for k in range(_FLANK_POINTS):
                frac = k / (_FLANK_POINTS - 1)
                t = t_chip - (t_chip - t_root) * frac
                r = max(r_d, min(r_a, r_b * math.sqrt(1.0 + t * t)))
                a = left_fn(t)
                pts.append((r * math.cos(a), r * math.sin(a)))

        else:
            # ---- Normal tooth --------------------------------------------
            # right flank
            for k in range(_FLANK_POINTS):
                frac = k / (_FLANK_POINTS - 1)
                t = t_root + (t_tip - t_root) * frac
                r = max(r_d, min(r_a, r_b * math.sqrt(1.0 + t * t)))
                a = _right_angle(t, tooth_center)
                pts.append((r * math.cos(a), r * math.sin(a)))
            # tip flat
            a_rt = _right_angle(t_tip, tooth_center)
            a_lt = _left_angle(t_tip, tooth_center)
            for k in range(1, _TIP_SEGS + 1):
                frac = k / (_TIP_SEGS + 1)
                a = a_rt + (a_lt - a_rt) * frac
                pts.append((r_a * math.cos(a), r_a * math.sin(a)))
            # left flank
            for k in range(_FLANK_POINTS):
                frac = k / (_FLANK_POINTS - 1)
                t = t_tip - (t_tip - t_root) * frac
                r = max(r_d, min(r_a, r_b * math.sqrt(1.0 + t * t)))
                a = _left_angle(t, tooth_center)
                pts.append((r * math.cos(a), r * math.sin(a)))

        # ---- Root arc between this tooth and the next -------------------
        a_lr   = _left_angle(t_root, tooth_center)
        a_rr_n = _right_angle(t_root, rotation_offset + (i + 1) * pitch_angle)
        a_mid  = (a_lr + a_rr_n) / 2.0
        pts.append((r_d * math.cos(a_mid), r_d * math.sin(a_mid)))

    if not pts:
        return QPainterPath()

    path = QPainterPath()
    path.moveTo(pts[0][0], pts[0][1])
    for x, y in pts[1:]:
        path.lineTo(x, y)
    path.closeSubpath()

    # Hub bore — even-odd fill rule makes it a transparent hole
    path.setFillRule(Qt.FillRule.OddEvenFill)
    path.addEllipse(-hub_r, -hub_r, hub_r * 2.0, hub_r * 2.0)

    return path
