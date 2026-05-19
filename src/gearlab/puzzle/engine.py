"""
puzzle/engine.py — GoalChecker, HintEngine, StarRater, GoalResult.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from gearlab.models import GearSystem, GoalSpec


# ---------------------------------------------------------------------------
# GoalResult — output of GoalChecker.check()
# ---------------------------------------------------------------------------

@dataclass
class GoalResult:
    solved:        bool
    feedback:      str
    current_ratio: Optional[float] = None
    target_ratio:  Optional[float] = None


# ---------------------------------------------------------------------------
# GoalChecker — evaluates a solved GearSystem against a GoalSpec
# ---------------------------------------------------------------------------

class GoalChecker:
    """Stateless checker: call check(system, goal) to get a GoalResult."""

    def check(self, system: GearSystem, goal: GoalSpec) -> GoalResult:
        # ── max gear count ────────────────────────────────────────────────
        if goal.max_gears is not None:
            count = len(system.elements)
            if count > goal.max_gears:
                return GoalResult(
                    solved=False,
                    feedback=(
                        f"Too many gears: you have {count}, "
                        f"but the goal allows at most {goal.max_gears}. "
                        "Try removing a gear."
                    ),
                )

        # ── ratio check ───────────────────────────────────────────────────
        current_ratio: Optional[float] = None
        if goal.target_ratio is not None:
            driver = next((g for g in system.elements if g.is_driver), None)
            if driver is None:
                return GoalResult(
                    solved=False,
                    feedback="No driver gear found. Mark one gear as the driver.",
                )

            # Find the last gear in the chain (largest RPM change from driver)
            driven = next(
                (g for g in reversed(system.elements) if not g.is_driver), None
            )
            if driven is None:
                return GoalResult(
                    solved=False,
                    feedback="Need at least two gears to form a ratio.",
                )

            current_ratio = driven.tooth_count / driver.tooth_count
            diff = abs(current_ratio - goal.target_ratio) / goal.target_ratio

            if diff > goal.tolerance:
                if current_ratio < goal.target_ratio:
                    direction_hint = (
                        "Ratio too low — increase driven teeth or reduce driver teeth."
                    )
                else:
                    direction_hint = (
                        "Ratio too high — reduce driven teeth or increase driver teeth."
                    )
                return GoalResult(
                    solved=False,
                    feedback=(
                        f"Ratio is {current_ratio:.2f}, need {goal.target_ratio:.2f}. "
                        f"{direction_hint}"
                    ),
                    current_ratio=current_ratio,
                    target_ratio=goal.target_ratio,
                )

        # ── direction check ───────────────────────────────────────────────
        if goal.target_direction is not None:
            last = next(
                (g for g in reversed(system.elements) if not g.is_driver), None
            )
            if last is not None:
                actual = getattr(last, "_direction", None)
                if actual is not None and actual != goal.target_direction:
                    return GoalResult(
                        solved=False,
                        feedback=(
                            f"Output gear spins {actual.value}, "
                            f"but the goal requires {goal.target_direction.value}. "
                            "Add or remove a gear to flip the direction."
                        ),
                    )

        return GoalResult(
            solved=True,
            feedback="Correct! Well done.",
            current_ratio=current_ratio,
            target_ratio=goal.target_ratio,
        )


# ---------------------------------------------------------------------------
# HintEngine — progressive 3-level hint reveal
# ---------------------------------------------------------------------------

class HintEngine:
    """Reveals hints one at a time in order."""

    def __init__(self, hints: list[str]) -> None:
        self._hints = list(hints)
        self.hints_used: int = 0

    def reveal_next(self) -> Optional[str]:
        """Return the next hint, or None if all hints have been revealed."""
        if self.hints_used >= len(self._hints):
            return None
        hint = self._hints[self.hints_used]
        self.hints_used += 1
        return hint

    def reset(self) -> None:
        """Reset the engine so hints can be revealed again from the start."""
        self.hints_used = 0


# ---------------------------------------------------------------------------
# StarRater — 3★ no hints · 2★ one hint · 1★ two+ hints
# ---------------------------------------------------------------------------

class StarRater:
    """Stateless star calculator."""

    def rate(self, hints_used: int) -> int:
        if hints_used == 0:
            return 3
        if hints_used == 1:
            return 2
        return 1
