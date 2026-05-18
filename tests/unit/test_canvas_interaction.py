"""
E03-S2 — Unit tests for canvas interaction.
Covers: select, highlight, delete, add gear, snap-to-mesh, rebuild animation.
All tests must FAIL before implementation.
"""
import pytest

from gearlab.models import Gear, GearType


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _spur(tooth_count=20, module=8.0, **kw) -> Gear:
    return Gear(gear_type=GearType.SPUR, tooth_count=tooth_count,
                module=module, position=(0.0, 0.0), **kw)


# ---------------------------------------------------------------------------
# E03-S2-03 — Click-to-select (flags)
# ---------------------------------------------------------------------------

def test_gear_item_is_selectable(qtbot):
    from PyQt6.QtWidgets import QGraphicsItem
    from gearlab.canvas.gear_item import GearItem
    item = GearItem(_spur())
    assert item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsSelectable


def test_gear_item_is_movable(qtbot):
    from PyQt6.QtWidgets import QGraphicsItem
    from gearlab.canvas.gear_item import GearItem
    item = GearItem(_spur())
    assert item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsMovable


def test_selected_item_appears_in_scene_selection(qtbot):
    from PyQt6.QtWidgets import QGraphicsScene
    from gearlab.canvas.gear_item import GearItem
    gear = _spur()
    scene = QGraphicsScene()
    item = GearItem(gear)
    scene.addItem(item)
    item.setSelected(True)
    assert item in scene.selectedItems()


def test_deselect_clears_scene_selection(qtbot):
    from PyQt6.QtWidgets import QGraphicsScene
    from gearlab.canvas.gear_item import GearItem
    scene = QGraphicsScene()
    item = GearItem(_spur())
    scene.addItem(item)
    item.setSelected(True)
    item.setSelected(False)
    assert item not in scene.selectedItems()


# ---------------------------------------------------------------------------
# E03-S2-02 — Snap-to-mesh geometry (pure math)
# ---------------------------------------------------------------------------

def test_snap_returns_exact_center_distance():
    """Gear dragged within snap radius snaps to exact CD from anchor."""
    from gearlab.canvas.snap import snap_position
    # anchor: 20T @ (0,0); drag gear: 20T; CD = 80+80 = 160
    # snap_radius = 160 * 0.5 = 80; drag to (60, 0) → dist=60 < 80 → snap
    pos = snap_position((60.0, 0.0), 20, 8.0, [(0.0, 0.0, 20, 8.0)])
    assert pos is not None
    assert abs(pos[0] - 160.0) < 0.5
    assert abs(pos[1] - 0.0) < 0.5


def test_snap_returns_none_outside_radius():
    """Gear dragged outside snap radius returns None."""
    from gearlab.canvas.snap import snap_position
    # drag at (300, 0): dist from anchor (0,0) = 300 > snap_radius=80
    pos = snap_position((300.0, 0.0), 20, 8.0, [(0.0, 0.0, 20, 8.0)])
    assert pos is None


def test_snap_snaps_to_nearest_anchor():
    """When two anchors are present, snap selects the closest one."""
    from gearlab.canvas.snap import snap_position
    # anchor A: 20T@(0,0), CD_A=160, snap_r_A=80
    # anchor B: 40T@(400,0), CD_B=80+160=240, snap_r_B=120
    # drag to (50, 0): dist_to_A=50 < 80 → snap to A → (160, 0)
    # dist_to_B = 350 > 120 → no snap to B
    pos = snap_position((50.0, 0.0), 20, 8.0,
                        [(0.0, 0.0, 20, 8.0), (400.0, 0.0, 40, 8.0)])
    assert pos is not None
    assert abs(pos[0] - 160.0) < 0.5


def test_snap_direction_preserved():
    """Snapped position is in the same direction as the drag from the anchor."""
    from gearlab.canvas.snap import snap_position
    import math
    # Drag at 45° from anchor: (40, 40) → dist=56.6 < 80 → snaps
    pos = snap_position((40.0, 40.0), 20, 8.0, [(0.0, 0.0, 20, 8.0)])
    assert pos is not None
    # Should be at distance=160 from origin in same direction
    dist = math.sqrt(pos[0] ** 2 + pos[1] ** 2)
    assert abs(dist - 160.0) < 1.0
    # Direction preserved: x ≈ y
    assert abs(pos[0] - pos[1]) < 1.0


# ---------------------------------------------------------------------------
# E03-S2-01 / E03-S2-10 — Add gear + rebuild animation
# ---------------------------------------------------------------------------

def test_rebuild_system_controller_is_running(qtbot):
    """After _rebuild_system(), AnimationController must be running."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    win._rebuild_system()
    assert win._controller is not None
    assert win._controller.is_running


def test_add_gear_increases_item_count(qtbot):
    """_add_gear() must add exactly one gear to _items."""
    from gearlab.app import GearLabApp
    win = GearLabApp()
    qtbot.addWidget(win)
    before = len(win._items)
    win._add_gear()
    assert len(win._items) == before + 1


# ---------------------------------------------------------------------------
# E03-S2-04 — Delete selected
# ---------------------------------------------------------------------------

def test_delete_selected_removes_gear(qtbot):
    """_delete_selected() removes all selected GearItems from _items."""
    from gearlab.app import GearLabApp
    from gearlab.canvas.gear_item import GearItem
    win = GearLabApp()
    qtbot.addWidget(win)
    # Select one gear item
    gear_items = [i for i in win._scene.items() if isinstance(i, GearItem)]
    assert gear_items, "Demo must have at least one GearItem"
    gear_items[0].setSelected(True)
    before = len(win._items)
    win._delete_selected()
    assert len(win._items) == before - 1
