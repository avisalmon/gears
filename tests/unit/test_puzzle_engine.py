"""
E07-S1 — Unit tests for Puzzle Engine & Player Experience.
All tests must FAIL before implementation (TDD RED phase).
Covers: models, loader, GoalChecker, HintEngine, StarRater, PuzzlePanel, app wiring.
"""
import json
import uuid
import pytest

from gearlab.models import (
    Connection, ConnectionType, Direction, Gear, GearSystem, GearType,
    GoalSpec, PuzzleFile, PuzzleDifficulty,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _simple_system(driver_teeth=20, driven_teeth=40) -> GearSystem:
    M = 8
    gA = Gear(gear_type=GearType.SPUR, tooth_count=driver_teeth, module=M,
              position=(0.0, 0.0), is_driver=True, rpm=100.0)
    cd = (driver_teeth + driven_teeth) * M / 2
    gB = Gear(gear_type=GearType.SPUR, tooth_count=driven_teeth, module=M,
              position=(cd, 0.0))
    conn = Connection(conn_type=ConnectionType.MESH,
                      element_a=gA.id, element_b=gB.id)
    return GearSystem(elements=[gA, gB], connections=[conn],
                      driver_rpm=100.0, driver_direction=Direction.CW)


def _simple_puzzle(title="Test Puzzle", ratio=2.0) -> PuzzleFile:
    return PuzzleFile(
        title=title,
        description="A test puzzle.",
        difficulty=PuzzleDifficulty.EASY,
        initial_state=_simple_system(),
        goal=GoalSpec(target_ratio=ratio, tolerance=0.05),
        hints=["Think about tooth counts.", "Double the teeth.", "Use 20 and 40."],
        locked_element_ids=[],
    )


# ===========================================================================
# E07-S1-01 — Model: GoalSpec extensions
# ===========================================================================

def test_goalspec_has_tolerance():
    g = GoalSpec(target_ratio=2.0, tolerance=0.05)
    assert g.tolerance == pytest.approx(0.05)


def test_goalspec_has_target_direction():
    g = GoalSpec(target_ratio=2.0, target_direction=Direction.CCW)
    assert g.target_direction == Direction.CCW


def test_goalspec_has_max_gears():
    g = GoalSpec(max_gears=3)
    assert g.max_gears == 3


def test_goalspec_to_dict():
    g = GoalSpec(target_ratio=2.0, tolerance=0.05, max_gears=3,
                 target_direction=Direction.CCW)
    d = g.to_dict()
    assert d["target_ratio"] == pytest.approx(2.0)
    assert d["tolerance"] == pytest.approx(0.05)
    assert d["max_gears"] == 3
    assert d["target_direction"] == "CCW"


def test_goalspec_from_dict_roundtrip():
    g = GoalSpec(target_ratio=3.0, tolerance=0.1,
                 target_direction=Direction.CW, max_gears=4)
    g2 = GoalSpec.from_dict(g.to_dict())
    assert g2.target_ratio == pytest.approx(3.0)
    assert g2.tolerance == pytest.approx(0.1)
    assert g2.target_direction == Direction.CW
    assert g2.max_gears == 4


def test_puzzlefile_to_dict_has_all_keys():
    p = _simple_puzzle()
    d = p.to_dict()
    for key in ("title", "description", "difficulty", "initial_state",
                "goal", "hints", "locked_element_ids"):
        assert key in d


def test_puzzlefile_from_dict_roundtrip():
    p = _simple_puzzle(title="Roundtrip")
    p2 = PuzzleFile.from_dict(p.to_dict())
    assert p2.title == "Roundtrip"
    assert p2.difficulty == PuzzleDifficulty.EASY
    assert len(p2.hints) == 3


# ===========================================================================
# E07-S1-01 — Puzzle loader: save / load .gearlab files
# ===========================================================================

def test_save_creates_file(tmp_path):
    from gearlab.puzzle.loader import save_puzzle
    path = str(tmp_path / "p.gearlab")
    save_puzzle(_simple_puzzle(), path)
    import os
    assert os.path.exists(path)


def test_load_roundtrip(tmp_path):
    from gearlab.puzzle.loader import load_puzzle, save_puzzle
    p = _simple_puzzle(title="Load Me")
    path = str(tmp_path / "p.gearlab")
    save_puzzle(p, path)
    p2 = load_puzzle(path)
    assert p2.title == "Load Me"
    assert len(p2.initial_state.elements) == 2


def test_saved_file_is_valid_json(tmp_path):
    from gearlab.puzzle.loader import save_puzzle
    path = str(tmp_path / "p.gearlab")
    save_puzzle(_simple_puzzle(), path)
    with open(path) as f:
        data = json.load(f)
    assert "title" in data


def test_load_missing_file_raises(tmp_path):
    from gearlab.puzzle.loader import load_puzzle
    with pytest.raises(FileNotFoundError):
        load_puzzle(str(tmp_path / "nonexistent.gearlab"))


def test_load_invalid_json_raises(tmp_path):
    from gearlab.puzzle.loader import load_puzzle
    path = str(tmp_path / "bad.gearlab")
    with open(path, "w") as f:
        f.write("not json {{{")
    with pytest.raises(ValueError):
        load_puzzle(path)


# ===========================================================================
# E07-S1-04 — GoalChecker
# ===========================================================================

def test_checker_solved_exact_ratio():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system(driver_teeth=20, driven_teeth=40))
    goal = GoalSpec(target_ratio=2.0, tolerance=0.05)
    result = GoalChecker().check(system, goal)
    assert result.solved is True


