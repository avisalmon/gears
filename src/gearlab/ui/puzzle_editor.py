"""
PuzzleEditorDialog — E07-S2.

A dialog that lets a teacher author, test-play, and save a custom puzzle.
"""
from __future__ import annotations

import uuid
from typing import Optional

from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gearlab.models import (
    Direction,
    Gear,
    GearSystem,
    GearType,
    GoalSpec,
    PuzzleDifficulty,
    PuzzleFile,
)
from gearlab.puzzle.loader import save_puzzle

_M = 8          # default module for template gears
_RPM = 100.0    # default driver RPM


class PuzzleEditorDialog(QDialog):
    """
    Dialog for authoring a GearLab puzzle.

    Usage::

        dlg = PuzzleEditorDialog()
        dlg.new_puzzle()          # or dlg.load_puzzle_file(pf)
        dlg.set_title("My puzzle")
        dlg.set_target_ratio(2.0)
        pf = dlg.build_puzzle_file()
        dlg.save_to_path("/path/puzzle.gearlab")
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Puzzle Editor")
        self.setMinimumWidth(460)
        self._gears: list[Gear] = []
        self._locked_ids: list[uuid.UUID] = []
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setSpacing(10)

        # ---- Metadata ----
        meta_box = QGroupBox("Puzzle Info")
        meta_box.setStyleSheet("QGroupBox { font-weight:600; }")
        form = QFormLayout(meta_box)

        self._title_edit = QLineEdit()
        self._title_edit.setPlaceholderText("Required")
        form.addRow("Title:", self._title_edit)

        self._desc_edit = QTextEdit()
        self._desc_edit.setPlaceholderText("Describe what the player must achieve.")
        self._desc_edit.setMaximumHeight(60)
        form.addRow("Description:", self._desc_edit)

        self._diff_combo = QComboBox()
        self._diff_combo.addItems(["easy", "medium", "hard"])
        form.addRow("Difficulty:", self._diff_combo)

        root.addWidget(meta_box)

        # ---- Goal ----
        goal_box = QGroupBox("Goal Constraints")
        goal_box.setStyleSheet("QGroupBox { font-weight:600; }")
        gfl = QFormLayout(goal_box)

        # target ratio
        ratio_row = QWidget()
        rl = QHBoxLayout(ratio_row)
        rl.setContentsMargins(0, 0, 0, 0)
        self._ratio_check = QCheckBox()
        self._ratio_spin = QDoubleSpinBox()
        self._ratio_spin.setRange(0.1, 50.0)
        self._ratio_spin.setSingleStep(0.5)
        self._ratio_spin.setValue(2.0)
        self._ratio_spin.setEnabled(False)
        self._ratio_check.toggled.connect(self._ratio_spin.setEnabled)
        rl.addWidget(self._ratio_check)
        rl.addWidget(self._ratio_spin)
        gfl.addRow("Target ratio:", ratio_row)

        # direction
        dir_row = QWidget()
        dl = QHBoxLayout(dir_row)
        dl.setContentsMargins(0, 0, 0, 0)
        self._dir_check = QCheckBox()
        self._dir_combo = QComboBox()
        self._dir_combo.addItems(["CW", "CCW"])
        self._dir_combo.setEnabled(False)
        self._dir_check.toggled.connect(self._dir_combo.setEnabled)
        dl.addWidget(self._dir_check)
        dl.addWidget(self._dir_combo)
        gfl.addRow("Output direction:", dir_row)

        # max gears
        max_row = QWidget()
        ml = QHBoxLayout(max_row)
        ml.setContentsMargins(0, 0, 0, 0)
        self._max_check = QCheckBox()
        self._max_spin = QSpinBox()
        self._max_spin.setRange(2, 10)
        self._max_spin.setValue(3)
        self._max_spin.setEnabled(False)
        self._max_check.toggled.connect(self._max_spin.setEnabled)
        ml.addWidget(self._max_check)
        ml.addWidget(self._max_spin)
        gfl.addRow("Max gears:", max_row)

        root.addWidget(goal_box)

        # ---- Hints ----
        hint_box = QGroupBox("Hints (1 → 2 → 3)")
        hint_box.setStyleSheet("QGroupBox { font-weight:600; }")
        hfl = QFormLayout(hint_box)
        self._hint_edits: list[QLineEdit] = []
        for i in range(3):
            le = QLineEdit()
            le.setPlaceholderText(f"Optional hint {i + 1}")
            self._hint_edits.append(le)
            hfl.addRow(f"Hint {i + 1}:", le)
        root.addWidget(hint_box)

        # ---- Gear list / lock toggles ----
        self._lock_box = QGroupBox("Locked Elements")
        self._lock_box.setStyleSheet("QGroupBox { font-weight:600; }")
        self._lock_layout = QVBoxLayout(self._lock_box)
        self._lock_checkboxes: dict[str, QCheckBox] = {}
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMaximumHeight(100)
        inner = QWidget()
        self._lock_inner_layout = QVBoxLayout(inner)
        scroll.setWidget(inner)
        self._lock_layout.addWidget(scroll)
        root.addWidget(self._lock_box)

        # ---- Buttons ----
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        btn_box.accepted.connect(self.accept)
        btn_box.rejected.connect(self.reject)
        root.addWidget(btn_box)

    # ------------------------------------------------------------------
    # Public API — metadata
    # ------------------------------------------------------------------

    def get_title(self) -> str:
        return self._title_edit.text().strip()

    def set_title(self, text: str) -> None:
        self._title_edit.setText(text)

    def get_description(self) -> str:
        return self._desc_edit.toPlainText().strip()

    def set_description(self, text: str) -> None:
        self._desc_edit.setPlainText(text)

    def get_difficulty(self) -> str:
        return self._diff_combo.currentText()

    def set_difficulty(self, d: str) -> None:
        idx = self._diff_combo.findText(d)
        if idx >= 0:
            self._diff_combo.setCurrentIndex(idx)

    # ------------------------------------------------------------------
    # Public API — goal
    # ------------------------------------------------------------------

    def get_target_ratio(self) -> Optional[float]:
        return self._ratio_spin.value() if self._ratio_check.isChecked() else None

    def set_target_ratio(self, v: Optional[float]) -> None:
        if v is None:
            self._ratio_check.setChecked(False)
        else:
            self._ratio_check.setChecked(True)
            self._ratio_spin.setValue(v)

    def get_target_direction(self) -> Optional[Direction]:
        if not self._dir_check.isChecked():
            return None
        return Direction(self._dir_combo.currentText())

    def set_target_direction(self, d: Optional[Direction]) -> None:
        if d is None:
            self._dir_check.setChecked(False)
        else:
            self._dir_check.setChecked(True)
            idx = self._dir_combo.findText(d.value)
            if idx >= 0:
                self._dir_combo.setCurrentIndex(idx)

    def get_max_gears(self) -> Optional[int]:
        return self._max_spin.value() if self._max_check.isChecked() else None

    def set_max_gears(self, v: Optional[int]) -> None:
        if v is None:
            self._max_check.setChecked(False)
        else:
            self._max_check.setChecked(True)
            self._max_spin.setValue(v)

    # ------------------------------------------------------------------
    # Public API — hints
    # ------------------------------------------------------------------

    def get_hints(self) -> list[str]:
        return [le.text() for le in self._hint_edits]

    def set_hints(self, hints: list[str]) -> None:
        padded = (list(hints) + ["", "", ""])[:3]
        for le, h in zip(self._hint_edits, padded):
            le.setText(h)

    # ------------------------------------------------------------------
    # Public API — gear list / locks
    # ------------------------------------------------------------------

    def get_gear_list(self) -> list[Gear]:
        return list(self._gears)

    def get_locked_ids(self) -> list[uuid.UUID]:
        return list(self._locked_ids)

    def set_gear_locked(self, gear_id, locked: bool) -> None:
        gid = gear_id if isinstance(gear_id, uuid.UUID) else uuid.UUID(str(gear_id))
        if locked:
            if gid not in self._locked_ids:
                self._locked_ids.append(gid)
        else:
            self._locked_ids = [i for i in self._locked_ids if i != gid]
        cb = self._lock_checkboxes.get(gid)
        if cb is not None:
            cb.setChecked(locked)

    # ------------------------------------------------------------------
    # Public API — template / load
    # ------------------------------------------------------------------

    def new_puzzle(self) -> None:
        """Pre-fill with a 2-gear starter template."""
        g1 = Gear(
            id=uuid.uuid4(),
            gear_type=GearType.SPUR,
            tooth_count=20,
            module=_M,
            position=(0.0, 0.0),
            is_driver=True,
            rpm=_RPM,
        )
        g2 = Gear(
            id=uuid.uuid4(),
            gear_type=GearType.SPUR,
            tooth_count=20,
            module=_M,
            position=(320.0, 0.0),
            is_driver=False,
            rpm=0.0,
        )
        self._gears = [g1, g2]
        self._locked_ids = []
        self._rebuild_lock_ui()

    def load_puzzle_file(self, pf: PuzzleFile) -> None:
        """Populate all fields from an existing PuzzleFile (duplicate/edit)."""
        self.set_title(pf.title)
        self.set_description(pf.description or "")
        diff_val = pf.difficulty.value if isinstance(pf.difficulty, PuzzleDifficulty) else str(pf.difficulty)
        self.set_difficulty(diff_val)
        self.set_target_ratio(pf.goal.target_ratio)
        self.set_target_direction(pf.goal.target_direction)
        self.set_max_gears(pf.goal.max_gears)
        padded = (list(pf.hints) + ["", "", ""])[:3]
        self.set_hints(padded)
        self._gears = list(pf.initial_state.elements)
        # Normalise to uuid.UUID objects
        self._locked_ids = [
            i if isinstance(i, uuid.UUID) else uuid.UUID(str(i))
            for i in pf.locked_element_ids
        ]
        self._rebuild_lock_ui()

    # ------------------------------------------------------------------
    # Public API — build / save
    # ------------------------------------------------------------------

    def build_puzzle_file(self) -> PuzzleFile:
        """
        Construct a PuzzleFile from the current editor state.
        Raises ValueError if the title is empty.
        """
        title = self.get_title()
        if not title:
            raise ValueError("Puzzle title must not be empty.")

        goal = GoalSpec(
            target_ratio=self.get_target_ratio(),
            target_direction=self.get_target_direction(),
            max_gears=self.get_max_gears(),
        )
        hints = [h for h in self.get_hints() if h.strip()]
        initial_state = GearSystem(
            elements=list(self._gears),
            connections=[],
            driver_rpm=_RPM,
            driver_direction=Direction.CW,
        )
        return PuzzleFile(
            title=title,
            description=self.get_description(),
            difficulty=PuzzleDifficulty(self.get_difficulty()),
            initial_state=initial_state,
            goal=goal,
            hints=hints,
            locked_element_ids=list(self._locked_ids),
        )

    def save_to_path(self, path: str) -> None:
        """Build the PuzzleFile and serialise it to *path*."""
        pf = self.build_puzzle_file()
        save_puzzle(pf, path)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _rebuild_lock_ui(self) -> None:
        """Rebuild the lock checkbox list from self._gears."""
        # Clear existing checkboxes
        while self._lock_inner_layout.count():
            item = self._lock_inner_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self._lock_checkboxes.clear()

        for g in self._gears:
            role = "Driver" if g.is_driver else "Gear"
            gid = g.id if isinstance(g.id, uuid.UUID) else uuid.UUID(str(g.id))
            cb = QCheckBox(f"{role} — {g.tooth_count}T  (id: {str(gid)[:8]}…)")
            cb.setChecked(gid in self._locked_ids)

            def _on_toggle(checked: bool, _id: uuid.UUID = gid) -> None:
                self.set_gear_locked(_id, checked)

            cb.toggled.connect(_on_toggle)
            self._lock_checkboxes[gid] = cb
            self._lock_inner_layout.addWidget(cb)
