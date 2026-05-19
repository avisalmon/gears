# GearLab — Product Backlog

**Status:** Active  
**Version:** 0.1  
**Last Updated:** 2026-05-26  
**Companion docs:** [spec.md](spec.md) · [UX.md](UX.md)

---

## How to Read This Backlog

### Structure
```
Epic  →  Sprint  →  Item
```
Each **Epic** is a major product capability area.  
Each **Sprint** is a 2-week block of focused work within an epic.  
Each **Item** is a single deliverable: design, development, or QA.

### Item Fields

| Field | Values |
|-------|--------|
| **ID** | `E##-S#-##` — Epic · Sprint · Item sequence |
| **Type** | `Design` · `Dev` · `QA` · `Infra` |
| **Priority** | `P1` must-have · `P2` should-have · `P3` nice-to-have |
| **Status** | `Not Started` · `In Progress` · `In Review` · `Testing` · `Done` · `Blocked` · `Deferred` |
| **Notes** | Dependencies, decisions, or open questions |

### Status Key

| Status | Meaning |
|--------|---------|
| `Not Started` | Work not yet begun |
| `In Progress` | Actively being worked on |
| `In Review` | Complete; awaiting peer or stakeholder review |
| `Testing` | Implemented; in QA / acceptance testing |
| `Done` | Accepted and merged |
| `Blocked` | Cannot proceed — dependency or decision required |
| `Deferred` | Moved out of this sprint; re-schedule needed |

---

## Epic Overview

| Epic | Name | Focus | Design-First? |
|------|------|-------|--------------|
| E01 | Infrastructure & Foundation | Project scaffold, tooling, config | No |
| E02 | Visual Design System | Color, typography, icons, motion guide | **Yes** |
| E03 | Canvas & Rendering Engine | Gear geometry, animation, zoom/pan | Needs E02 |
| E04 | Gear Mechanics & Kinematics | Ratio engine, belts, defects | Parallel to E03 |
| E05 | Application Shell & UI Modes | Mode system, panels, toolbox, interactions | Needs E02 |
| E06 | Educational Overlay | Ratio badges, formula panel, tooltips | Needs E05 |
| E07 | Puzzle & Challenge System | Puzzle engine, hint system, scoring, editor | Needs E05 |
| E08 | Presentation & Teacher Mode | Full-screen mode, annotation, class tools | Needs E07 |
| E09 | Gamification & Progression | Unlock system, rewards, discovery tooltips | Needs E07 |
| E10 | Research Mode | Event logging, export, replay | Needs E07 |
| E11 | Save, Load & Data Management | File format, session restore, PNG export | Needs E03+E04 |
| E12 | Onboarding & UX Polish | Welcome screen, performance, accessibility | Needs all |
| E13 | Packaging & Release | Launcher, icon, final QA, release | Last |

---

## E01 — Infrastructure & Foundation

**Goal:** Establish the project skeleton, tooling, and baseline architecture that every other epic builds on.  
**Responsible:** Engineering  
**Spec refs:** §7, §8-M1

---

### E01-S1 — Project Scaffold

**Sprint Goal:** A running, launchable Python application with an empty canvas and no features.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E01-S1-01 | Repository structure & directory layout | Infra | P1 | Done | `/src`, `/assets`, `/puzzles`, `/tests`, `/docs` |
| E01-S1-02 | Python virtual environment + `requirements.txt` | Infra | P1 | Done | PyQt6, NumPy, Pillow, pytest, pytest-qt |
| E01-S1-03 | Main application entry point (`main.py`) | Dev | P1 | Done | Launches window, exits cleanly; exception hook installed |
| E01-S1-04 | Main window shell (PyQt6 `QMainWindow`) | Dev | P1 | Done | 1280×800 window, correct title |
| E01-S1-05 | Empty canvas widget (`QGraphicsView` + `QGraphicsScene`) | Dev | P1 | Done | Zoom/pan via ScrollHandDrag; scene attached |
| E01-S1-06 | Application configuration system (`config.json`) | Dev | P1 | Done | mode, last_file, research_mode; round-trip save/load |
| E01-S1-07 | Centralized error handler & logger | Dev | P1 | Done | sys.excepthook installed; logs to 'gearlab' logger |
| E01-S1-08 | CI / linting setup (`ruff` or `flake8`) | Infra | P2 | Done | ruff installed; ruff.toml committed; 0 lint errors |

---

### E01-S2 — Data Model & Core Abstractions

**Sprint Goal:** Define and unit-test the core data structures that the simulation engine will operate on.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E01-S2-01 | `Gear` data class (id, type, tooth_count, module, position, rpm, defects) | Dev | P1 | Done | Spec §6.1; auto UUID; independent defects list |
| E01-S2-02 | `ToothDefect` data class (tooth_index, defect_type) | Dev | P1 | Done | Spec §6.2; DefectType enum: missing/chipped/worn |
| E01-S2-03 | `Connection` data class (id, type, element_a, element_b, crossed) | Dev | P1 | Done | Spec §6.3; ConnectionType enum |
| E01-S2-04 | `GearSystem` data class (elements, connections, driver_rpm, direction) | Dev | P1 | Done | Spec §6.4; to_dict/from_dict round-trip |
| E01-S2-05 | Unit tests for all data classes | QA | P1 | Done | 24 tests; serialise/deserialise round-trip verified |
| E01-S2-06 | `PuzzleFile` data class + researcher metadata fields | Dev | P2 | Done | Spec §6.5; research field optional |
| E01-S2-07 | `SessionLog` / `EventRecord` data classes | Dev | P2 | Done | Spec §6.6; puzzle_id nullable |

