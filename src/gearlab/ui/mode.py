"""
Application mode system — E05-S1.

AppMode    : five named modes that determine which UI panels are visible.
ModeController : holds current mode and provides per-mode capability queries.
"""
from __future__ import annotations

from enum import Enum


# ---------------------------------------------------------------------------
# AppMode enum
# ---------------------------------------------------------------------------

class AppMode(str, Enum):
    EXPLORER     = "explorer"       # read-only, icon-only toolbar, simple badges
    STUDENT      = "student"        # playback + formula panel, hidden defects
    ENGINEER     = "engineer"       # all controls, defect injection, full badges
    PUZZLE       = "puzzle"         # challenge mode; editing locked by puzzle engine
    PRESENTATION = "presentation"   # clean canvas, no toolbar noise


# ---------------------------------------------------------------------------
# Per-mode capability matrix
# ---------------------------------------------------------------------------

_EDIT_CONTROLS:    frozenset[AppMode] = frozenset({AppMode.ENGINEER})
_DEFECT_CONTROLS:  frozenset[AppMode] = frozenset({AppMode.ENGINEER})
_FORMULA_PANEL:    frozenset[AppMode] = frozenset({AppMode.STUDENT, AppMode.ENGINEER})
_FULL_RATIO_BADGE: frozenset[AppMode] = frozenset({AppMode.STUDENT, AppMode.ENGINEER})
_MIN_RATIO_BADGE:  frozenset[AppMode] = frozenset({AppMode.EXPLORER})
# PUZZLE / PRESENTATION → "hidden"


# ---------------------------------------------------------------------------
# ModeController
# ---------------------------------------------------------------------------

class ModeController:
    """
    Tracks the current AppMode and answers per-mode UI capability queries.

    All methods are pure; no Qt dependencies.
    """

    def __init__(self) -> None:
        self.current: AppMode = AppMode.EXPLORER

    def set_mode(self, mode: AppMode) -> AppMode:
        """Switch to *mode* and return it (for chaining / assignment)."""
        self.current = mode
        return mode

    # ------------------------------------------------------------------
    # Capability queries (E05-S1-02 … 06)
    # ------------------------------------------------------------------

    def shows_edit_controls(self) -> bool:
        """Add Gear / Delete / Teeth spinbox — Engineer only."""
        return self.current in _EDIT_CONTROLS

    def shows_defect_controls(self) -> bool:
        """Per-tooth defect grid / injection UI — Engineer only."""
        return self.current in _DEFECT_CONTROLS

    def shows_formula_panel(self) -> bool:
        """Gear-ratio formula panel — Student and Engineer."""
        return self.current in _FORMULA_PANEL

    def ratio_badge_style(self) -> str:
        """
        Return "full" | "minimal" | "hidden" for ratio badge rendering.

        full     — tooth-count ratio + RPM values (Student / Engineer)
        minimal  — plain ratio fraction only (Explorer)
        hidden   — no badges (Puzzle / Presentation)
        """
        if self.current in _FULL_RATIO_BADGE:
            return "full"
        if self.current in _MIN_RATIO_BADGE:
            return "minimal"
        return "hidden"
