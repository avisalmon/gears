"""
FormulaPanel — E06-S1 educational overlay dock widget.
Shows gear ratio formula, direction rule, and (Engineer mode) expert data table.
"""
from __future__ import annotations

import math

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDockWidget,
    QHeaderView,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class FormulaPanel(QDockWidget):
    """Dockable educational panel: formula + direction rule + expert table."""

    def __init__(self, parent=None) -> None:
        super().__init__("Formula", parent)
        self.setAllowedAreas(
            Qt.DockWidgetArea.BottomDockWidgetArea
            | Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self.setMinimumWidth(220)
        self.setMaximumHeight(260)

        self._mode = "student"   # "student" | "engineer" | "explorer"

        # ----- inner widget -------------------------------------------------
        inner = QWidget()
        inner.setStyleSheet(
            "QWidget { background:#1e2030; }"
            "QLabel  { color:#cdd6f4; }"
        )
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # formula text label
        self._formula_label = QLabel()
        self._formula_label.setWordWrap(True)
        self._formula_label.setTextFormat(Qt.TextFormat.PlainText)
        self._formula_label.setStyleSheet(
            "color:#cdd6f4; font-size:13px; font-weight:600;"
        )
        self._formula_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        layout.addWidget(self._formula_label)

        # direction rule label
        self._dir_label = QLabel(
            "\u21bb Driver \u2192 \u21ba Driven  |  External mesh reverses direction."
        )
        self._dir_label.setWordWrap(True)
        self._dir_label.setStyleSheet("color:#a6e3a1; font-size:12px;")
        layout.addWidget(self._dir_label)

        # expert table (Engineer mode only) ---------------------------------
        self._expert_table = QTableWidget(0, 6)
        self._expert_table.setHorizontalHeaderLabels(
            ["Gear", "Teeth", "Module", "Ratio", "RPM", "Vel (m/s)"]
        )
        self._expert_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self._expert_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._expert_table.setAlternatingRowColors(True)
        self._expert_table.setStyleSheet(
            "QTableWidget { font-size:10px; color:#cdd6f4; "
            "background:#1e2030; alternate-background-color:#24273a; "
            "gridline-color:#45475a; }"
            "QHeaderView::section { background:#313244; color:#cdd6f4; "
            "font-size:10px; border:none; }"
        )
        self._expert_table.setVisible(False)
        scroll = QScrollArea()
        scroll.setWidget(self._expert_table)
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(130)
        self._expert_table_scroll = scroll
        layout.addWidget(scroll)

        inner.setLayout(layout)
        self.setWidget(inner)

        self.clear()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def set_mode(self, mode) -> None:
        """
        Accept AppMode enum or plain string.
        Shows expert table only in Engineer mode.
        """
        from gearlab.ui.mode import AppMode
        if isinstance(mode, AppMode):
            mode_str = mode.value.lower()
        else:
            mode_str = str(mode).lower()
        self._mode = mode_str
        is_engineer = "engineer" in mode_str
        self._expert_table.setVisible(is_engineer)
        self._expert_table_scroll.setVisible(is_engineer)

    def update_for_system(self, system) -> None:
        """Refresh formula text and (Engineer) expert table from a solved system."""
        if system is None or not system.elements:
            self.clear()
            return

        driver = next((g for g in system.elements if g.is_driver), None)
        if driver is None:
            self.clear()
            return

        # Build formula text --------------------------------------------------
        lines: list[str] = []

        # Find first non-driver gear connected to driver
        driven = None
        if system.connections:
            conn = system.connections[0]
            other_id = (conn.element_b if conn.element_a == driver.id
                        else conn.element_a)
            driven = next((g for g in system.elements if g.id == other_id), None)

        if driven is not None:
            ratio = driven.tooth_count / driver.tooth_count
            lines.append(
                f"Gear Ratio = N\u2082 \u00f7 N\u2081 "
                f"= {driven.tooth_count} \u00f7 {driver.tooth_count} "
                f"= {ratio:.2f}"
            )
            out_rpm = getattr(driven, "rpm", None)
            if out_rpm is not None:
                lines.append(
                    f"Output RPM = {driver.rpm:.0f} \u00f7 {ratio:.2f} "
                    f"= {out_rpm:.1f} RPM"
                )
        else:
            lines.append(
                f"Driver: {driver.tooth_count} teeth  |  {driver.rpm:.0f} RPM"
            )

        self._formula_label.setText("\n".join(lines))

        # Expert table --------------------------------------------------------
        if "engineer" in self._mode:
            self._rebuild_expert_table(system, driver)

    def clear(self) -> None:
        """Reset panel to empty/placeholder state."""
        self._formula_label.setText("No gears connected.")
        self._expert_table.setRowCount(0)

    def get_text(self) -> str:
        """Return all visible text content for testing."""
        parts = [
            self._formula_label.text(),
            self._dir_label.text(),
        ]
        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _rebuild_expert_table(self, system, driver) -> None:
        gears = system.elements
        self._expert_table.setRowCount(len(gears))
        for row, g in enumerate(gears):
            ratio = (g.tooth_count / driver.tooth_count
                     if not g.is_driver else 1.0)
            rpm = getattr(g, "rpm", 0.0) or 0.0
            # tangential velocity = pi * module * teeth * rpm / 60  (mm/s → m/s)
            vel_ms = (math.pi * g.module * g.tooth_count * rpm / 60) / 1000.0
            label = "Driver" if g.is_driver else f"Gear {row + 1}"
            self._expert_table.setItem(row, 0, QTableWidgetItem(label))
            self._expert_table.setItem(row, 1, QTableWidgetItem(str(g.tooth_count)))
            self._expert_table.setItem(row, 2, QTableWidgetItem(f"{g.module:.1f}"))
            self._expert_table.setItem(row, 3, QTableWidgetItem(f"{ratio:.3f}"))
            self._expert_table.setItem(row, 4, QTableWidgetItem(f"{rpm:.1f}"))
            self._expert_table.setItem(row, 5, QTableWidgetItem(f"{vel_ms:.3f}"))