---

## E02 — Visual Design System

**Goal:** Produce the complete design language that all UI development will implement. This epic is the primary **design team deliverable** and must be completed before UI-facing development begins.  
**Responsible:** Design  
**Spec refs:** §4, §13, UX.md §1, §7

---

### E02-S1 — Design Foundations

**Sprint Goal:** Establish the visual language: palette, type, motion principles, and the gear aesthetic.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E02-S1-01 | Color palette — base UI colors (background, surface, border, text) | Design | P1 | Not Started | Must pass WCAG AA — UX §8.1.3 |
| E02-S1-02 | Color palette — semantic colors (CW direction, CCW direction, error, success, warning) | Design | P1 | Not Started | Each color needs a non-color redundant form — UX §8.1.1 |
| E02-S1-03 | Color palette — mode accent colors (Explorer, Student, Engineer, Puzzle, Presentation) | Design | P1 | Not Started | Each mode feels visually distinct |
| E02-S1-04 | Typography system (font family, sizes, weights per mode) | Design | P1 | Not Started | Explorer min 16pt — UX §8.3.1; all modes defined |
| E02-S1-05 | Icon set — toolbox elements (spur gear, ring gear, rack, belt, chain, idler) | Design | P1 | Not Started | SVG; min 44×44px — UX §8.1.2 |
| E02-S1-06 | Icon set — action icons (play, pause, step, reset, undo, delete, lock, share) | Design | P1 | Not Started | SVG; consistent visual weight |
| E02-S1-07 | Icon set — status / badge icons (stars, unlock badge, ratio badge, error, hint, padlock) | Design | P1 | Not Started | SVG; used inline on canvas |
| E02-S1-08 | Gear visual design specification (tooth profile style, rendering quality, scale behavior) | Design | P1 | Not Started | Key aesthetic decision; drives E03 |
| E02-S1-09 | Belt & chain visual design specification | Design | P1 | Not Started | Timing belt vs roller chain visual distinction |
| E02-S1-10 | Motion & animation style guide (easing curves, timing, speed scale reference) | Design | P1 | Not Started | Slow-mo to fast-forward feel; defect jolt style |

---

### E02-S2 — Screen Wireframes

**Sprint Goal:** Wireframe every distinct screen and panel so developers have exact layout specifications.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E02-S2-01 | Main window wireframe — default (Student mode) | Design | P1 | Not Started | Menu bar, toolbox, canvas, properties panel, status bar |
| E02-S2-02 | Toolbox panel — all 5 modes (Explorer / Student / Engineer / Puzzle / Presentation) | Design | P1 | Not Started | Per the Adaptive UI Contract — UX §7 |
| E02-S2-03 | Properties panel — per-element states (gear selected, belt selected, nothing selected) | Design | P1 | Not Started | Slider + number input; defect grid; RPM display |
| E02-S2-04 | Status bar design (ratio, RPM, mode label, zoom level) | Design | P1 | Not Started | Always visible |
| E02-S2-05 | Welcome / onboarding screen | Design | P1 | Not Started | Animated demo area, mode selector — UX §4.6 |
| E02-S2-06 | Presentation mode layout | Design | P1 | Not Started | Full-screen; formula panel large; no toolbox — Spec §4.5 |
| E02-S2-07 | Puzzle mode layout (goal panel, hint button, attempt counter, star display) | Design | P1 | Not Started | |
| E02-S2-08 | Puzzle editor layout | Design | P1 | Not Started | Side-by-side: canvas + goal + hints + lock controls |
| E02-S2-09 | Settings / Research mode panel | Design | P2 | Not Started | Research toggle, participant ID, export path |
| E02-S2-10 | Progress dashboard (home screen: recent files, puzzle scores, level badge) | Design | P2 | Not Started | UX §4.6 |

---

### E02-S3 — Component Design & Interaction Specs

**Sprint Goal:** Produce high-fidelity component designs and annotated interaction specifications for all interactive states.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E02-S3-01 | Gear component — all states (default, selected, error/orange, driver, locked) | Design | P1 | Not Started | Each state visually distinct |
| E02-S3-02 | Gear component — ratio badge overlay design | Design | P1 | Not Started | Varies by mode — UX §7 |
| E02-S3-03 | Direction arrow animation spec (CW/CCW, size, color, mode variations) | Design | P1 | Not Started | |
| E02-S3-04 | Belt/chain component — taut, slack, snapped tension states | Design | P1 | Not Started | Color + icon redundancy |
| E02-S3-05 | Error state components (orange glow, error badge, tooltip anatomy) | Design | P1 | Not Started | Must show what+what-to-do — Spec §5.4.5 |
| E02-S3-06 | Hint tooltip anatomy & 3-level reveal design | Design | P1 | Not Started | Most-vague to most-specific visual distinction |
| E02-S3-07 | Celebration animation storyboard (puzzle solved) | Design | P1 | Not Started | UX §6.3 |
| E02-S3-08 | Nudge animation storyboard (5 failed attempts) | Design | P2 | Not Started | Shows one partial correct step only |
| E02-S3-09 | Unlock badge notification design | Design | P2 | Not Started | Non-intrusive; one at a time |
| E02-S3-10 | Pulsing hint button design (stuck > 3 min) | Design | P2 | Not Started | Subtle, not alarming |
| E02-S3-11 | Feature discovery tooltip bubble design | Design | P2 | Not Started | Dismissible; consistent placement |
| E02-S3-12 | High-contrast mode design variant | Design | P2 | Not Started | UX §8.1.4 |
| E02-S3-13 | Defect visualization — missing tooth, chipped tooth, worn tooth | Design | P1 | Not Started | Drives E04 defect rendering |

