"""
PuzzlePanel — E07-S1 dock widget.
Shows puzzle title, goal, feedback, hints, and star rating.
"""
from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDockWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PuzzlePanel(QDockWidget):
    """Dockable panel shown during Puzzle mode."""

    hint_requested  = pyqtSignal()
    check_requested = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__("Puzzle", parent)
        self.setAllowedAreas(
            Qt.DockWidgetArea.RightDockWidgetArea
            | Qt.DockWidgetArea.LeftDockWidgetArea
        )
        self.setMinimumWidth(220)

        inner = QWidget()
        inner.setStyleSheet("QWidget { background:#1e2030; } QLabel { color:#cdd6f4; }")
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(6)

        # Goal title
        self._title_label = QLabel("Load a puzzle to begin.")
        self._title_label.setWordWrap(True)
        self._title_label.setStyleSheet(
            "color:#cdd6f4; font-size:13px; font-weight:700;"
        )
        layout.addWidget(self._title_label)

        # Goal description
        self._goal_label = QLabel()
        self._goal_label.setWordWrap(True)
        self._goal_label.setStyleSheet("color:#a6adc8; font-size:12px;")
        layout.addWidget(self._goal_label)

        # Feedback line
        self._feedback_label = QLabel()
        self._feedback_label.setWordWrap(True)
        self._feedback_label.setStyleSheet("color:#f38ba8; font-size:11px;")
        layout.addWidget(self._feedback_label)

        # Hint area
        self._hint_label = QLabel()
        self._hint_label.setWordWrap(True)
        self._hint_label.setStyleSheet(
            "color:#fab387; font-size:11px; "
            "border:1px solid #45475a; padding:4px; border-radius:4px;"
        )
        self._hint_label.setVisible(False)
        layout.addWidget(self._hint_label)

        # Star display
        self._star_label = QLabel()
        self._star_label.setStyleSheet("color:#f9e2af; font-size:16px;")
        self._star_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._star_label.setVisible(False)
        layout.addWidget(self._star_label)

        # Buttons
        self._check_btn = QPushButton("✓ Check Solution")
        self._check_btn.setStyleSheet(
            "QPushButton { background:#313244; color:#a6e3a1; "
            "border:1px solid #45475a; border-radius:4px; padding:4px 8px; }"
            "QPushButton:hover { background:#45475a; }"
        )
        self._check_btn.clicked.connect(self.check_requested.emit)
        layout.addWidget(self._check_btn)

        self._hint_btn = QPushButton("💡 Hint")
        self._hint_btn.setStyleSheet(
            "QPushButton { background:#313244; color:#f9e2af; "
            "border:1px solid #45475a; border-radius:4px; padding:4px 8px; }"
            "QPushButton:hover { background:#45475a; }"
        )
        self._hint_btn.clicked.connect(self.hint_requested.emit)
        layout.addWidget(self._hint_btn)

        layout.addStretch()
        inner.setLayout(layout)
        self.setWidget(inner)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load_puzzle(self, puzzle) -> None:
        """Populate the panel from a PuzzleFile."""
        self._title_label.setText(puzzle.title)
        goal = puzzle.goal

        # Always show human-readable description first
        lines = []
        if puzzle.description:
            lines.append(puzzle.description)
            lines.append("")  # blank separator

        # Then the measurable goal specs
        if goal.target_ratio is not None:
            lines.append(f"🎯 Target ratio: {goal.target_ratio:.2f}")
        if goal.target_direction is not None:
            lines.append(f"🔄 Output direction: {goal.target_direction.value}")
        if goal.max_gears is not None:
            lines.append(f"⚙ Max gears: {goal.max_gears}")
        if not lines:
            lines.append("Connect the gears to meet the goal.")

        self._goal_label.setText("\n".join(lines))
        self._feedback_label.setText("")
        self._hint_label.setVisible(False)
        self._star_label.setVisible(False)

    def show_result(self, result) -> None:
        """Display a GoalResult — green on solve, red/orange on failure."""
        if result.solved:
            self._feedback_label.setStyleSheet(
                "color:#a6e3a1; font-size:12px; font-weight:600;"
            )
            self._feedback_label.setText("✓ Correct! Well done.")
        else:
            self._feedback_label.setStyleSheet(
                "color:#f38ba8; font-size:11px;"
            )
            self._feedback_label.setText(result.feedback)

    def show_hint(self, hint_text: str, hint_num: int) -> None:
        """Show the next revealed hint."""
        self._hint_label.setText(f"Hint {hint_num}: {hint_text}")
        self._hint_label.setVisible(True)

    def show_stars(self, stars: int) -> None:
        """Show star rating (1–3)."""
        filled   = "★" * stars
        unfilled = "☆" * (3 - stars)
        self._star_label.setText(filled + unfilled + f"  {stars}/3")
        self._star_label.setVisible(True)

    def clear(self) -> None:
        self._title_label.setText("Load a puzzle to begin.")
        self._goal_label.setText("")
        self._feedback_label.setText("")
        self._hint_label.setVisible(False)
        self._star_label.setVisible(False)

    # ------------------------------------------------------------------
    # Text accessors for testing
    # ------------------------------------------------------------------

    def get_goal_text(self) -> str:
        return self._title_label.text() + "\n" + self._goal_label.text()

    def get_hint_text(self) -> str:
        return self._hint_label.text()

    def get_feedback_text(self) -> str:
        return self._feedback_label.text()

    def get_star_text(self) -> str:
        return self._star_label.text()
