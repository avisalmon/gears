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
    QGraphicsView,
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

        self._scene = QGraphicsScene(self)
        self._canvas = QGraphicsView(self._scene, self)
        self._canvas.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._canvas.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self._canvas.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self._canvas.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        self.setCentralWidget(self._canvas)

        self._controller = None   # set by _setup_demo
        self._fit_rect   = None   # bounding rect to fit on first show
        self._new_tooth_count = 20  # default for Add Gear spinbox
        self._gear_label_items: list = []  # floating RPM/info labels
        self._static_overlays:  list = []  # ratio badges + title (hidden in Presentation)

        from gearlab.ui.mode import ModeController
        self._mode_ctrl = ModeController()

        self._setup_demo()
        self._setup_mode_bar()
        self._setup_toolbar()
        self._apply_mode_ui()
        self._scene.selectionChanged.connect(self._on_selection_changed)

    # ------------------------------------------------------------------
    # Demo scene — E03-S1
    # ------------------------------------------------------------------

    def _setup_demo(self) -> None:
        from gearlab.canvas.animation import AnimationController
        from gearlab.canvas.gear_item import GearItem, add_ratio_badge
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

        # Ratio badges
        for conn in system.connections:
            ga = next(x for x in system.elements if x.id == conn.element_a)
            gb = next(x for x in system.elements if x.id == conn.element_b)
            mx = (ga.position[0] + gb.position[0]) / 2
            my = -(ga.tooth_count * M / 2) - 30
            ratio = gb.tooth_count / ga.tooth_count
            badge = (f"↓ {ratio:.0f}:1 reduction"
                     if ratio >= 1 else f"↑ 1:{1/ratio:.0f} speedup")
            self._static_overlays.append(add_ratio_badge(self._scene, mx, my, badge))

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
        self._mode_ctrl.set_mode(mode)
        self._mode_buttons[mode].setChecked(True)
        self._apply_mode_ui()

    def _apply_mode_ui(self) -> None:
        """Show/hide controls according to the current mode."""
        shows_edit = self._mode_ctrl.shows_edit_controls()
        self._btn_add_gear.setVisible(shows_edit)
        self._btn_delete.setVisible(shows_edit)
        self._tooth_spin.setVisible(shows_edit)
        self._lbl_teeth.setVisible(shows_edit)
        self._update_gear_labels()

    # ------------------------------------------------------------------
    # Live gear info labels — E05-S1 demo
    # ------------------------------------------------------------------

    def _update_gear_labels(self) -> None:
        """Create/refresh floating tooth-count + RPM labels for each gear."""
        from gearlab.canvas.gear_geometry import addendum_radius
        from gearlab.canvas.gear_item import GearItem
        from gearlab.models import Direction

        for lbl in self._gear_label_items:
            self._scene.removeItem(lbl)
        self._gear_label_items = []

        style = self._mode_ctrl.ratio_badge_style()

        # Always toggle static overlays (ratio badges + title)
        for item in self._static_overlays:
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
        for g_solved, item in pairs:
            g = next(x for x in system.elements if x.id == g_solved.id)
            item._gear.rpm = g.rpm
            item._gear._direction = getattr(g, "_direction", None)  # type: ignore[attr-defined]
            item.set_direction(getattr(g, "_direction", None))
            self._controller.register(g.id, item)
        self._controller.set_defect_callback(self._on_defect_engaged)
        self._controller.start()
        self._update_gear_labels()

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
        self._speed_slider.setValue(10)     # default 1.0×
        self._speed_slider.setFixedWidth(160)
        self._speed_slider.valueChanged.connect(self._on_speed_changed)
        bar.addWidget(self._speed_slider)

        self._speed_label = QLabel("1.0×  ")
        bar.addWidget(self._speed_label)

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
        """Keep tooth spinbox in sync with the selected gear."""
        from gearlab.canvas.gear_item import GearItem
        selected = [it for it in self._scene.selectedItems()
                    if isinstance(it, GearItem)]
        if len(selected) == 1:
            self._tooth_spin.blockSignals(True)
            self._tooth_spin.setValue(selected[0]._gear.tooth_count)
            self._tooth_spin.blockSignals(False)

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