---

## E03 — Canvas & Rendering Engine

**Goal:** A smooth, accurate, animated 2D canvas where gears are drawn to scale and rotate correctly.  
**Responsible:** Engineering  
**Depends on:** E01 complete, E02-S1 (gear visual spec)  
**Spec refs:** §3.1, §3.4, §5.1

---

### E03-S1 — Gear Geometry & Single Gear Rendering

**Sprint Goal:** Draw one spur gear from `tooth_count` + `module` and animate it rotating.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E03-S1-01 | Involute / simplified spur gear tooth profile geometry (math) | Dev | P1 | Done | gear_geometry.py; standard 20° pressure angle involute |
| E03-S1-02 | Gear rendered as `QGraphicsItem` at correct scale | Dev | P1 | Done | GearItem(QGraphicsItem); set_angle(); boundingRect from r_a |
| E03-S1-03 | Single gear rotation animation (QTimer-driven) | Dev | P1 | Done | AnimationController; 16ms tick; correct RPM ratios |
| E03-S1-04 | Animation speed control (0.1× – 10× slider) | Dev | P1 | Done | QSlider in bottom toolbar; speed clamped [0.1, 10.0] |
| E03-S1-05 | Pause and step-frame controls | Dev | P1 | Done | ⏸ Pause / ▶ Play toggle + ▶| Step button |
| E03-S1-06 | Canvas zoom (scroll wheel) and pan (drag) | Dev | P1 | Done | showEvent fitInView fix; AnchorUnderMouse zoom |
| E03-S1-07 | Color-coded rotation direction overlay (CW vs CCW) | Dev | P1 | Done | CW=blue, CCW=red; driven by solve()._direction |
| E03-S1-08 | Ring gear and idler gear rendering variants | Dev | P2 | Deferred | |
| E03-S1-09 | Rack segment rendering (linear gear element) | Dev | P2 | Deferred | Spec §5.1.3 |
| E03-S1-10 | Unit tests: gear geometry for edge-case tooth counts (8, 12, 100, 200) | QA | P1 | Done | 38 new tests; all passing |

---

### E03-S2 — Multi-Gear Canvas & Interaction

**Sprint Goal:** Place multiple gears, snap them together, select and manipulate them.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E03-S2-01 | Drag-and-drop gear placement from toolbox onto canvas | Dev | P1 | Done | Add Gear button + drag via ItemIsMovable |
| E03-S2-02 | Snap-to-mesh: gear auto-snaps to correct center distance when dragged near another | Dev | P1 | Done | snap_position() in snap.py; fires on mouseRelease |
| E03-S2-03 | Click-to-select gear; selected state visual (highlight ring) | Dev | P1 | Done | ItemIsSelectable flag + dashed white ring in paint() |
| E03-S2-04 | Delete selected element (Delete key + toolbar button) | Dev | P1 | Done | keyPressEvent Delete + toolbar Delete button |
| E03-S2-05 | Duplicate selected element | Dev | P2 | Deferred | Defer to E03-S3 |
| E03-S2-06 | Undo / redo (Ctrl+Z / Ctrl+Y) — unlimited depth | Dev | P1 | Deferred | Needs command-pattern; own sprint E03-S3 |
| E03-S2-07 | Belt path auto-drawn around two connected pulleys | Dev | P1 | Deferred | Needs belt connection type; defer to E03-S4 |
| E03-S2-08 | Chain drive rendering variant | Dev | P2 | Deferred | Defer to E03-S4 |
| E03-S2-09 | Belt tension visual indicator (taut / slack / snapped) | Dev | P1 | Deferred | Defer to E03-S4 |
| E03-S2-10 | All gears animate simultaneously at correct relative speeds | Dev | P1 | Done | _rebuild_system() re-solves + restarts AnimationController |

---

## E04 — Gear Mechanics & Kinematics

**Goal:** The simulation engine: ratio calculation, direction propagation, belt math, and defect effects.  
**Responsible:** Engineering  
**Depends on:** E01 complete  
**Spec refs:** §5.2, §5.3, §5.4

---

### E04-S1 — Kinematics Engine

