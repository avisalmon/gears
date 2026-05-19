"""
GearLab main application window — E03-S1.
Canvas, animation controller, and playback toolbar.
"""
import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QSpinBox,
    QToolBar,
    QButtonGroup,
)


class GearLabApp(QMainWindow):
    """Top-level application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("GearLab — Interactive Gear & Belt Simulator")
        self.resize(1280, 800)

        from gearlab.canvas.view import GearView
        self._scene = QGraphicsScene(self)
        self._canvas = GearView(self._scene, self)
        self._canvas.setDragMode(GearView.DragMode.NoDrag)
        self._canvas.setTransformationAnchor(
            GearView.ViewportAnchor.AnchorUnderMouse
        )
        self._canvas.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._canvas.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setCentralWidget(self._canvas)
        self._canvas.zoom_changed.connect(self._update_status_bar)

        self._controller = None   # set by _setup_demo
        self._fit_rect   = None   # bounding rect to fit on first show
        self._new_tooth_count = 20  # default for Add Gear spinbox
        self._gear_label_items: list = []  # floating RPM/info labels
        self._static_overlays:  list = []  # title text (hidden when badges hidden)
        self._badge_overlays:   list = []  # dynamic ratio badges (E06-S1)
        self._last_system = None            # most-recent solved GearSystem

        from gearlab.ui.mode import ModeController
        self._mode_ctrl = ModeController()

        self._setup_demo()
        self._setup_mode_bar()
        self._setup_toolbar()
        self._setup_properties_panel()
        self._setup_formula_panel()
        self._setup_puzzle_panel()
        self._apply_mode_ui()
        self._scene.selectionChanged.connect(self._on_selection_changed)
        self._update_status_bar()

    # ------------------------------------------------------------------
    # Demo scene — E03-S1
    # ------------------------------------------------------------------

    def _setup_demo(self) -> None:
        from gearlab.canvas.animation import AnimationController
        from gearlab.canvas.gear_item import GearItem
        from gearlab.engine.kinematics import solve
        from gearlab.models import (
            Connection, ConnectionType, DefectType, Direction,
            Gear, GearSystem, GearType, ToothDefect,
        )

        M = 8  # module

        gA = Gear(gear_type=GearType.SPUR, tooth_count=20, module=M,
                  position=(0.0, 0.0), is_driver=True, rpm=100.0)
        # Add a missing tooth defect to the driver so it's visible
        gA.defects = [ToothDefect(tooth_index=0, defect_type=DefectType.MISSING)]
        cd_AB = (gA.tooth_count + 40) * M / 2   # 240
        gB = Gear(gear_type=GearType.SPUR, tooth_count=40, module=M,
                  position=(cd_AB, 0.0))
        cd_BC = (40 + 20) * M / 2                # 240
        gC = Gear(gear_type=GearType.SPUR, tooth_count=20, module=M,
                  position=(cd_AB + cd_BC, 0.0))

        conn_AB = Connection(conn_type=ConnectionType.MESH,
                             element_a=gA.id, element_b=gB.id)
        conn_BC = Connection(conn_type=ConnectionType.MESH,
                             element_a=gB.id, element_b=gC.id)

        system = GearSystem(
            elements=[gA, gB, gC],
            connections=[conn_AB, conn_BC],
            driver_rpm=100.0,
            driver_direction=Direction.CW,
        )
        system = solve(system)

        self._scene.setBackgroundBrush(QBrush(QColor("#13161f")))

        # Half-tooth offset so teeth look meshed at startup
        half_B = math.pi / gB.tooth_count
        offsets = {gA.id: 0.0, gB.id: half_B, gC.id: 0.0}

        self._items: dict = {}
        for g in system.elements:
            direction = getattr(g, "_direction", None)
            item = GearItem(g)
            item.set_direction(direction)
            item.set_angle(offsets[g.id] * 180.0 / math.pi)
            item._snap_callback = self._try_snap
            self._scene.addItem(item)
            self._items[g.id] = item

        # Title text
        title = QGraphicsTextItem(
            "E03  \u00b7  involute gears  \u00b7  scroll to zoom  \u00b7  drag to pan"
        )
        title.setDefaultTextColor(QColor("#4a6a80"))
        title.setFont(QFont("Segoe UI", 9))
        br = self._scene.itemsBoundingRect()
        title.setPos(br.left(), br.bottom() + 28)
        self._scene.addItem(title)
        self._static_overlays.append(title)

        # Save rect for fitInView in showEvent
        self._fit_rect = self._scene.itemsBoundingRect().adjusted(
            -40, -60, 40, 60
        )

        # Wire up animation controller
        self._controller = AnimationController(system)
        for g in system.elements:
            self._controller.register(g.id, self._items[g.id])
        self._controller.set_defect_callback(self._on_defect_engaged)
        self._controller.start()
        self._update_tooltips()
        self._update_ratio_badges(system)

    # ------------------------------------------------------------------
    # Mode bar — E05-S1-01
    # ------------------------------------------------------------------

    def _setup_mode_bar(self) -> None:
        from gearlab.ui.mode import AppMode
        bar = QToolBar("Mode", self)
        bar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, bar)

        _LABELS = [
            (AppMode.EXPLORER,     "🔭 Explorer"),
            (AppMode.STUDENT,      "📐 Student"),
            (AppMode.ENGINEER,     "⚙️ Engineer"),
            (AppMode.PUZZLE,       "🧩 Puzzle"),
            (AppMode.PRESENTATION, "📺 Present"),
        ]

        self._mode_btn_group = QButtonGroup(self)
        self._mode_btn_group.setExclusive(True)
        self._mode_buttons: dict = {}

        for mode, label in _LABELS:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setFixedWidth(110)
            btn.clicked.connect(lambda _checked, m=mode: self._set_mode(m))
            self._mode_btn_group.addButton(btn)
            bar.addWidget(btn)
            self._mode_buttons[mode] = btn

        # Reflect default mode
        self._mode_buttons[self._mode_ctrl.current].setChecked(True)

    def _set_mode(self, mode) -> None:
        """Switch application mode and update adaptive UI."""
        from gearlab.ui.mode import AppMode
        self._mode_ctrl.set_mode(mode)
        self._mode_buttons[mode].setChecked(True)
        if mode == AppMode.PUZZLE:
            self._enter_puzzle_mode()
        self._apply_mode_ui()

    def _apply_mode_ui(self) -> None:
        """Show/hide controls according to the current mode."""
        from gearlab.ui.mode import AppMode
        shows_edit = self._mode_ctrl.shows_edit_controls()
        self._btn_add_gear.setVisible(shows_edit)
        self._btn_delete.setVisible(shows_edit)
        self._tooth_spin.setVisible(shows_edit)
        self._lbl_teeth.setVisible(shows_edit)

        # Properties panel: hidden in Presentation mode only
        is_presentation = self._mode_ctrl.current == AppMode.PRESENTATION
        if hasattr(self, "_prop_panel"):
            self._prop_panel.setVisible(not is_presentation)
            self._prop_panel.set_engineer_mode(shows_edit)

        # Formula panel: shown in Student + Engineer only
        if hasattr(self, "_formula_panel"):
            shows_formula = self._mode_ctrl.shows_formula_panel()
            self._formula_panel.setVisible(shows_formula)
            if shows_formula:
                self._formula_panel.set_mode(self._mode_ctrl.current)
                if self._last_system is not None:
                    self._formula_panel.update_for_system(self._last_system)

        # Puzzle panel: shown in Puzzle mode only
        if hasattr(self, "_puzzle_panel"):
            is_puzzle = self._mode_ctrl.current == AppMode.PUZZLE
            self._puzzle_panel.setVisible(is_puzzle)

        self._update_gear_labels()
        self._update_status_bar()

    # ------------------------------------------------------------------
    # Puzzle mode — E07-S1
    # ------------------------------------------------------------------

    def _enter_puzzle_mode(self) -> None:
        """Open a file dialog to pick a .gearlab puzzle, then load it."""
        from PyQt6.QtWidgets import QFileDialog
        from gearlab.puzzle.loader import load_puzzle
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Puzzle", "", "GearLab Puzzles (*.gearlab);;All Files (*)"
        )
        if not path:
            return
        try:
            puzzle = load_puzzle(path)
        except (FileNotFoundError, ValueError) as exc:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Load Error", str(exc))
            return
        self._load_puzzle(puzzle)

    def _load_puzzle(self, puzzle) -> None:
        """Populate canvas and panel from a PuzzleFile."""
        from gearlab.canvas.gear_item import GearItem
        from gearlab.canvas.animation import AnimationController
        from gearlab.engine.kinematics import solve
        from gearlab.models import GearSystem
        from gearlab.puzzle.engine import HintEngine

        # Stop existing animation
        if self._controller is not None:
            self._controller.pause()

        # Clear canvas
        self._scene.clear()
        self._items = {}
        self._badge_overlays = []
        self._gear_label_items = []
        self._static_overlays = []

        # Start with NO connections — only the driver spins at launch.
        # The player snaps free gears into mesh to form connections.
        initial = puzzle.initial_state
        start_system = GearSystem(
            elements=initial.elements,
            connections=[],
            driver_rpm=initial.driver_rpm,
            driver_direction=initial.driver_direction,
        )
        system = solve(start_system)
        locked_ids = set(puzzle.locked_element_ids)

        import math
        gears = system.elements
        offsets = {g.id: 0.0 for g in gears}

        for g in gears:
            direction = getattr(g, "_direction", None)
            item = GearItem(g)
            item.set_direction(direction)
            item.set_angle(offsets[g.id] * 180.0 / math.pi)
            item._snap_callback = self._try_snap
            if g.id in locked_ids:
                item.set_locked(True)
            self._scene.addItem(item)
            self._items[g.id] = item

        self._controller = AnimationController(system)
        for g in system.elements:
            self._controller.register(g.id, self._items[g.id])
        self._controller.set_defect_callback(self._on_defect_engaged)
        self._controller.start()

        self._active_puzzle = puzzle
        self._hint_engine = HintEngine(puzzle.hints)
        self._puzzle_panel.load_puzzle(puzzle)
        self._update_ratio_badges(system)
        self._update_status_bar()

    def _on_puzzle_check(self) -> None:
        """Check the current system against the active puzzle goal."""
        if self._active_puzzle is None or self._last_system is None:
            return
        from gearlab.engine.kinematics import solve
        from gearlab.puzzle.engine import GoalChecker, StarRater
        system = solve(self._last_system)
        result = GoalChecker().check(system, self._active_puzzle.goal)
        self._puzzle_panel.show_result(result)
        if result.solved:
            hints_used = self._hint_engine.hints_used if self._hint_engine else 0
            stars = StarRater().rate(hints_used)
            self._puzzle_panel.show_stars(stars)

    def _on_puzzle_hint(self) -> None:
        """Reveal the next hint for the active puzzle."""
        if self._hint_engine is None:
            return
        hint = self._hint_engine.reveal_next()
        if hint is not None:
            self._puzzle_panel.show_hint(hint, self._hint_engine.hints_used)

    # ------------------------------------------------------------------

    def _setup_properties_panel(self) -> None:
        from PyQt6.QtCore import Qt
        from gearlab.ui.properties_panel import PropertiesPanel
        self._prop_panel = PropertiesPanel(self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self._prop_panel)
        # Connect panel signals → app handlers
        self._prop_panel.tooth_count_changed.connect(self._on_panel_tooth_count)
        self._prop_panel.module_changed.connect(self._on_panel_module)
        self._prop_panel.driver_toggled.connect(self._on_panel_driver_toggled)
        self._prop_panel.driver_rpm_changed.connect(self._on_panel_driver_rpm)
        self._prop_panel.defect_toggled.connect(self._on_panel_defect_toggled)

    # ------------------------------------------------------------------
    # Formula panel — E06-S1
    # ------------------------------------------------------------------

    def _setup_formula_panel(self) -> None:
        from PyQt6.QtCore import Qt
        from gearlab.ui.formula_panel import FormulaPanel
        self._formula_panel = FormulaPanel(self)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self._formula_panel)

    def _setup_puzzle_panel(self) -> None:
        from PyQt6.QtCore import Qt
        from gearlab.ui.puzzle_panel import PuzzlePanel
        self._puzzle_panel = PuzzlePanel(self)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._puzzle_panel)
        self._puzzle_panel.setVisible(False)
        self._puzzle_panel.check_requested.connect(self._on_puzzle_check)
        self._puzzle_panel.hint_requested.connect(self._on_puzzle_hint)
        self._hint_engine = None
        self._active_puzzle = None

    def _update_ratio_badges(self, system) -> None:
        """Rebuild dynamic ratio badges for every mesh connection in *system*."""
        from gearlab.canvas.gear_geometry import pitch_radius
        from gearlab.canvas.gear_item import add_ratio_badge

        # Remove old badges from scene
        for item in self._badge_overlays:
            self._scene.removeItem(item)
        self._badge_overlays.clear()

        self._last_system = system
        if system is None:
            return

        for conn in system.connections:
            ga = next((x for x in system.elements if x.id == conn.element_a), None)
            gb = next((x for x in system.elements if x.id == conn.element_b), None)
            if ga is None or gb is None:
                continue
            mx = (ga.position[0] + gb.position[0]) / 2
            r_a = pitch_radius(ga.tooth_count, ga.module)
            my = (ga.position[1] + gb.position[1]) / 2 - r_a - 30
            ratio = gb.tooth_count / ga.tooth_count
            badge_text = (
                f"\u2193 {ratio:.0f}:1 reduction"
                if ratio >= 1
                else f"\u2191 1:{1/ratio:.0f} speedup"
            )
            badge = add_ratio_badge(self._scene, mx, my, badge_text)
            self._badge_overlays.append(badge)

        # Apply current mode visibility
        style = self._mode_ctrl.ratio_badge_style()
        for item in self._badge_overlays:
            item.setVisible(style != "hidden")

    def _on_panel_tooth_count(self, v: int) -> None:
        """Properties panel tooth count changed — same logic as toolbar spinbox."""
        self._on_tooth_count_changed(v)

    def _on_panel_module(self, v: float) -> None:
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems() if isinstance(it, GearItem)]
        if len(selected) == 1:
            gear = selected[0]._gear
            if gear.module != v:
                gear.module = v
                selected[0]._rebuild_path()
                self._rebuild_system()

    def _on_panel_driver_toggled(self, is_driver: bool) -> None:
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems() if isinstance(it, GearItem)]
        if len(selected) == 1:
            if is_driver:
                # Only one driver allowed — clear all others first
                for item in self._scene.items():
                    if isinstance(item, GearItem) and item is not selected[0]:
                        item._gear.is_driver = False
            selected[0]._gear.is_driver = is_driver
            self._rebuild_system()

    def _on_panel_driver_rpm(self, rpm: float) -> None:
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems() if isinstance(it, GearItem)]
        if len(selected) == 1 and selected[0]._gear.is_driver:
            selected[0]._gear.rpm = rpm
            self._rebuild_system()

    def _on_panel_defect_toggled(self, tooth_index: int, is_defective: bool) -> None:
        from gearlab.canvas.gear_item import GearItem
        from gearlab.models import DefectType, ToothDefect
        selected = [it for it in self._scene.selectedItems() if isinstance(it, GearItem)]
        if len(selected) != 1:
            return
        gear = selected[0]._gear
        if is_defective:
            if not any(d.tooth_index == tooth_index for d in gear.defects):
                gear.defects.append(ToothDefect(tooth_index=tooth_index,
                                                 defect_type=DefectType.MISSING))
        else:
            gear.defects = [d for d in gear.defects if d.tooth_index != tooth_index]
        selected[0]._rebuild_path()

    # ------------------------------------------------------------------
    # Status bar — E05-S2-08
    # ------------------------------------------------------------------

    def _update_status_bar(self, _zoom: float | None = None) -> None:
        """Refresh status bar: Mode | Ratio | Output RPM | Zoom."""
        from gearlab.canvas.gear_item import GearItem
        mode_name = self._mode_ctrl.current.value.title()
        zoom_pct  = int(self._canvas.transform().m11() * 100)

        # Find selected gear for ratio / RPM info
        selected = [it for it in self._scene.selectedItems() if isinstance(it, GearItem)]
        if selected:
            gear = selected[0]._gear
            rpm  = getattr(gear, "rpm", 0.0) or 0.0
            rpm_text = f"{rpm:.0f} RPM"
            # Ratio relative to driver
            driver_rpm = next(
                (g._gear.rpm for g in self._scene.items()
                 if isinstance(g, GearItem) and g._gear.is_driver),
                None,
            )
            if driver_rpm and rpm > 0:
                ratio = driver_rpm / rpm
                ratio_text = f"{ratio:.2f}:1"
            else:
                ratio_text = "—"
        else:
            ratio_text = "—"
            rpm_text   = "—"

        self.statusBar().showMessage(
            f"Mode: {mode_name}  |  Ratio: {ratio_text}  |  Output: {rpm_text}  |  Zoom: {zoom_pct}%"
        )

    # ------------------------------------------------------------------
    # Live gear info labels — E05-S1 demo
    # ------------------------------------------------------------------

    def _update_tooltips(self) -> None:
        """Set plain-language 'Why?' tooltips on every GearItem — E05-S2-09."""
        from gearlab.canvas.gear_item import GearItem
        from gearlab.models import Direction
        items = [it for it in self._scene.items() if isinstance(it, GearItem)]
        driver_gear = next((it._gear for it in items if it._gear.is_driver), None)

        for item in items:
            gear = item._gear
            rpm  = getattr(gear, "rpm", 0.0) or 0.0
            direction = getattr(gear, "_direction", None)
            dir_text  = "clockwise (↻)" if direction == Direction.CW else "counter-clockwise (↺)"

            if gear.is_driver:
                tip = (
                    f"Driver gear — {gear.tooth_count} teeth\n"
                    f"Input: {rpm:.0f} RPM, spinning {dir_text}.\n"
                    f"This gear drives the whole system."
                )
            elif driver_gear and rpm > 0 and driver_gear.rpm > 0:
                ratio = driver_gear.rpm / rpm
                tip = (
                    f"{gear.tooth_count} teeth — {rpm:.0f} RPM, spinning {dir_text}.\n"
                    f"Overall ratio from driver: {ratio:.2f}:1\n"
                    f"Why? Ratio = driver teeth / this gear's teeth along the chain."
                )
            else:
                tip = (
                    f"{gear.tooth_count} teeth — not connected to the driver.\n"
                    f"Drag it close to another gear to connect."
                )
            item.setToolTip(tip)

    def _update_gear_labels(self) -> None:
        """Create/refresh floating tooth-count + RPM labels for each gear."""
        from gearlab.canvas.gear_geometry import addendum_radius
        from gearlab.canvas.gear_item import GearItem
        from gearlab.models import Direction

        for lbl in self._gear_label_items:
            self._scene.removeItem(lbl)
        self._gear_label_items = []

        style = self._mode_ctrl.ratio_badge_style()

        # Toggle static overlays (title text) and dynamic badge overlays
        for item in self._static_overlays:
            item.setVisible(style != "hidden")
        for item in self._badge_overlays:
            item.setVisible(style != "hidden")

        if style == "hidden":
            return

        for item in self._scene.items():
            if not isinstance(item, GearItem):
                continue
            gear = item._gear
            pos  = item.pos()
            r_a  = addendum_radius(gear.tooth_count, gear.module)

            if style == "full":
                direction = getattr(gear, "_direction", None)
                if direction == Direction.CW:
                    arrow = "\u21bb"      # ↻
                elif direction == Direction.CCW:
                    arrow = "\u21ba"      # ↺
                else:
                    arrow = ""
                rpm_val = getattr(gear, "rpm", 0.0) or 0.0
                text  = f"{gear.tooth_count}T  ·  {rpm_val:.0f} RPM {arrow}"
                color = QColor("#e2e4f0")
                fsize = 9
            else:  # "minimal"
                text  = f"{gear.tooth_count}T"
                color = QColor("#7a7f9a")
                fsize = 8

            lbl = QGraphicsTextItem(text)
            lbl.setDefaultTextColor(color)
            lbl.setFont(QFont("Segoe UI", fsize))
            # Centre the label horizontally above the gear
            br = lbl.boundingRect()
            lbl.setPos(pos.x() - br.width() / 2,
                       pos.y() - r_a - br.height() - 6)
            self._scene.addItem(lbl)
            self._gear_label_items.append(lbl)

    # ------------------------------------------------------------------
    # Defect engagement callback — E04-S2-05
    # ------------------------------------------------------------------

    def _on_defect_engaged(self, gear_id) -> None:
        """Flash the GearItem whose defective tooth just engaged."""
        item = self._items.get(gear_id)
        if item is not None:
            item.flash()

    # ------------------------------------------------------------------
    # Canvas interaction — E03-S2
    # ------------------------------------------------------------------

    def keyPressEvent(self, event) -> None:  # type: ignore[override]
        if event.key() == Qt.Key.Key_Delete:
            self._delete_selected()
        elif event.key() == Qt.Key.Key_Escape:
            self._scene.clearSelection()
        else:
            super().keyPressEvent(event)

    def _add_gear(self) -> None:
        """Add a new gear below the existing gear cluster and select it."""
        from gearlab.canvas.gear_geometry import addendum_radius
        from gearlab.canvas.gear_item import GearItem
        from gearlab.models import Gear, GearType

        # Spawn below all current gear items so nothing overlaps
        r_new = addendum_radius(self._new_tooth_count, 8.0)
        existing = [it for it in self._scene.items() if isinstance(it, GearItem)]
        if existing:
            max_y = max(
                it.pos().y() + addendum_radius(it._gear.tooth_count, it._gear.module)
                for it in existing
            )
            spawn_x = sum(it.pos().x() for it in existing) / len(existing)
            spawn_y = max_y + r_new + 40.0
        else:
            spawn_x, spawn_y = 0.0, 0.0

        gear = Gear(
            gear_type=GearType.SPUR,
            tooth_count=self._new_tooth_count,
            module=8.0,
            position=(spawn_x, spawn_y),
        )
        item = GearItem(gear)
        item._snap_callback = self._try_snap
        self._scene.addItem(item)
        self._items[gear.id] = item
        self._scene.clearSelection()
        item.setSelected(True)
        self._rebuild_system()

    def _delete_selected(self) -> None:
        """Remove all selected GearItems from the scene."""
        from gearlab.canvas.gear_item import GearItem
        for item in list(self._scene.selectedItems()):
            if isinstance(item, GearItem):
                self._items.pop(item._gear.id, None)
                self._scene.removeItem(item)
        self._rebuild_system()

    def _try_snap(self, moved_item) -> None:
        """Called on mouse-release; snaps the item to the nearest gear if close."""
        from gearlab.canvas.gear_item import GearItem
        from gearlab.canvas.snap import snap_position

        pos = moved_item.pos()
        gear = moved_item._gear
        anchors = [
            (other.pos().x(), other.pos().y(),
             other._gear.tooth_count, other._gear.module)
            for other in self._scene.items()
            if isinstance(other, GearItem) and other is not moved_item
        ]
        snapped = snap_position(
            (pos.x(), pos.y()), gear.tooth_count, gear.module, anchors
        )
        if snapped is not None:
            moved_item.setPos(snapped[0], snapped[1])
        self._rebuild_system()

    def _rebuild_system(self) -> None:
        """Re-detect connections, re-solve kinematics, restart animation."""
        from gearlab.canvas.animation import AnimationController
        from gearlab.canvas.gear_geometry import pitch_radius
        from gearlab.canvas.gear_item import GearItem
        from gearlab.engine.kinematics import solve
        from gearlab.models import (
            Connection, ConnectionType, Direction, GearSystem,
        )

        if self._controller is not None:
            self._controller.pause()

        # Collect gear items, sync positions
        pairs: list[tuple] = []
        for item in self._scene.items():
            if isinstance(item, GearItem):
                p = item.pos()
                item._gear.position = (p.x(), p.y())
                pairs.append((item._gear, item))

        if not pairs:
            return

        gears = [g for g, _ in pairs]

        # Auto-detect MESH connections by center-distance proximity
        connections: list[Connection] = []
        for i, (g1, _) in enumerate(pairs):
            for j, (g2, _) in enumerate(pairs):
                if j <= i:
                    continue
                cd_exp = (pitch_radius(g1.tooth_count, g1.module)
                          + pitch_radius(g2.tooth_count, g2.module))
                dx = g1.position[0] - g2.position[0]
                dy = g1.position[1] - g2.position[1]
                if abs(math.sqrt(dx * dx + dy * dy) - cd_exp) < 4.0:
                    connections.append(Connection(
                        conn_type=ConnectionType.MESH,
                        element_a=g1.id,
                        element_b=g2.id,
                    ))

        driver = next((g for g in gears if g.is_driver), None)
        if driver is None:
            driver = gears[0]
            driver.is_driver = True
        driver.rpm = driver.rpm if driver.rpm > 0 else 100.0
        system = GearSystem(
            elements=gears,
            connections=connections,
            driver_rpm=driver.rpm,
            driver_direction=Direction.CW,
        )
        system = solve(system)

        self._controller = AnimationController(system)
        # Preserve current speed — rebuild must not reset to 1.0×
        if hasattr(self, "_speed_slider"):
            self._controller.set_speed(self._speed_slider.value() / 10.0)
        for g_solved, item in pairs:
            g = next(x for x in system.elements if x.id == g_solved.id)
            item._gear.rpm = g.rpm
            item._gear._direction = getattr(g, "_direction", None)  # type: ignore[attr-defined]
            item.set_direction(getattr(g, "_direction", None))
            self._controller.register(g.id, item)
        self._controller.set_defect_callback(self._on_defect_engaged)
        self._controller.start()

        # Conflict detection: freeze if a gear is caught between contradicting neighbours
        from gearlab.engine.kinematics import has_direction_conflict
        if has_direction_conflict(system):
            self._controller.pause()
            if hasattr(self, "_conflict_label"):
                self._conflict_label.setText("  ⚠ Gear conflict — system locked  ")
                self._conflict_label.setStyleSheet("color: #ff4444; font-weight: bold;")
        else:
            if hasattr(self, "_conflict_label"):
                self._conflict_label.setText("")

        self._update_tooltips()
        self._update_gear_labels()
        self._update_ratio_badges(system)
        if hasattr(self, "_formula_panel"):
            self._formula_panel.set_mode(self._mode_ctrl.current)
            self._formula_panel.update_for_system(system)
        self._update_status_bar()

    # ------------------------------------------------------------------
    # Playback toolbar — E03-S1-04 / E03-S1-05
    # ------------------------------------------------------------------

    def _setup_toolbar(self) -> None:
        bar = QToolBar("Playback", self)
        bar.setMovable(False)
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, bar)

        # --- Gear editing controls (E03-S2) ---
        self._btn_add_gear = QPushButton("＋ Add Gear")
        self._btn_add_gear.setFixedWidth(100)
        self._btn_add_gear.clicked.connect(self._add_gear)
        bar.addWidget(self._btn_add_gear)

        self._btn_delete = QPushButton("🗑 Delete")
        self._btn_delete.setFixedWidth(80)
        self._btn_delete.clicked.connect(self._delete_selected)
        bar.addWidget(self._btn_delete)

        self._lbl_teeth = QLabel("  Teeth:")
        bar.addWidget(self._lbl_teeth)
        self._tooth_spin = QSpinBox()
        self._tooth_spin.setRange(8, 100)
        self._tooth_spin.setValue(20)
        self._tooth_spin.setFixedWidth(60)
        self._tooth_spin.valueChanged.connect(self._on_tooth_count_changed)
        bar.addWidget(self._tooth_spin)

        bar.addSeparator()

        # --- Playback controls ---
        self._btn_playpause = QPushButton("⏸  Pause")
        self._btn_playpause.setFixedWidth(90)
        self._btn_playpause.clicked.connect(self._toggle_play_pause)
        bar.addWidget(self._btn_playpause)

        btn_step = QPushButton("▶|  Step")
        btn_step.setFixedWidth(80)
        btn_step.clicked.connect(self._step_frame)
        bar.addWidget(btn_step)

        bar.addSeparator()

        lbl = QLabel("  Speed:")
        bar.addWidget(lbl)

        self._speed_slider = QSlider(Qt.Orientation.Horizontal)
        self._speed_slider.setMinimum(1)    # represents 0.1×
        self._speed_slider.setMaximum(100)  # represents 10.0×
        self._speed_slider.setFixedWidth(160)
        bar.addWidget(self._speed_slider)

        self._speed_label = QLabel("0.2×  ")
        bar.addWidget(self._speed_label)

        # Connect after label exists so _on_speed_changed can update it.
        # setValue triggers valueChanged which applies the speed to the controller.
        self._speed_slider.valueChanged.connect(self._on_speed_changed)
        self._speed_slider.setValue(2)      # default 0.2× — slow

        self._conflict_label = QLabel("")
        bar.addWidget(self._conflict_label)

    def _on_tooth_count_changed(self, v: int) -> None:
        """Spinbox changed: update selected gear's tooth count, or set new-gear default."""
        self._new_tooth_count = v
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems()
                    if isinstance(it, GearItem)]
        if len(selected) == 1:
            gear = selected[0]._gear
            if gear.tooth_count != v:
                gear.tooth_count = v
                selected[0]._rebuild_path()
                self._rebuild_system()

    def _on_selection_changed(self) -> None:
        """Keep toolbar spinbox and properties panel in sync with the selected gear."""
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems()
                    if isinstance(it, GearItem)]
        if len(selected) == 1:
            gear = selected[0]._gear
            self._tooth_spin.blockSignals(True)
            self._tooth_spin.setValue(gear.tooth_count)
            self._tooth_spin.blockSignals(False)

            # Populate properties panel
            if hasattr(self, "_prop_panel"):
                driver_rpm = next(
                    (g._gear.rpm for g in self._scene.items()
                     if isinstance(g, GearItem) and g._gear.is_driver),
                    None,
                )
                rpm = getattr(gear, "rpm", 0.0) or 0.0
                ratio = (driver_rpm / rpm) if (driver_rpm and rpm > 0) else None
                self._prop_panel.populate(gear, ratio=ratio)
        else:
            if hasattr(self, "_prop_panel"):
                self._prop_panel.clear()

        self._update_status_bar()

    # ------------------------------------------------------------------
    # Toolbar callbacks
    # ------------------------------------------------------------------

    def _toggle_play_pause(self) -> None:
        if self._controller is None:
            return
        if self._controller.is_running:
            self._controller.pause()
            self._btn_playpause.setText("▶  Play")
        else:
            self._controller.start()
            self._btn_playpause.setText("⏸  Pause")

    def _step_frame(self) -> None:
        if self._controller is not None:
            self._controller.step_frame()

    def _on_speed_changed(self, slider_val: int) -> None:
        speed = slider_val / 10.0
        self._speed_label.setText(f"{speed:.1f}×  ")
        if self._controller is not None:
            self._controller.set_speed(speed)

    # ------------------------------------------------------------------
    # showEvent — fix fitInView (E03-S1-06)
    # ------------------------------------------------------------------

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self._fit_rect is not None:
            self._canvas.fitInView(
                self._fit_rect,
                Qt.AspectRatioMode.KeepAspectRatio,
            )
            self._fit_rect = None   # only do this once