def test_checker_not_solved_wrong_ratio():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system(driver_teeth=20, driven_teeth=20))  # ratio=1.0
    goal = GoalSpec(target_ratio=2.0, tolerance=0.05)
    result = GoalChecker().check(system, goal)
    assert result.solved is False


def test_checker_within_tolerance():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    # ratio ~2.0, target 2.0, tol 0.05 → solved
    system = solve(_simple_system(driver_teeth=20, driven_teeth=40))
    goal = GoalSpec(target_ratio=2.02, tolerance=0.1)
    result = GoalChecker().check(system, goal)
    assert result.solved is True


def test_checker_feedback_mentions_target(capsys):
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system(driver_teeth=20, driven_teeth=20))
    goal = GoalSpec(target_ratio=3.0, tolerance=0.05)
    result = GoalChecker().check(system, goal)
    assert "3" in result.feedback or "ratio" in result.feedback.lower()


def test_checker_feedback_is_directional():
    """Feedback says 'too low' when ratio < target."""
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system(driver_teeth=20, driven_teeth=20))  # ratio=1.0
    goal = GoalSpec(target_ratio=3.0, tolerance=0.05)
    result = GoalChecker().check(system, goal)
    assert "low" in result.feedback.lower() or "increase" in result.feedback.lower() \
           or "more" in result.feedback.lower()


def test_checker_max_gears_exceeded():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system())   # 2 gears
    goal = GoalSpec(target_ratio=2.0, tolerance=0.05, max_gears=1)
    result = GoalChecker().check(system, goal)
    assert result.solved is False
    assert "gear" in result.feedback.lower()


def test_checker_no_ratio_goal_any_ratio_passes():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system())
    goal = GoalSpec()   # no target_ratio, no max_gears
    result = GoalChecker().check(system, goal)
    assert result.solved is True


# ===========================================================================
# E07-S1-05 — Wrong-answer feedback (directional hints)
# ===========================================================================

def test_feedback_ratio_too_high():
    from gearlab.engine.kinematics import solve
    from gearlab.puzzle.engine import GoalChecker
    system = solve(_simple_system(driver_teeth=10, driven_teeth=40))  # ratio=4.0
    goal = GoalSpec(target_ratio=2.0, tolerance=0.05)
    result = GoalChecker().check(system, goal)
    assert "high" in result.feedback.lower() or "reduc" in result.feedback.lower() \
           or "fewer" in result.feedback.lower()


# ===========================================================================
# E07-S1-06 — HintEngine
# ===========================================================================

def test_hint_engine_reveals_first_on_first_call():
    from gearlab.puzzle.engine import HintEngine
    engine = HintEngine(["Hint 1", "Hint 2", "Hint 3"])
    assert engine.reveal_next() == "Hint 1"


def test_hint_engine_reveals_in_order():
    from gearlab.puzzle.engine import HintEngine
    engine = HintEngine(["A", "B", "C"])
    engine.reveal_next()
    assert engine.reveal_next() == "B"


def test_hint_engine_count_increments():
    from gearlab.puzzle.engine import HintEngine
    engine = HintEngine(["A", "B", "C"])
    assert engine.hints_used == 0
    engine.reveal_next()
    assert engine.hints_used == 1
    engine.reveal_next()
    assert engine.hints_used == 2


def test_hint_engine_returns_none_when_exhausted():
    from gearlab.puzzle.engine import HintEngine
    engine = HintEngine(["A"])
    engine.reveal_next()
    assert engine.reveal_next() is None


def test_hint_engine_reset():
    from gearlab.puzzle.engine import HintEngine
    engine = HintEngine(["A", "B"])
    engine.reveal_next()
    engine.reveal_next()
    engine.reset()
    assert engine.hints_used == 0
    assert engine.reveal_next() == "A"


# ===========================================================================
# E07-S1-07 — StarRater
# ===========================================================================

def test_star_rater_3_stars_no_hints():
    from gearlab.puzzle.engine import StarRater
    assert StarRater().rate(hints_used=0) == 3