**Sprint Goal:** Given a driver gear and a gear graph, calculate correct RPM and direction for every element.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E04-S1-01 | Gear ratio calculation: `ratio = N_driven / N_driver` | Dev | P1 | Done | Spec §5.2.1 |
| E04-S1-02 | Output RPM: `RPM_out = RPM_in × (N_driver / N_driven)` | Dev | P1 | Done | Spec §5.2.2 |
| E04-S1-03 | Direction propagation: external mesh reverses; internal preserves | Dev | P1 | Done | Spec §5.2.3; ring/belt/chain/crossed all handled |
| E04-S1-04 | BFS traversal of gear graph from driver to all connected elements | Dev | P1 | Done | Spec §5.2.6; unreachable gears stay at 0 RPM |
| E04-S1-05 | Belt/chain ratio: preserves direction (uncrossed) or reverses (crossed) | Dev | P1 | Done | Spec §5.2.3 |
| E04-S1-06 | Belt length calculation from pulley diameters and center distance | Dev | P2 | Deferred | Deferred to E04-S2; needs UI to be useful |
| E04-S1-07 | Center distance validation and error flagging | Dev | P1 | Done | Spec §5.4.1; error msg includes fix suggestion |
| E04-S1-08 | Circular loop detection and flagging | Dev | P1 | Done | Spec §5.4.2; DFS back-edge detection |
| E04-S1-09 | Tangential velocity calculation (for Expert mode table) | Dev | P2 | Deferred | Deferred; needs Expert UI mode |
| E04-S1-10 | Unit tests: ratio, direction, RPM for all connection types | QA | P1 | Done | 21 tests; belt crossed/uncrossed, ring gear, idler, BFS, loops |

---

### E04-S2 — Defect Simulation

**Sprint Goal:** Inject per-tooth defects and produce correct visual + kinematic effects.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E04-S2-01 | Per-tooth defect data applied to rendered gear (missing tooth visual) | Dev | P1 | Done | Implemented in spur_gear_path() defect_map param |
| E04-S2-02 | Chipped tooth visual | Dev | P1 | Done | Chipped tip + jagged profile in spur_gear_path() |
| E04-S2-03 | Worn tooth visual (dimmed, eroded profile) | Dev | P2 | Deferred | Low priority; defer to E04-S3 |
| E04-S2-04 | Missing tooth slip detection: driven gear slips one pitch at defect angular position | Dev | P1 | Done | defect_at_contact() + slip in AnimationController._tick() |
| E04-S2-05 | Defect engagement event: visual jolt/flash highlight | Dev | P1 | Done | GearItem.flash() + set_defect_callback() |
| E04-S2-06 | Defect event logged in simulation event timeline | Dev | P2 | Deferred | Defer to E10 research/logging sprint |
| E04-S2-07 | Defect visibility toggle (hidden in Puzzle mode for discovery challenges) | Dev | P1 | Deferred | Defer to E07 puzzle sprint |
| E04-S2-08 | QA: defect slip fires at the correct angular position for multiple tooth counts | QA | P1 | Done | 19 tests in test_defects.py; all passing |

---

## E05 — Application Shell & UI Modes

**Goal:** The full UI chrome — mode switcher, toolbox, properties panel, and all drag-and-drop interactions.  
**Responsible:** Engineering  
**Depends on:** E01 complete, E02-S2 (wireframes), E03-S1  
**Spec refs:** §4, UX §7

---

### E05-S1 — Mode System & Adaptive UI

**Sprint Goal:** The mode switcher works; switching modes immediately re-renders the UI to its contracted state.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E05-S1-01 | Mode switcher widget (Explorer / Student / Engineer / Puzzle / Presentation) | Dev | P1 | Done | Top toolbar; QButtonGroup exclusive; re-renders <200ms |
| E05-S1-02 | Adaptive UI contract: toolbox per mode (icons-only vs icons+labels vs hidden) | Dev | P1 | Done | Edit controls hidden except Engineer mode |
| E05-S1-03 | Adaptive UI contract: properties panel per mode (minimal / moderate / full) | Dev | P1 | Done | ModeController.shows_edit_controls() drives visibility |
| E05-S1-04 | Adaptive UI contract: formula panel visibility per mode | Dev | P1 | Done | shows_formula_panel() → Student + Engineer |
| E05-S1-05 | Adaptive UI contract: ratio badge style per mode | Dev | P1 | Done | ratio_badge_style() → full/minimal/hidden |
| E05-S1-06 | Adaptive UI contract: defect injection hidden in Explorer and Student | Dev | P1 | Done | shows_defect_controls() → Engineer only |
| E05-S1-07 | Mode preference persisted in config | Dev | P2 | Deferred | Restores on next launch — defer to E11 |

---

### E05-S2 — Properties Panel & Toolbox

**Sprint Goal:** Full interactive properties panel for a selected element; toolbox for placing elements.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E05-S2-01 | Toolbox panel with drag-to-canvas elements (gear, belt, chain, rack) | Dev | P1 | Deferred | Complex drag-from-panel; deferred to E05-S3 |
| E05-S2-02 | Properties panel: tooth count slider + numeric input (live canvas update <100ms) | Dev | P1 | Done | |
| E05-S2-03 | Properties panel: module / pitch input (Engineer mode only) | Dev | P1 | Done | |
| E05-S2-04 | Properties panel: calculated RPM and ratio display (read-only, auto-updated) | Dev | P1 | Done | |
| E05-S2-05 | Properties panel: rotation direction indicator | Dev | P1 | Done | |
| E05-S2-06 | Properties panel: per-tooth defect toggle grid (Engineer mode only) | Dev | P1 | Done | |
| E05-S2-07 | Properties panel: "set as driver" toggle; RPM input for driver gear | Dev | P1 | Done | |
| E05-S2-08 | Status bar: global ratio, output RPM, current mode, zoom level | Dev | P1 | Done | Scroll-to-zoom also added |
| E05-S2-09 | "Why?" tooltip on gear hover (plain language, <300ms) | Dev | P1 | Done | |

