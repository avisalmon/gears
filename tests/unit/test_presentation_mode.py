"""
E08-S1 — Presentation Mode tests (TDD).

Tests written before implementation — must fail until features are built.
"""
from __future__ import annotations

import pytest


def _make_app(qtbot):
    from gearlab.app import GearLabApp
    app = GearLabApp()
    qtbot.addWidget(app)
    return app


# ===========================================================================
# E08-S1-01  F11 / enter_presentation_mode() toggle
# ===========================================================================

def test_presentation_mode_entered_via_method(qtbot):
    """enter_presentation_mode() switches to PRESENTATION mode."""
    from gearlab.ui.mode import AppMode
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    assert app._mode_ctrl.current == AppMode.PRESENTATION


def test_presentation_mode_exited_via_method(qtbot):
    """exit_presentation_mode() restores the previous mode."""
    from gearlab.ui.mode import AppMode
    app = _make_app(qtbot)
    app._set_mode(AppMode.STUDENT)
    app.enter_presentation_mode()
    app.exit_presentation_mode()
    assert app._mode_ctrl.current == AppMode.STUDENT


def test_presentation_mode_default_previous_is_explorer(qtbot):
    """Exiting presentation when entered from EXPLORER restores EXPLORER."""
    from gearlab.ui.mode import AppMode
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    app.exit_presentation_mode()
    assert app._mode_ctrl.current == AppMode.EXPLORER


# ===========================================================================
# E08-S1-02  Layout — toolbox and properties panel hidden
# ===========================================================================

def test_presentation_hides_toolbar(qtbot):
    """Main toolbar is hidden in Presentation mode."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    assert app._main_toolbar.isHidden()


def test_presentation_hides_properties_panel(qtbot):
    """Properties dock is hidden in Presentation mode."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    assert app._prop_panel.isHidden()


def test_presentation_exit_restores_toolbar(qtbot):
    """Exiting Presentation mode shows the toolbar again."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    app.exit_presentation_mode()
    assert not app._main_toolbar.isHidden()


def test_presentation_exit_restores_properties_panel(qtbot):
    """Exiting Presentation mode shows the properties dock again."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    app.exit_presentation_mode()
    assert not app._prop_panel.isHidden()


# ===========================================================================
# E08-S1-03  Formula panel always visible and enlarged
# ===========================================================================

def test_presentation_shows_formula_panel(qtbot):
    """Formula panel is visible in Presentation mode."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    assert not app._formula_panel.isHidden()


def test_presentation_formula_panel_large_font(qtbot):
    """Formula panel reports enlarged font size in Presentation mode."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    # get_font_size() returns the px size set on the formula label
    assert app._formula_panel.get_font_size() >= 16


def test_presentation_exit_restores_formula_font(qtbot):
    """Exiting Presentation mode restores normal formula font size."""
    app = _make_app(qtbot)
    normal_size = app._formula_panel.get_font_size()
    app.enter_presentation_mode()
    app.exit_presentation_mode()
    assert app._formula_panel.get_font_size() == normal_size


# ===========================================================================
# E08-S1-04  Direction / ratio badge size enlarged
# ===========================================================================

def test_presentation_mode_badge_style_is_presentation(qtbot):
    """ModeController returns 'presentation' badge style in Presentation mode."""
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.PRESENTATION)
    assert mc.ratio_badge_style() == "presentation"


# ===========================================================================
# E08-S1-05  Canvas still editable
# ===========================================================================

def test_presentation_mode_canvas_accepts_interaction(qtbot):
    """GearView is not disabled in Presentation mode."""
    app = _make_app(qtbot)
    app.enter_presentation_mode()
    assert app._canvas.isEnabled()


# ===========================================================================
# E08-S1-07  ModeController — shows_formula_panel in PRESENTATION
# ===========================================================================

def test_mode_controller_shows_formula_in_presentation():
    """ModeController.shows_formula_panel() returns True for PRESENTATION."""
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.PRESENTATION)
    assert mc.shows_formula_panel() is True


def test_mode_controller_hides_edit_controls_in_presentation():
    """Edit controls (add gear / delete) are hidden in Presentation mode."""
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.PRESENTATION)
    assert mc.shows_edit_controls() is False


def test_presentation_mode_ratio_badge_not_hidden(qtbot):
    """Ratio badges are visible (not 'hidden') in Presentation mode."""
    from gearlab.ui.mode import AppMode, ModeController
    mc = ModeController()
    mc.set_mode(AppMode.PRESENTATION)
    assert mc.ratio_badge_style() != "hidden"
