"""
E01-S1 scaffold tests.
Covers: main window title, canvas widget, config system, error logger.
All tests must fail before implementation, pass after.
"""
import json
import logging
import sys
import types
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent.parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# ---------------------------------------------------------------------------
# E01-S1-03 — main entry point
# ---------------------------------------------------------------------------

def test_main_module_is_importable():
    """main.py must be importable without side-effects (no window opens)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("main", ROOT / "main.py")
    mod = importlib.util.module_from_spec(spec)
    # Should not raise
    spec.loader.exec_module(mod)
    assert callable(getattr(mod, "main", None)), "main() function must exist in main.py"


# ---------------------------------------------------------------------------
# E01-S1-04 — QMainWindow shell
# ---------------------------------------------------------------------------

def test_main_window_title(qtbot):
    """GearLabApp window title must match the product name from the spec."""
    from gearlab.app import GearLabApp
    window = GearLabApp()
    qtbot.addWidget(window)
    assert window.windowTitle() == "GearLab — Interactive Gear & Belt Simulator"


def test_main_window_minimum_size(qtbot):
    """Window must open at at least 1280×800 (spec §8-M1 desktop layout)."""
    from gearlab.app import GearLabApp
    window = GearLabApp()
    qtbot.addWidget(window)
    assert window.width() >= 1280
    assert window.height() >= 800


# ---------------------------------------------------------------------------
# E01-S1-05 — Canvas widget (QGraphicsView + QGraphicsScene)
# ---------------------------------------------------------------------------

def test_canvas_widget_is_graphics_view(qtbot):
    """Central widget of GearLabApp must be a QGraphicsView (not a placeholder label)."""
    from PyQt6.QtWidgets import QGraphicsView
    from gearlab.app import GearLabApp
    window = GearLabApp()
    qtbot.addWidget(window)
    assert isinstance(window.centralWidget(), QGraphicsView), (
        "centralWidget() must be a QGraphicsView, not a QLabel placeholder"
    )


def test_canvas_has_scene(qtbot):
    """The QGraphicsView must have a QGraphicsScene attached."""
    from PyQt6.QtWidgets import QGraphicsView
    from gearlab.app import GearLabApp
    window = GearLabApp()
    qtbot.addWidget(window)
    canvas = window.centralWidget()
    assert isinstance(canvas, QGraphicsView)
    assert canvas.scene() is not None, "canvas.scene() must not be None"


# ---------------------------------------------------------------------------
# E01-S1-06 — Config system
# ---------------------------------------------------------------------------

def test_config_loads_defaults(tmp_path):
    """AppConfig must write a config.json with all required keys on first load."""
    from gearlab.config import AppConfig
    cfg = AppConfig(config_dir=tmp_path)
    cfg_file = tmp_path / "config.json"
    assert cfg_file.exists(), "config.json must be created on first use"
    data = json.loads(cfg_file.read_text())
    for key in ("mode", "last_file", "research_mode"):
        assert key in data, f"config.json must contain key '{key}'"


def test_config_default_values(tmp_path):
    """AppConfig defaults: mode='student', last_file=None, research_mode=False."""
    from gearlab.config import AppConfig
    cfg = AppConfig(config_dir=tmp_path)
    assert cfg.mode == "student"
    assert cfg.last_file is None
    assert cfg.research_mode is False


def test_config_roundtrip(tmp_path):
    """Changes saved to AppConfig must persist after reload."""
    from gearlab.config import AppConfig
    cfg = AppConfig(config_dir=tmp_path)
    cfg.mode = "engineer"
    cfg.save()
    cfg2 = AppConfig(config_dir=tmp_path)
    assert cfg2.mode == "engineer"


# ---------------------------------------------------------------------------
# E01-S1-07 — Error handler & logger
# ---------------------------------------------------------------------------

def test_logger_exists():
    """gearlab.logger must expose a module-level logger named 'gearlab'."""
    from gearlab import logger as gl_logger
    log = gl_logger.get_logger()
    assert isinstance(log, logging.Logger)
    assert log.name == "gearlab"


def test_exception_handler_logs_and_does_not_reraise(caplog):
    """handle_exception() must log the error without re-raising it."""
    from gearlab.logger import handle_exception
    with caplog.at_level(logging.ERROR, logger="gearlab"):
        handle_exception(ValueError, ValueError("boom"), None)
    assert any("boom" in r.message for r in caplog.records), (
        "handle_exception must log the exception message"
    )