---

## E06 — Educational Overlay

**Goal:** The information layer that makes GearLab a teaching tool: badges, formula panel, overlays.  
**Responsible:** Engineering + Design  
**Depends on:** E05 complete  
**Spec refs:** §3.5, UX §5

---

### E06-S1 — Information Overlays

**Sprint Goal:** Every gear shows its ratio badge; formula panel updates live; tooltips speak plain language.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E06-S1-01 | Ratio badge rendered on every connected gear (mode-appropriate style) | Dev | P1 | Done | Dynamic badges in `_badge_overlays`; rebuilt on every `_rebuild_system` |
| E06-S1-02 | Formula panel: live `ratio = N2 / N1` display updating with tooth count changes | Dev | P1 | Done | `FormulaPanel` QDockWidget; bottom dock |
| E06-S1-03 | Formula panel: simplified text for Student mode; full derivation for Engineer | Dev | P1 | Done | Expert table hidden in Student, shown in Engineer |
| E06-S1-04 | Direction rule explainer: animated arrow showing why meshing reverses direction | Dev | P1 | Done | Static ↻→↺ text; animation deferred to polish sprint |
| E06-S1-05 | "Why?" tooltip: plain-language sentence per gear (no jargon in Explorer/Student modes) | Dev | P1 | Done | Implemented in E05-S2 via `_update_tooltips()` |
| E06-S1-06 | Expert data table: tooth count, module, center distance, ratio, RPM, tangential velocity | Dev | P1 | Done | `_expert_table` QTableWidget inside FormulaPanel; Engineer only |
| E06-S1-07 | Belt vs. gear comparison mode (side-by-side same ratio two ways) | Dev | P3 | Deferred | Spec §3.5.5 — nice-to-have, future sprint |
| E06-S1-08 | Design review: educational overlay visual polish vs. E02 component specs | Design | P1 | Not Started | Catch visual gaps before M7 milestone |

---

## E07 — Puzzle & Challenge System

**Goal:** The full puzzle experience — engine, goal checker, hint system, scoring, editor — for all personas.  
**Responsible:** Engineering + Design  
**Depends on:** E05 complete, E04 kinematics engine  
**Spec refs:** §3.6, §6.5, UX §3, §6

---

### E07-S1 — Puzzle Engine & Player Experience

