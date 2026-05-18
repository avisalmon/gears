"""
GearView — E05-S2.

QGraphicsView subclass that adds scroll-to-zoom and emits zoom_changed.
"""
from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QGraphicsView


class GearView(QGraphicsView):
    """Canvas view with scroll-to-zoom and a zoom_changed signal."""

    zoom_changed = pyqtSignal(float)   # current scale factor (1.0 = 100%)

    _ZOOM_FACTOR = 1.15
    _MIN_ZOOM    = 0.05
    _MAX_ZOOM    = 20.0

    def wheelEvent(self, event) -> None:  # type: ignore[override]
        current = self.transform().m11()
        factor = self._ZOOM_FACTOR if event.angleDelta().y() > 0 else 1.0 / self._ZOOM_FACTOR
        new_zoom = current * factor
        if self._MIN_ZOOM <= new_zoom <= self._MAX_ZOOM:
            self.scale(factor, factor)
            self.zoom_changed.emit(self.transform().m11())
        event.accept()
