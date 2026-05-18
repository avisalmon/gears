"""
Properties Panel — E05-S2.

A QDockWidget that shows and edits properties of the selected gear.
Signals are emitted when the user changes a value; the app applies them.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QDockWidget,
    QDoubleSpinBox,
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from gearlab.models import Direction


class PropertiesPanel(QDockWidget):
    """Right-side dock showing and editing properties of the selected gear."""

    tooth_count_changed = pyqtSignal(int)
    module_changed      = pyqtSignal(float)
    driver_toggled      = pyqtSignal(bool)
    driver_rpm_changed  = pyqtSignal(float)
    defect_toggled      = pyqtSignal(int, bool)   # (tooth_index, is_defective)

    def __init__(self, parent=None) -> None:
        super().__init__("Properties", parent)
        self.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)
        self.setFeatures(
            QDockWidget.DockWidgetFeature.DockWidgetMovable
            | QDockWidget.DockWidgetFeature.DockWidgetFloatable
        )
        self.setMinimumWidth(200)

        self._engineer_mode: bool = False
        self._building: bool = False    # suppress signals while populating
        self._defect_buttons: list[QPushButton] = []

        self._build_ui()
        self.clear()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        container = QWidget()
        self.setWidget(container)
        outer = QVBoxLayout(container)
        outer.setContentsMargins(8, 8, 8, 8)
        outer.setSpacing(6)

        # ── No-selection placeholder ────────────────────────────────────
        self._no_sel_label = QLabel("No gear selected")
        self._no_sel_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._no_sel_label.setStyleSheet("color: #888; font-style: italic;")
        outer.addWidget(self._no_sel_label)

        # ── Properties form ─────────────────────────────────────────────
        self._form_widget = QWidget()
        form = QFormLayout(self._form_widget)
        form.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Tooth count spinbox
        self._teeth_spin = QSpinBox()
        self._teeth_spin.setRange(8, 100)
        self._teeth_spin.valueChanged.connect(self._on_teeth_spin_changed)
        form.addRow("Teeth:", self._teeth_spin)

        # Tooth count slider (same row below)
        self._teeth_slider = QSlider(Qt.Orientation.Horizontal)
        self._teeth_slider.setRange(8, 100)
        self._teeth_slider.valueChanged.connect(self._on_teeth_slider_changed)
        form.addRow("", self._teeth_slider)

        # Module (Engineer-only)
        self._module_label = QLabel("Module:")
        self._module_spin = QDoubleSpinBox()
        self._module_spin.setRange(1.0, 25.0)
        self._module_spin.setSingleStep(0.5)
        self._module_spin.valueChanged.connect(self._on_module_changed)
        form.addRow(self._module_label, self._module_spin)

        # RPM (read-only)
        self._rpm_label = QLabel("—")
        form.addRow("RPM:", self._rpm_label)

        # Ratio (read-only)
        self._ratio_label = QLabel("—")
        form.addRow("Ratio:", self._ratio_label)

        # Direction
        self._dir_label = QLabel("—")
        form.addRow("Direction:", self._dir_label)

        # Is-driver checkbox
        self._driver_check = QCheckBox("Set as driver gear")
        self._driver_check.toggled.connect(self._on_driver_toggled)
        form.addRow("", self._driver_check)

        # Driver RPM input (only visible when is_driver)
        self._driver_rpm_label = QLabel("Driver RPM:")
        self._driver_rpm_spin = QDoubleSpinBox()
        self._driver_rpm_spin.setRange(1.0, 10000.0)
        self._driver_rpm_spin.setValue(100.0)
        self._driver_rpm_spin.valueChanged.connect(self._on_driver_rpm_changed)
        form.addRow(self._driver_rpm_label, self._driver_rpm_spin)

        outer.addWidget(self._form_widget)

        # ── Defect grid (Engineer-only) ──────────────────────────────────
        self._defect_label = QLabel("Tooth Defects — click to toggle missing:")
        self._defect_label.setWordWrap(True)
        self._defect_label.setStyleSheet("color: #aaa; font-size: 11px;")
        outer.addWidget(self._defect_label)

        self._defect_grid_widget = QWidget()
        self._defect_grid = QGridLayout(self._defect_grid_widget)
        self._defect_grid.setSpacing(3)
        outer.addWidget(self._defect_grid_widget)

        outer.addStretch()

    # ------------------------------------------------------------------
    # Slot helpers
    # ------------------------------------------------------------------

    def _on_teeth_spin_changed(self, v: int) -> None:
        if self._building:
            return
        self._building = True
        self._teeth_slider.setValue(v)
        self._building = False
        self.tooth_count_changed.emit(v)

    def _on_teeth_slider_changed(self, v: int) -> None:
        if self._building:
            return
        self._building = True
        self._teeth_spin.setValue(v)
        self._building = False
        self.tooth_count_changed.emit(v)

    def _on_module_changed(self, v: float) -> None:
        if not self._building:
            self.module_changed.emit(v)

    def _on_driver_toggled(self, checked: bool) -> None:
        if self._building:
            return
        self._driver_rpm_label.setVisible(checked)
        self._driver_rpm_spin.setVisible(checked)
        self.driver_toggled.emit(checked)

    def _on_driver_rpm_changed(self, v: float) -> None:
        if not self._building:
            self.driver_rpm_changed.emit(v)

    # ------------------------------------------------------------------
    # Defect grid builder
    # ------------------------------------------------------------------

    def _rebuild_defect_grid(self, tooth_count: int, defective: set[int]) -> None:
        for btn in self._defect_buttons:
            self._defect_grid.removeWidget(btn)
            btn.deleteLater()
        self._defect_buttons.clear()

        cols = 5
        for i in range(tooth_count):
            btn = QPushButton(str(i))
            btn.setFixedSize(34, 28)
            btn.setCheckable(True)
            btn.setChecked(i in defective)
            btn.setStyleSheet(
                "QPushButton { font-size: 10px; }"
                "QPushButton:checked { background-color: #cc3333; color: #fff; }"
            )
            idx = i
            btn.toggled.connect(
                lambda checked, t=idx: self.defect_toggled.emit(t, checked)
            )
            self._defect_grid.addWidget(btn, i // cols, i % cols)
            self._defect_buttons.append(btn)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def populate(self, gear, ratio: float | None = None) -> None:
        """Fill the panel from a Gear instance (post-solve state)."""
        from gearlab.models import DefectType

        self._building = True

        self._no_sel_label.setVisible(False)
        self._form_widget.setVisible(True)

        # Teeth
        self._teeth_spin.setValue(gear.tooth_count)
        self._teeth_slider.setValue(gear.tooth_count)

        # Module (Engineer-only visibility)
        self._module_label.setVisible(self._engineer_mode)
        self._module_spin.setVisible(self._engineer_mode)
        self._module_spin.setValue(float(gear.module))

        # RPM
        rpm = getattr(gear, "rpm", 0.0) or 0.0
        self._rpm_label.setText(f"{rpm:.1f} RPM")

        # Ratio
        if ratio is not None:
            self._ratio_label.setText(f"{ratio:.2f} : 1")
        else:
            self._ratio_label.setText("—")

        # Direction
        direction = getattr(gear, "_direction", None)
        if direction == Direction.CW:
            self._dir_label.setText("↻  Clockwise")
        elif direction == Direction.CCW:
            self._dir_label.setText("↺  Counter-clockwise")
        else:
            self._dir_label.setText("—")

        # Driver
        self._driver_check.setChecked(gear.is_driver)
        self._driver_rpm_label.setVisible(gear.is_driver)
        self._driver_rpm_spin.setVisible(gear.is_driver)
        if gear.is_driver and gear.rpm:
            self._driver_rpm_spin.setValue(float(gear.rpm))

        # Defects (Engineer-only)
        self._defect_label.setVisible(self._engineer_mode)
        self._defect_grid_widget.setVisible(self._engineer_mode)
        if self._engineer_mode:
            defective = {
                d.tooth_index for d in getattr(gear, "defects", [])
                if d.defect_type == DefectType.MISSING
            }
            self._rebuild_defect_grid(gear.tooth_count, defective)

        self._building = False

    def clear(self) -> None:
        """Show the no-selection placeholder; hide the form."""
        self._no_sel_label.setVisible(True)
        self._form_widget.setVisible(False)
        self._defect_label.setVisible(False)
        self._defect_grid_widget.setVisible(False)

    def set_engineer_mode(self, is_engineer: bool) -> None:
        """Show/hide engineer-only fields. Call before or after populate()."""
        self._engineer_mode = is_engineer
        if self._form_widget.isVisible():
            self._module_label.setVisible(is_engineer)
            self._module_spin.setVisible(is_engineer)
            self._defect_label.setVisible(is_engineer)
            self._defect_grid_widget.setVisible(is_engineer)