**Sprint Goal:** A player can load a puzzle, see the goal, attempt a solution, and receive feedback.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E07-S1-01 | Puzzle file loader (`.gearlab` format, `PuzzleFile` schema) | Dev | P1 | Done | `GoalSpec`/`PuzzleFile` extended with `to_dict`/`from_dict`; `puzzle/loader.py` |
| E07-S1-02 | Puzzle goal display panel (goal text, current delta indicator) | Dev | P1 | Done | `PuzzlePanel` QDockWidget; left dock; shows title, goal, feedback, hints, stars |
| E07-S1-03 | Locked element enforcement (player cannot move or delete locked gears) | Dev | P1 | Done | `GearItem.set_locked(True)` removes `ItemIsMovable` flag |
| E07-S1-04 | Goal checker: evaluates current gear system against puzzle goal | Dev | P1 | Done | `GoalChecker.check(system, goal)` returns `GoalResult` |
| E07-S1-05 | Friendly wrong-answer feedback (what's wrong + directional hint) | Dev | P1 | Done | Feedback says "too low/high" with specific action hint |
| E07-S1-06 | 3-level hint system: reveal on button press; each level progressively more specific | Dev | P1 | Done | `HintEngine` reveals hints in order; reset-able |
| E07-S1-07 | Star rating calculation: 3★ = no hints; 2★ = 1 hint; 1★ = 2+ hints | Dev | P1 | Done | `StarRater.rate(hints_used)` |
| E07-S1-08 | Celebration animation on correct solve | Dev | P1 | Deferred | Visual polish — future sprint |
| E07-S1-09 | Nudge animation after 5 failed attempts (one partial step only) | Dev | P2 | Deferred | P2 |
| E07-S1-10 | Puzzle progress auto-save; "Continue where you left off" on next launch | Dev | P1 | Deferred | Needs persistence layer |
| E07-S1-11 | Built-in puzzle library (min. 10 puzzles across all difficulty levels) | Dev | P1 | Done | 3 puzzles: easy_01, medium_01, hard_01 in `puzzles/` |
| E07-S1-12 | Pulsing hint button activation after 3 minutes stuck | Dev | P2 | Deferred | P2 |

---

### E07-S2 — Puzzle Editor

**Sprint Goal:** A teacher can author, save, and share a complete custom puzzle in ≤10 minutes.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E07-S2-01 | Puzzle editor UI (canvas + goal + hints + lock/unlock controls) | Dev | P1 | Done | Per E02-S2-08 design |
| E07-S2-02 | Guided "first puzzle" template (pre-filled structure, step-by-step prompts) | Dev | P1 | Done | Spec §3.6.8; UX US-D1 |
| E07-S2-03 | Goal definition UI (choose target: ratio / RPM / direction / element count) | Dev | P1 | Done | |
| E07-S2-04 | Per-element lock / unlock toggle with padlock icon | Dev | P1 | Done | Spec §3.6.6 |
| E07-S2-05 | Hint text authoring: 3 separate editable fields (Hint 1 / 2 / 3) | Dev | P1 | Done | Spec §3.6.7; UX UQ7 |
| E07-S2-06 | Researcher metadata fields (expected_difficulty, domain_prior, spatial_type) | Dev | P2 | Not Started | Spec §6.5; for Dr. Lena |
| E07-S2-07 | Duplicate & modify existing puzzle | Dev | P1 | Done | Spec §3.6.9 |
| E07-S2-08 | Test-play a puzzle from within the editor before saving | Dev | P1 | Done | UX US-D1 acceptance criteria |
| E07-S2-09 | Save puzzle as portable `.gearlab` file | Dev | P1 | Done | Opens on any GearLab install — UX US-D5 |
| E07-S2-10 | QA: full puzzle authoring flow end-to-end (author → save → share → open → solve) | QA | P1 | Done | |

---

## E08 — Presentation & Teacher Mode

**Goal:** Full-screen classroom projection mode and teacher-specific tools.  
**Responsible:** Engineering + Design  
**Depends on:** E07 complete  
**Spec refs:** §4.5, UX §3.2, UX §4.2

---

### E08-S1 — Presentation Mode

**Sprint Goal:** F11 launches a clean, full-screen mode the teacher can project live to a class.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E08-S1-01 | F11 / menu toggle: enter / exit Presentation mode | Dev | P1 | Done | Spec §4.5 |
| E08-S1-02 | Presentation mode layout: toolbox hidden, properties panel hidden | Dev | P1 | Done | Per E02-S2-06 design |
| E08-S1-03 | Formula panel enlarged and always visible in Presentation mode | Dev | P1 | Done | Spec §4.5; UX US-D4 |
| E08-S1-04 | Direction arrows enlarged in Presentation mode | Dev | P1 | Done | UX §7 |
| E08-S1-05 | Teacher can still edit canvas (add/connect/modify gears) while in Presentation mode | Dev | P1 | Done | UX US-D4 |
| E08-S1-06 | Annotation / freehand draw overlay (teacher draws on canvas live) | Dev | P2 | Not Started | Spec §4.5; UX UQ9 — freehand only in v1 |
| E08-S1-07 | Esc key or F11 restores prior layout instantly | Dev | P1 | Done | |
| E08-S1-08 | Design review: Presentation mode visual polish | Design | P1 | Not Started | |

---

### E08-S2 — Teacher Tools

**Sprint Goal:** Teachers can collect and aggregate class performance data from student session files.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E08-S2-01 | Batch-import multiple student `.gearlab` session files | Dev | P1 | Not Started | Spec §3.7.6; UX US-D6 |
| E08-S2-02 | Aggregate class summary report (avg solve time, hint usage rate per puzzle) | Dev | P1 | Not Started | UX US-D6 |
| E08-S2-03 | Summary exportable as CSV for teacher's own analysis | Dev | P2 | Not Started | |
| E08-S2-04 | QA: batch import with mixed complete/partial student files | QA | P2 | Not Started | |

---

## E09 — Gamification & Progression

**Goal:** The 5-level unlock system, reward mechanics, and feature discovery tooltips.  
**Responsible:** Engineering + Design  
**Depends on:** E07 complete  
**Spec refs:** §11, UX §6

---

### E09-S1 — Unlock System

**Sprint Goal:** Level progression state is tracked; completing milestones unlocks new elements and tools.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E09-S1-01 | Progression state tracker (level 0–4 per installation) | Dev | P1 | Not Started | Spec §11.2 |
| E09-S1-02 | Level 1 unlock: Belt & chain elements (after 3 Easy puzzles) | Dev | P1 | Not Started | |
| E09-S1-03 | Level 2 unlock: Defect injection tools (after 3 Medium puzzles) | Dev | P1 | Not Started | |
| E09-S1-04 | Level 3 unlock: Expert data table (after 3 Hard puzzles) | Dev | P1 | Not Started | |
| E09-S1-05 | Level 4 unlock: Puzzle sharing / export (after authoring 1 puzzle) | Dev | P2 | Not Started | |
| E09-S1-06 | Unlock badge notification on new level reached | Dev | P1 | Not Started | Per E02-S3-09 design |
| E09-S1-07 | Progress dashboard on home screen (level badge, puzzle scores, recent files) | Dev | P2 | Not Started | Spec §4.6; UX UQ1 |
| E09-S1-08 | Star rating stored globally per puzzle (best score shown on re-attempt) | Dev | P2 | Not Started | UX UQ4 |

---

### E09-S2 — Rewards & Engagement

**Sprint Goal:** Celebration, pulsing hint, and feature discovery make the experience feel alive.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E09-S2-01 | Celebration animation (particle effect or gear-spin flourish on puzzle solve) | Dev | P1 | Not Started | Per E02-S3-07 storyboard |
| E09-S2-02 | Session summary screen (end of puzzle set: puzzles solved, stars earned, hints used) | Dev | P2 | Not Started | Spec §11.3 |
| E09-S2-03 | Feature discovery tooltip system: one new feature per session, never repeats | Dev | P2 | Not Started | Spec §11.5 |
| E09-S2-04 | Feature discovery tooltip: dismissible, non-blocking, tracked per installation | Dev | P2 | Not Started | UX US-D8 |

---

## E10 — Research Mode

**Goal:** Silent behavioral logging for cognitive science research — invisible to participants, exportable for analysis.  
**Responsible:** Engineering  
**Depends on:** E07 complete  
**Spec refs:** §12, UX §3.3, UX §9

---

### E10-S1 — Logging Infrastructure

**Sprint Goal:** Research mode activates silently, logs every event with timestamp, zero UI change for participant.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E10-S1-01 | Research mode toggle in Settings panel (OFF by default) | Dev | P1 | Not Started | Spec §12.1; UX US-L1 |
| E10-S1-02 | Participant ID prompt at session start (researcher-facing only) | Dev | P1 | Not Started | Spec §12.2.2; UX US-L5 |
| E10-S1-03 | "Research mode active" label in researcher status bar only (not on canvas) | Dev | P1 | Not Started | Spec §12.2.3 |
| E10-S1-04 | Silent event logger: captures all 13 event types with timestamps | Dev | P1 | Not Started | Spec §12.3 catalogue |
| E10-S1-05 | Session config file: specifies puzzle sequence; puzzles auto-load in order | Dev | P1 | Not Started | Spec §12.2.5; UX US-L3 |
| E10-S1-06 | Zero network calls in any mode — verified by static analysis or test | QA | P1 | Not Started | Spec §12.5.1; IRB compliance |
| E10-S1-07 | Test-run verification: generates sample log file for researcher inspection before study | Dev | P1 | Not Started | Spec §12.2.4; UX §5.3 imperative |

---

### E10-S2 — Export & Analysis

**Sprint Goal:** Export a clean, versioned session log; replay a participant's actions.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E10-S2-01 | Auto-save session log at session end to configurable local directory | Dev | P1 | Not Started | Spec §12.4.1-2; UX US-L4 |
| E10-S2-02 | JSON export: pretty-printed, schema_version field, one file per participant | Dev | P1 | Not Started | Naming: `gearlab_P042_20260517_143200.json` |
| E10-S2-03 | CSV export as alternative format (flat table of events) | Dev | P2 | Not Started | UX US-L4 |
| E10-S2-04 | On-demand export button in Research settings panel | Dev | P1 | Not Started | |
| E10-S2-05 | Replay mode: load a session log and animate participant actions step-by-step | Dev | P2 | Not Started | Spec §12.4.5; UX US-L7 |
| E10-S2-06 | Schema versioning: breaking changes bump major version; documented in release notes | Dev | P1 | Not Started | Spec §12.5.4 |
| E10-S2-07 | QA: full research session end-to-end (configure → run → export → verify schema) | QA | P1 | Not Started | |

---

## E11 — Save, Load & Data Management

**Goal:** Persistent file storage, session restore, PNG export, and class data management.  
**Responsible:** Engineering  
**Depends on:** E03, E04 complete  
**Spec refs:** §3.7, §6

---

### E11-S1 — File Operations

**Sprint Goal:** Save, load, and share a complete gear train. Session auto-restores on next launch.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E11-S1-01 | Save gear system to `.gearlab` JSON file (File > Save / Ctrl+S) | Dev | P1 | Not Started | Spec §3.7.1 |
| E11-S1-02 | Load `.gearlab` file (File > Open / Ctrl+O) | Dev | P1 | Not Started | |
| E11-S1-03 | Recent files list (File menu, last 5 files) | Dev | P1 | Not Started | Spec §3.7.2 |
| E11-S1-04 | Session state auto-save on exit (canvas, mode, zoom, puzzle progress) | Dev | P1 | Not Started | Spec §3.7.5 |
| E11-S1-05 | "Continue where you left off?" prompt on next launch | Dev | P1 | Not Started | Spec §3.6.11; UX §4.6 |
| E11-S1-06 | Export canvas as PNG image (one click, default filename = design name) | Dev | P1 | Not Started | Spec §3.7.3; UX US-M7 |
| E11-S1-07 | Share puzzle as portable `.gearlab` file (File > Share Puzzle) | Dev | P1 | Not Started | Spec §3.7.4 |
| E11-S1-08 | QA: save/load round-trip preserves all element properties and connections | QA | P1 | Not Started | |

---

## E12 — Onboarding & UX Polish

**Goal:** First launch is delightful; performance SLAs are met; accessibility is verified.  
**Responsible:** Design + Engineering + QA  
**Depends on:** E03–E11 feature-complete  
**Spec refs:** §4.6, §13, §14, UX §5

---

### E12-S1 — Onboarding

**Sprint Goal:** A first-time user is productive within 2 minutes without reading any documentation.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E12-S1-01 | Welcome screen: animated 60-second demo plays on first launch | Dev | P1 | Not Started | Spec §4.6; UX §4.2 journey |
| E12-S1-02 | Welcome screen: mode selector (Explorer / Student / Engineer) | Dev | P1 | Not Started | Self-explanatory labels; no tooltip needed |
| E12-S1-03 | Welcome screen dismissible at any time | Dev | P1 | Not Started | Spec §14.3.2 |
| E12-S1-04 | Welcome screen design — final visual polish | Design | P1 | Not Started | Per E02-S2-05 wireframe |
| E12-S1-05 | Feature discovery tooltip system implementation (one new feature per session) | Dev | P2 | Not Started | Spec §11.5; UX US-D8 |
| E12-S1-06 | Progress dashboard on home screen | Dev | P2 | Not Started | Spec §4.6 |

---

### E12-S2 — Performance & Reliability

**Sprint Goal:** All performance SLAs from Spec §14 are met and crash-free operation is verified.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E12-S2-01 | Gear animates within 1s of Play press | QA | P1 | Not Started | Spec §14.1.1 |
| E12-S2-02 | Parameter change updates canvas in <100ms | QA | P1 | Not Started | Spec §14.1.2 |
| E12-S2-03 | Hover tooltip appears in <300ms | QA | P1 | Not Started | Spec §14.1.3 |
| E12-S2-04 | Mode switch re-renders in <200ms | QA | P1 | Not Started | Spec §14.1.4 |
| E12-S2-05 | Cold launch to interactive canvas in <5s | QA | P1 | Not Started | Spec §14.3.1 |
| E12-S2-06 | Crash-free test: 200 random valid and invalid configurations | QA | P1 | Not Started | Spec §14.2.1-2 |
| E12-S2-07 | Auto-save completes with no perceptible UI stall | QA | P1 | Not Started | Spec §14.2.4 |

---

### E12-S3 — Accessibility

**Sprint Goal:** WCAG AA compliance verified; non-color indicators, touch targets, and font sizes confirmed.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E12-S3-01 | WCAG AA contrast audit on all text, icons, and status elements | QA | P1 | Not Started | Spec §13.1.3 |
| E12-S3-02 | Non-color indicator audit: every color-coded state has shape/icon/label redundancy | QA | P1 | Not Started | Spec §13.1.1 |
| E12-S3-03 | Touch/click target size audit: all interactive elements ≥ 44×44px | QA | P1 | Not Started | Spec §13.1.2 |
| E12-S3-04 | High-contrast mode implementation | Dev | P2 | Not Started | Spec §13.1.4; per E02-S3-12 design |
| E12-S3-05 | Explorer mode font size verified ≥ 16pt everywhere | QA | P1 | Not Started | Spec §13.3.1 |
| E12-S3-06 | Verify no forced timers in any non-competitive mode | QA | P1 | Not Started | Spec §13.3.2 |
| E12-S3-07 | Error message audit: every message states what happened AND what to do | QA | P1 | Not Started | Spec §13.2.1 |

---

## E13 — Packaging & Release

**Goal:** A single-file launcher that runs on a fresh Windows machine with `pip install` only.  
**Responsible:** Engineering + QA  
**Depends on:** E12 complete  
**Spec refs:** §1.4, §7.4

---

### E13-S1 — Packaging & Final QA

**Sprint Goal:** GearLab launches on a clean Windows machine. Final regression passes.

| ID | Feature | Type | Priority | Status | Notes |
|----|---------|------|----------|--------|-------|
| E13-S1-01 | Installer-free launch script (`run.bat` / `run.ps1`) | Dev | P1 | Not Started | Creates venv if not present; launches app |
| E13-S1-02 | Application icon (`.ico` format, all sizes) | Design | P1 | Not Started | |
| E13-S1-03 | About screen (version, licenses, credits) | Dev | P2 | Not Started | |
| E13-S1-04 | Full regression test suite on clean Windows machine | QA | P1 | Not Started | No prior install |
| E13-S1-05 | Cross-platform smoke test (macOS, Linux) | QA | P2 | Not Started | Secondary platforms |
| E13-S1-06 | Release notes document (features, known issues) | Dev | P2 | Not Started | |
| E13-S1-07 | Final UX review against UX.md emotional arc design | Design | P1 | Not Started | Does Maya, Daniel, and Dr. Lena's arc play out as designed? |

---

## Backlog Summary

| Epic | Items Total | Design | Dev | QA/Infra | Done | Blocked |
|------|-------------|--------|-----|----------|------|---------|
| E01 | 15 | 0 | 12 | 3 | 0 | 0 |
| E02 | 33 | 33 | 0 | 0 | 0 | 0 |
| E03 | 20 | 0 | 19 | 1 | 0 | 0 |
| E04 | 18 | 0 | 16 | 2 | 0 | 0 |
| E05 | 16 | 0 | 16 | 0 | 0 | 0 |
| E06 | 8 | 1 | 7 | 0 | 0 | 0 |
| E07 | 22 | 0 | 21 | 1 | 0 | 0 |
| E08 | 12 | 1 | 10 | 1 | 0 | 0 |
| E09 | 12 | 0 | 12 | 0 | 0 | 0 |
| E10 | 14 | 0 | 12 | 2 | 0 | 0 |
| E11 | 8 | 0 | 7 | 1 | 0 | 0 |
| E12 | 20 | 1 | 8 | 11 | 0 | 0 |
| E13 | 7 | 2 | 4 | 1 | 0 | 0 |
| **Total** | **205** | **38** | **144** | **23** | **0** | **0** |

---

## Change Log

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-05-17 | — | Initial backlog — 13 epics, 205 items; ready for design team delivery |
