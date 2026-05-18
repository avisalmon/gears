"""
Canvas gear rendering — E03-S1.

GearItem   : QGraphicsItem subclass with involute tooth profile.
add_gear_to_scene : convenience wrapper (used by app.py).
add_ratio_badge   : floating annotation between two gears.
"""
from __future__ import annotations

from PyQt6.QtCore import QPointF, QRectF, Qt, QTimer
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsScene,
    QGraphicsTextItem,
)

from gearlab.canvas.gear_geometry import (
    addendum_radius,
    spur_gear_path,
)
from gearlab.models import Direction, Gear

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------

_CW_COLOR      = QColor("#2d7fc1")   # blue  — clockwise
_CCW_COLOR     = QColor("#c14040")   # red   — counter-clockwise
_UNK_COLOR     = QColor("#1e5f9e")   # default (direction unknown)
_BORDER        = QColor("#7ab0d4")
_DRIVER_BORDER = QColor("#f0c94a")
_LABEL         = QColor("#c8dde8")
_ACCENT        = QColor("#f0c94a")
_MUTED         = QColor("#607890")


# ---------------------------------------------------------------------------
# GearItem — E03-S1-02
# ---------------------------------------------------------------------------

class GearItem(QGraphicsItem):
    """
    A single spur gear rendered as a QGraphicsItem.

    Position is set from gear.position at construction.
    Rotation is driven by AnimationController via set_angle().
    Direction colour is updated via set_direction().
    """

    def __init__(
        self,
        gear: Gear,
        parent: QGraphicsItem | None = None,
    ) -> None:
        super().__init__(parent)
        self._gear          = gear
        self._color         = _UNK_COLOR
        self._flashing      = False
        self._snap_callback = None   # set by app for snap-to-mesh
        self._rebuild_path()
        self.setPos(gear.position[0], gear.position[1])
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def _rebuild_path(self) -> None:
        """Compute the gear path, applying any defects from gear.defects."""
        defect_map = (
            {d.tooth_index: d.defect_type for d in self._gear.defects}
            if self._gear.defects else None
        )
        self._path = spur_gear_path(
            self._gear.tooth_count, self._gear.module, defect_map=defect_map
        )

    def set_angle(self, degrees: float) -> None:
        """Set absolute rotation in degrees (positive = CW in Qt coords)."""
        self.setRotation(degrees)

    def set_direction(self, direction: Direction | None) -> None:
        """Update fill colour to reflect rotation direction (E03-S1-07)."""
        if direction == Direction.CW:
            self._color = _CW_COLOR
        elif direction == Direction.CCW:
            self._color = _CCW_COLOR
        else:
            self._color = _UNK_COLOR
        self.update()

    def flash(self, duration_ms: int = 250) -> None:
        """Brief bright flash to signal a defect engagement event (E04-S2-05)."""
        self._flashing = True
        self.update()
        QTimer.singleShot(duration_ms, self._end_flash)

    def _end_flash(self) -> None:
        self._flashing = False
        self.update()

    # ------------------------------------------------------------------
    # QGraphicsItem interface
    # ------------------------------------------------------------------

    def mouseReleaseEvent(self, event) -> None:  # type: ignore[override]
        super().mouseReleaseEvent(event)
        if callable(self._snap_callback):
            self._snap_callback(self)

    def boundingRect(self) -> QRectF:
        r_a  = addendum_radius(self._gear.tooth_count, self._gear.module)
        side = r_a + max(self._gear.module, 10.0)   # room for highlight ring
        return QRectF(-side, -side, side * 2.0, side * 2.0)

    def paint(
        self,
        painter: QPainter,
        option,          # QStyleOptionGraphicsItem — unused
        widget=None,
    ) -> None:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        fill   = QColor("#ffe040") if self._flashing else self._color
        border = _DRIVER_BORDER if self._gear.is_driver else _BORDER
        painter.setBrush(QBrush(fill))
        painter.setPen(QPen(border, 1.5))
        painter.drawPath(self._path)

        # Selection highlight ring (E03-S2-03)
        if self.isSelected():
            r_a = addendum_radius(self._gear.tooth_count, self._gear.module)
            ring_r = r_a + 6.0
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QColor("#ffffff"), 2.5, Qt.PenStyle.DashLine))
            painter.drawEllipse(QPointF(0.0, 0.0), ring_r, ring_r)

        # Label centred below the gear (local coords: gear centred at 0,0)
        r_a    = addendum_radius(self._gear.tooth_count, self._gear.module)
        sym    = "◆" if self._gear.is_driver else "◇"
        label  = f"{sym}  {self._gear.tooth_count}T  {self._gear.rpm:.0f} RPM"
        color  = _ACCENT if self._gear.is_driver else _LABEL
        weight = QFont.Weight.Bold if self._gear.is_driver else QFont.Weight.Normal
        painter.setPen(QPen(color))
        painter.setFont(QFont("Segoe UI", 9, weight))
        fm = painter.fontMetrics()
        tw = fm.horizontalAdvance(label)
        painter.drawText(int(-tw / 2), int(r_a + 18), label)


# ---------------------------------------------------------------------------
# Convenience helpers (used by app.py)
# ---------------------------------------------------------------------------

def add_gear_to_scene(
    scene: QGraphicsScene,
    gear: Gear,
    rotation_offset: float = 0.0,
    direction: Direction | None = None,
) -> GearItem:
    """Create a GearItem, add it to *scene*, and return it."""
    item = GearItem(gear)
    item.set_direction(direction)
    import math as _math
    item.set_angle(rotation_offset * 180.0 / _math.pi)
    scene.addItem(item)
    return item


def add_ratio_badge(
    scene: QGraphicsScene,
    x: float,
    y: float,
    label: str,
) -> QGraphicsTextItem:
    """Floating ratio annotation — yellow text at (x, y) in scene coords."""
    text = QGraphicsTextItem(label)
    text.setDefaultTextColor(_ACCENT)
    text.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
    br = text.boundingRect()
    text.setPos(x - br.width() / 2, y - br.height() / 2)
    scene.addItem(text)
    return text