def test_star_rater_2_stars_one_hint():
    from gearlab.puzzle.engine import StarRater
    assert StarRater().rate(hints_used=1) == 2


def test_star_rater_1_star_two_hints():
    from gearlab.puzzle.engine import StarRater
    assert StarRater().rate(hints_used=2) == 1


def test_star_rater_1_star_many_hints():
    from gearlab.puzzle.engine import StarRater
    assert StarRater().rate(hints_used=99) == 1


# ===========================================================================
# E07-S1-02 — PuzzlePanel widget
# ===========================================================================

def test_puzzle_panel_exists(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    assert panel is not None


def test_puzzle_panel_shows_goal_text(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    panel.show()
    panel.load_puzzle(_simple_puzzle(title="My Puzzle"))
    assert "My Puzzle" in panel.get_goal_text() or "2" in panel.get_goal_text()


def test_puzzle_panel_shows_hint(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    panel.show()
    panel.show_hint("Use a bigger gear.", hint_num=1)
    assert "bigger" in panel.get_hint_text().lower()


def test_puzzle_panel_shows_stars(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    panel.show()
    panel.show_stars(3)
    assert "3" in panel.get_star_text() or "★" in panel.get_star_text()


def test_puzzle_panel_shows_feedback(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    from gearlab.puzzle.engine import GoalResult
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    panel.show()
    result = GoalResult(solved=False, feedback="Ratio too low — add more teeth.")
    panel.show_result(result)
    assert "low" in panel.get_feedback_text().lower() or \
           "ratio" in panel.get_feedback_text().lower()


def test_puzzle_panel_solved_feedback(qtbot):
    from gearlab.ui.puzzle_panel import PuzzlePanel
    from gearlab.puzzle.engine import GoalResult
    panel = PuzzlePanel()
    qtbot.addWidget(panel)
    panel.show()
    result = GoalResult(solved=True, feedback="")
    panel.show_result(result)
    text = panel.get_feedback_text().lower()
    assert "correct" in text or "solved" in text or "well done" in text or "★" in text


# ===========================================================================
# E07-S1-03 — Locked element enforcement (app level)
# ===========================================================================

def test_app_has_puzzle_panel(qtbot):
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    assert hasattr(win, "_puzzle_panel")


def test_gear_item_can_be_locked(qtbot):
    """GearItem supports a locked state that prevents dragging."""
    from gearlab.canvas.gear_item import GearItem
    from gearlab.models import Gear, GearType
    gear = Gear(gear_type=GearType.SPUR, tooth_count=20, module=8,
                position=(0.0, 0.0))
    item = GearItem(gear)
    item.set_locked(True)
    assert item.is_locked()
    assert not (item.flags() & item.GraphicsItemFlag.ItemIsMovable)


def test_gear_item_unlock_restores_movable(qtbot):
    """Unlocking a gear item restores its movable flag."""
    from gearlab.canvas.gear_item import GearItem
    from gearlab.models import Gear, GearType
    gear = Gear(gear_type=GearType.SPUR, tooth_count=20, module=8,
                position=(0.0, 0.0))
    item = GearItem(gear)
    item.set_locked(True)
    item.set_locked(False)
    assert not item.is_locked()
    assert item.flags() & item.GraphicsItemFlag.ItemIsMovable


# ===========================================================================
# E07-S1-11 — Built-in puzzle library
# ===========================================================================

def test_builtin_puzzle_easy_exists():
    from gearlab.puzzle.loader import load_puzzle, builtin_puzzle_path
    path = builtin_puzzle_path("easy_01")
    p = load_puzzle(path)
    assert p.difficulty == PuzzleDifficulty.EASY


def test_builtin_puzzle_medium_exists():
    from gearlab.puzzle.loader import load_puzzle, builtin_puzzle_path
    path = builtin_puzzle_path("medium_01")
    p = load_puzzle(path)
    assert p.difficulty == PuzzleDifficulty.MEDIUM


def test_builtin_puzzle_hard_exists():
    from gearlab.puzzle.loader import load_puzzle, builtin_puzzle_path
    path = builtin_puzzle_path("hard_01")
    p = load_puzzle(path)
    assert p.difficulty == PuzzleDifficulty.HARD


def test_builtin_puzzles_have_hints():
    from gearlab.puzzle.loader import load_puzzle, builtin_puzzle_path
    for name in ("easy_01", "medium_01", "hard_01"):
        p = load_puzzle(builtin_puzzle_path(name))
        assert len(p.hints) >= 1


def test_builtin_puzzles_have_goal():
    from gearlab.puzzle.loader import load_puzzle, builtin_puzzle_path
    for name in ("easy_01", "medium_01", "hard_01"):
        p = load_puzzle(builtin_puzzle_path(name))
        assert p.goal is not None
