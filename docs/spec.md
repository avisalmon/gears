# Product Specification — 0Mech Gear Simulator

**Status:** Draft  
**Version:** 0.2  
**Last Updated:** 2026-05-17  

---

## 1. Overview

### 1.1 Product Name
GearLab — Interactive Gear & Belt Simulator

### 1.2 Purpose
GearLab is an interactive Python desktop application for learning, visualizing, and experimenting with mechanical gear trains and belt/chain drive systems. Users place gears and belts on a canvas, configure their properties, and watch the system animate in real time. The tool serves multiple audiences — from young children discovering how gears mesh, to students solving ratio puzzles, to experienced mechanical designers calculating torque and speed across complex drive trains. Defect injection (missing teeth, worn profiles) makes it useful for diagnostics training as well.

### 1.3 Target Audience

| Level | Who | Primary Use |
|-------|-----|-------------|
| Beginner (Kids) | Ages 6–12 | Visual play, cause-and-effect, "what happens if I connect these?" |
| Intermediate (Students) | Ages 13–18 / hobbyists | Gear ratio calculation, belt routing, direction rules |
| Advanced (Engineers) | Mechanical designers, educators | Torque/speed analysis, defect simulation, custom parameters |
| Puzzle Player | Any age | Brain-teaser challenges, reverse-engineering target ratios |

### 1.4 Platform
Python 3.11+ desktop application, targeting Windows (primary), macOS and Linux (secondary). Single-file launch with no installer required.

---

## 2. Goals and Non-Goals

### 2.1 Goals
- 2.1.1 Real-time animated visualization of gear trains and belt/chain systems.
- 2.1.2 Intuitive drag-and-drop canvas where users build systems without coding.
- 2.1.3 Live calculation and display of gear ratios, output RPM, and rotation direction for every element.
- 2.1.4 Configurable gear parameters: tooth count, module/pitch, diameter, position, rotation direction, and defects.
- 2.1.5 Support for spur gears, rack-and-pinion, timing belts, and chain drives.
- 2.1.6 Defect simulation: missing teeth, chipped teeth, worn profiles — visually highlighted.
- 2.1.7 Multi-level UI that adapts complexity to the selected experience level.
- 2.1.8 Built-in puzzle/challenge mode with graded difficulty and hints.
- 2.1.9 Educational overlay layer: on-screen annotations explaining what is happening and why.
- 2.1.10 Save and load gear train configurations as files.

### 2.2 Non-Goals
- 2.2.1 Full 3D rendering or CAD-level output (e.g., STEP/DXF export) — out of scope for v1.
- 2.2.2 Structural stress / finite-element analysis.
- 2.2.3 Multi-axis / bevel gear simulation in v1.
- 2.2.4 Network or multiplayer features.

---

## 3. Features

### 3.1 Canvas and Interaction
- 3.1.1 Infinite zoomable/pannable 2D canvas for placing mechanical elements.
- 3.1.2 Drag-and-drop placement of gears, pulleys, and belt anchors.
- 3.1.3 Snap-to-mesh: when a gear is dragged near another, it snaps to the correct center distance automatically.
- 3.1.4 Click-to-select any element; selected element shows a properties panel.
- 3.1.5 Delete, duplicate, and undo/redo for all canvas operations.
- 3.1.6 A "driver" gear that is the input — user sets its RPM and direction; everything else is calculated.

### 3.2 Gear Parameters (per gear)
- 3.2.1 Number of teeth (integer, e.g., 8–200).
- 3.2.2 Module / pitch (determines physical diameter from tooth count).
- 3.2.3 Visual diameter and tooth profile drawn accurately to scale.
- 3.2.4 Rotation direction (shown as animated arrow overlay).
- 3.2.5 RPM — calculated automatically from driver; optionally user can set a constraint to back-calculate.
- 3.2.6 Gear type: spur (standard), internal ring gear, or rack segment.
- 3.2.7 Defect injection per individual tooth: missing, chipped, or worn (visual + effect on simulation).

### 3.3 Belt and Chain Features
- 3.3.1 Timing belt / synchronous belt connecting two or more pulleys.
- 3.3.2 Chain drive (roller chain) as an alternative to belt.
- 3.3.3 Belt path drawn automatically around connected pulleys; crossed belt option for direction reversal.
- 3.3.4 Belt ratio calculated from pulley tooth/sprocket counts.
- 3.3.5 Visual tension indicator — belt shown taut, slack, or snapped (if parameters are invalid).

### 3.4 Simulation and Animation
- 3.4.1 Real-time animated rotation of all elements at correct relative speeds.
- 3.4.2 Animation speed control: slow-motion to fast-forward.
- 3.4.3 Pause / step-frame mode for close inspection.
- 3.4.4 When a defective tooth engages, a visual "jolt" or highlight event fires.
- 3.4.5 Color-coded rotation direction: e.g., clockwise = blue, counterclockwise = red.

### 3.5 Educational Overlay
- 3.5.1 Gear ratio badge shown on every gear (relative to driver).
- 3.5.2 "Why?" tooltip — hover over any gear for a plain-language explanation of its ratio.
- 3.5.3 Formula panel: shows the live gear ratio formula as user modifies tooth counts.
- 3.5.4 Direction rule explainer: animated arrows showing how meshing reverses direction.
- 3.5.5 Belt vs. gear comparison mode: side-by-side showing same ratio achieved two ways.
- 3.5.6 Beginner mode: large labels, simplified language, emoji-style indicators.
- 3.5.7 Expert mode: numerical table of all elements (tooth count, module, center distance, ratio, RPM, tangential velocity).

### 3.6 Puzzle / Challenge Mode
- 3.6.1 Pre-built puzzle library with difficulty levels: Easy, Medium, Hard, Expert.
- 3.6.2 Goal-based challenges — examples:
  - "Make the output gear spin exactly 3× faster than the input."
  - "Find the broken gear causing the jitter."
  - "Connect A to B using only belts so both spin the same direction."
  - "Achieve a 1:5 reduction using exactly 3 gears."
- 3.6.3 Hint system: 3 levels of hints per puzzle, each revealing a bit more.
- 3.6.4 Score and star rating based on efficiency (fewest gears, fewest steps).
- 3.6.5 Custom challenge editor: user can author and save their own puzzles.
- 3.6.6 Puzzle elements can be individually locked (immovable by the solver); locked elements display a padlock icon.
- 3.6.7 Hint text is authored per-puzzle by the creator — not auto-generated; each of the 3 hint levels is a separate editable text field.
- 3.6.8 Puzzle editor provides a guided "first puzzle" template so a new author can create and save a complete puzzle in ≤10 minutes.
- 3.6.9 An existing puzzle can be duplicated and modified in the editor — to produce a harder or easier variant without starting from scratch.
- 3.6.10 After 5 consecutive failed solve attempts on the same puzzle, a single "nudge" animation plays showing one correct partial step (without revealing the full solution).
- 3.6.11 Puzzle progress is auto-saved; on next launch the tool offers "Continue where you left off" for any incomplete puzzle.

### 3.7 Save / Load / Export
- 3.7.1 Save gear train as a `.gearlab` JSON file.
- 3.7.2 Load saved files; recent files list.
- 3.7.3 Export canvas as PNG image (static snapshot); default filename is the design name.
- 3.7.4 Share puzzle as a self-contained file that another user can open and solve.
- 3.7.5 Session state (current canvas, mode, puzzle progress) is auto-saved on exit and restored on next launch.
- 3.7.6 A teacher can batch-import multiple student session files and generate an aggregated class performance summary (average solve time, hint usage rate per puzzle).

---

## 4. User Interface

### 4.1 Main Layout
```
┌──────────────────────────────────────────────────────────────┐
│  Menu Bar: File | Edit | View | Mode | Help                  │
├────────────┬─────────────────────────────────┬───────────────┤
│            │                                 │               │
│  Toolbox   │        Canvas (main area)        │  Properties   │
│  (left)    │        zoomable / pannable       │  Panel        │
│            │                                 │  (right)      │
│  - Gears   │                                 │               │
│  - Belts   │                                 │  Selected     │
│  - Rack    │                                 │  element      │
│  - Chain   │                                 │  parameters   │
│            │                                 │               │
├────────────┴─────────────────────────────────┴───────────────┤
│  Status Bar: Ratio | Output RPM | Mode | Zoom level          │
└──────────────────────────────────────────────────────────────┘
```

### 4.2 Experience Level Selector
A persistent mode switcher (top ribbon or settings):
- **Explorer** (kids): large icons, animation-first, minimal numbers, fun colors.
- **Student**: gear ratio formulas visible, moderate detail.
- **Engineer**: full numerical table, defect controls, all parameters unlocked.
- **Puzzle**: hides parameters, shows only the challenge goal.

### 4.3 Properties Panel (right side)
Shows for the selected element:
- Tooth count (slider + numeric input)
- Module / pitch
- Defect controls (per-tooth toggle grid for missing/chipped)
- Current calculated RPM and ratio
- Rotation direction indicator

### 4.4 Animation Controls (bottom toolbar)
Play | Pause | Step | Speed slider (0.1× – 10×) | Reset

### 4.5 Presentation Mode
A dedicated full-screen mode for classroom projection, activated by pressing F11 or via the View menu:
- Toolbox panel hidden.
- Properties panel hidden.
- Formula panel always visible and prominently sized.
- Direction arrows enlarged.
- Ratio badges shown in large type.
- All developer/debug chrome removed.
- A live canvas the teacher can interact with (add, connect, and modify gears) while students watch.
- An optional annotation overlay: teacher can draw freehand lines or arrows on the canvas to highlight elements during explanation.
- Exiting Presentation mode (Esc or F11) restores the previous layout instantly.

### 4.6 Onboarding & Session State

**Welcome Screen (first launch only):**
- Animated 60-second demo plays automatically showing a gear being placed, meshed, and animated.
- Mode selector (Explorer / Student / Engineer) presented prominently before entering the canvas.
- Mode names are self-explanatory without any supplementary text.

**Progressive Feature Discovery:**
- In-context tooltip bubbles introduce one previously unseen feature per session.
- Each bubble is dismissible; dismissed bubbles never reappear.
- All features are surfaced this way over time — no manual to read.

**Session State Restoration:**
- On every exit, the full canvas state (elements, connections, mode, zoom level) is saved automatically.
- On next launch: "Continue where you left off?" is offered. User can accept or start fresh.
- Progress dashboard on the home screen shows: recent files, last-opened puzzle, best star rating per puzzle.

---

## 5. Simulation Engine

### 5.1 Supported Mechanical Elements
- 5.1.1 **Spur gear** — standard external meshing gear.
- 5.1.2 **Internal (ring) gear** — gear meshes inside a ring; output same direction as input.
- 5.1.3 **Rack and pinion** — rotary to linear translation.
- 5.1.4 **Timing belt / synchronous pulley** — positive-engagement belt drive.
- 5.1.5 **Chain and sprocket** — roller-chain drive.
- 5.1.6 **Idler gear** — direction-reversing or tensioning intermediate gear (no ratio change).

### 5.2 Kinematic Rules
- 5.2.1 **Gear ratio**: `ratio = N_driven / N_driver` where N = tooth count.
- 5.2.2 **Output RPM**: `RPM_out = RPM_in × (N_driver / N_driven)`.
- 5.2.3 **Direction**: each external mesh reverses direction; internal mesh preserves direction; belt/chain preserves direction (uncrossed) or reverses (crossed).
- 5.2.4 **Center distance**: `C = (d1 + d2) / 2` where `d = N × module`; enforced by snap-to-mesh.
- 5.2.5 **Belt length**: calculated from pulley diameters and center distance; displayed in properties.
- 5.2.6 **Gear train chains**: the engine propagates ratio and direction from the driver through every connected element in dependency order (BFS traversal of the gear graph).

### 5.3 Defect Simulation
- 5.3.1 A missing tooth causes the driven gear to slip one pitch per revolution at that angular position.
- 5.3.2 Slip events are flagged visually (flash highlight) and logged in an event timeline.
- 5.3.3 Worn tooth reduces effective contact and is shown as a dimmed/eroded tooth profile.
- 5.3.4 Defects can be hidden in Puzzle mode so the user must discover them.

### 5.4 Validation and Error States
- 5.4.1 Gears that do not mesh (center distance mismatch) shown in orange with an error badge.
- 5.4.2 Circular/impossible gear loops detected and flagged.
- 5.4.3 Belt length too short or too long shown with a tension color indicator.
- 5.4.4 All error states are non-blocking and graceful — the application never crashes on any valid or invalid user-constructed configuration.
- 5.4.5 Every error message states both what went wrong and one concrete action the user can take to fix it. A message that only says what is wrong (without a suggested fix) is not acceptable.

---

## 6. Data Model

### 6.1 Gear Object
```
Gear {
  id: UUID
  type: spur | ring | rack | pulley | sprocket | idler
  tooth_count: int
  module: float          // determines diameter
  position: (x, y)       // canvas coordinates
  is_driver: bool
  rpm: float             // calculated; editable only for driver
  defects: [ToothDefect] // list of per-tooth defect records
}
```

### 6.2 ToothDefect Object
```
ToothDefect {
  tooth_index: int       // 0-based index around the gear
  defect_type: missing | chipped | worn
}
```

### 6.3 Connection Object
```
Connection {
  id: UUID
  type: mesh | belt | chain | rack
  element_a: Gear.id
  element_b: Gear.id
  crossed: bool          // for belts — crosses = direction reversal
}
```

### 6.4 System State
```
GearSystem {
  elements: [Gear]
  connections: [Connection]
  driver_rpm: float
  driver_direction: CW | CCW
}
```

### 6.5 Puzzle File Format
```
PuzzleFile {
  title: string
  description: string
  difficulty: easy | medium | hard | expert
  initial_state: GearSystem   // locked elements
  goal: GoalSpec              // what the player must achieve
  hints: [string]             // ordered, most vague to most specific
  locked_element_ids: [UUID]  // elements the solver cannot move or delete
  // Optional researcher metadata (ignored by non-research builds)
  research: {
    expected_difficulty_rating: float   // 1.0–10.0 researcher-assigned
    domain_prior_required: bool         // true if mechanical background needed
    spatial_reasoning_type: string      // e.g. "ratio", "direction", "defect"
    cognitive_load_notes: string        // free-text annotation
  }
}
```

### 6.6 Session Log File Format
```
SessionLog {
  schema_version: "1.0"
  participant_id: string       // researcher-assigned code; no personal data
  session_id: UUID
  events: [EventRecord]        // ordered list of all logged actions
}

EventRecord {
  timestamp_ms: int            // milliseconds since session_start
  event_type: string           // see Section 12.2 for event type catalogue
  puzzle_id: string | null
  payload: object              // event-specific fields
}
```

---

## 7. Technology Stack

### 7.1 Language
Python 3.11+

### 7.2 GUI Framework
**PyQt6** — chosen for smooth canvas rendering, rich widget set, and cross-platform support. The main canvas uses `QGraphicsScene` / `QGraphicsView` for hardware-accelerated 2D rendering and animation.

### 7.3 Core Libraries
| Library | Purpose |
|---------|---------|
| PyQt6 | GUI framework, canvas, animation |
| NumPy | Gear tooth profile geometry calculations |
| json | Save/load `.gearlab` files |
| Pillow | PNG export |

### 7.4 No-dependency constraint
The tool must run with `pip install pyqt6 numpy pillow` only. No heavy simulation frameworks.

---

## 8. Development Milestones

| ID | Milestone | Description | Status |
|----|-----------|-------------|--------|
| M1 | Project scaffold | Repo structure, venv, main window shell, empty canvas | Not started |
| M2 | Gear rendering | Draw a single spur gear from tooth count + module; animate rotation | Not started |
| M3 | Gear meshing | Place two gears, snap-to-mesh, propagate ratio and direction | Not started |
| M4 | Belt/chain | Add timing belt and chain connections between pulleys | Not started |
| M5 | Properties panel | Live-edit tooth count, module, defects; update canvas in real time | Not started |
| M6 | Defect simulation | Missing/chipped tooth injection with visual events | Not started |
| M7 | Educational overlay | Ratio badges, formula panel, tooltips, beginner/expert modes | Not started |
| M8 | Puzzle mode | Puzzle loader, goal checker, hint system, score display, locked elements, nudge animation | Not started |
| M9 | Save / load / export | `.gearlab` file format, PNG export, recent files, session state restore | Not started |
| M10 | Presentation mode | Full-screen F11 mode, annotation overlay, formula panel prominence | Not started |
| M11 | Gamification & progression | 5-level unlock system, celebration animation, pulsing hint button, feature discovery tooltips | Not started |
| M12 | Research mode | Silent event logging, participant ID, session config, export to JSON/CSV, replay mode | Not started |
| M13 | Teacher tools | Puzzle editor (guided template, duplicate, hint authoring), batch class summary import | Not started |
| M14 | Polish and packaging | Installer-free launcher, icon, onboarding screen, About screen, accessibility pass | Not started |

---

## 9. Open Questions

| ID | Question | Owner | Resolution |
|----|----------|-------|------------|
| Q1 | Should rack-and-pinion show linear translation animation (moving rack) in v1? | — | — |
| Q2 | What is the target minimum screen resolution? | — | — |
| Q3 | Should puzzles have a timer / competitive mode? (UX.md UQ3) | — | — |
| Q4 | Do we need localization (Hebrew, etc.) for the UI strings? (UX.md UQ8) | — | — |
| Q5 | Should the tool support helical or bevel gears as a stretch goal? | — | — |
| Q6 | Is there a web/browser version desired in a future phase? | — | — |
| Q7 | Should Maya's 5-level progression be shown as a persistent progress bar, or milestone-only notifications? (UX.md UQ1) | — | — |
| Q8 | Should puzzle star ratings be stored globally so a student can see and beat their best score on re-attempts? (UX.md UQ4) | — | — |
| Q9 | Should the annotation draw layer in Presentation mode support text labels or freehand only? (UX.md UQ2) | — | — |
| Q10 | How should a partial session log be handled if a participant quits mid-puzzle in Research mode? (UX.md UQ3) | — | — |
| Q11 | Is a dual-monitor Research mode needed (researcher overlay on one screen; clean participant view on the other)? (UX.md UQ5) | — | — |

---

## 10. Change Log

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-05-17 | — | Initial skeleton |
| 0.2 | 2026-05-17 | — | Full spec draft based on product vision |
| 0.3 | 2026-05-17 | — | UX-derived requirements integrated: sections 11–14 added; sections 3.6, 3.7, 4, 5.4, 6 enriched; milestones expanded to M14 |

---

## 11. Gamification & Progression System

### 11.1 Design Basis
The progression system is built on **Self-Determination Theory (SDT)**:
- **Autonomy**: Free-build and puzzle modes are always available. No forced linear progression.
- **Competence**: Graduated difficulty and a 3-level hint system ensure every user can always move forward.
- **Relatedness**: Sharing designs and puzzles creates social connection even within a single-player desktop tool.

### 11.2 Progression Levels

| Level | Name | Unlock Condition | What Is Unlocked |
|-------|------|-----------------|------------------|
| 0 | Explorer | Default (no requirement) | Spur gears, free-build canvas |
| 1 | Apprentice | Complete 3 Easy puzzles | Belt and chain elements |
| 2 | Mechanic | Complete 3 Medium puzzles | Defect injection tools |
| 3 | Engineer | Complete 3 Hard puzzles | Expert data table (RPM, velocity) |
| 4 | Inventor | Author and save 1 custom puzzle | Puzzle sharing / export |

### 11.3 Reward Mechanics

| Mechanic | Trigger | Purpose |
|----------|---------|---------|
| Star rating (1–3★) | Puzzle solved | Mastery signal; motivates replay with fewer hints |
| Celebration animation | Puzzle solved correctly | Emotional reward at the peak of the arc |
| Unlock badge notification | First use of a newly unlocked element type | Feature discovery nudge |
| Ratio badge on every gear | Any gear connected to driver | Immediate kinematic feedback for all users |
| Puzzle authored badge | First custom puzzle saved | Creator recognition for teacher / advanced user |
| Session summary | End of a puzzle set | Reflection and progress visibility |

### 11.4 Anti-Frustration Rules

| Trigger | System Response |
|---------|-----------------|
| User stuck on same puzzle > 3 minutes | Hint button begins a subtle pulsing animation (visible but not intrusive) |
| Wrong gear configuration placed | Gear glows orange; tooltip states what is wrong and one way to fix it |
| 5 consecutive failed solve attempts | A single "nudge" animation plays showing one correct partial step only |
| User closes app mid-puzzle | Canvas and puzzle state auto-saved; next launch offers "Continue where you left off" |

### 11.5 Feature Discovery Tooltip System
- One in-context tooltip bubble introduces a previously unseen feature per session.
- Tooltips are non-blocking and dismissible.
- Once dismissed, a tooltip never reappears.
- The system tracks which features have been introduced per installation and cycles through the full feature set before repeating none.

---

## 12. Research Mode

### 12.1 Overview
Research mode is an optional, **off-by-default** behavioral logging layer designed for cognitive science and educational research. When active, it silently records every user interaction with full timestamps. It produces no visible UI changes for the participant.

### 12.2 Activation & Configuration
- 12.2.1 Research mode is enabled via a `research.json` configuration file or via a Settings panel (researcher-accessible).
- 12.2.2 When Research mode starts, the tool prompts the researcher (not the participant) for a Participant ID.
- 12.2.3 A "Research mode active" indicator is shown on the researcher's screen only (e.g., a status bar label); it is never shown on the participant's canvas.
- 12.2.4 A **test-run verification** option generates a sample session log the researcher can inspect before the real study begins. This confirms that logging is working correctly.
- 12.2.5 A session config file specifies the puzzle sequence; puzzles load automatically in the defined order without any participant navigation.

### 12.3 Event Log Catalogue

All events share the same envelope:
```json
{
  "schema_version": "1.0",
  "participant_id": "P042",
  "session_id": "uuid",
  "puzzle_id": "gear_ratio_medium_07",
  "timestamp_ms": 12345678,
  "event_type": "...",
  "payload": {}
}
```

| Event Type | Key Payload Fields |
|------------|--------------------|
| `session_start` | participant_id, mode, puzzle_sequence |
| `puzzle_opened` | puzzle_id, difficulty |
| `gear_placed` | gear_id, type, tooth_count, position |
| `gear_moved` | gear_id, from_position, to_position |
| `gear_deleted` | gear_id |
| `connection_made` | connection_type, element_a, element_b |
| `parameter_changed` | gear_id, field, old_value, new_value |
| `play_pressed` | current_system_state_snapshot |
| `hint_requested` | puzzle_id, hint_level (1/2/3), time_since_puzzle_open_ms |
| `solve_attempted` | current_system_state_snapshot, is_correct |
| `puzzle_solved` | puzzle_id, solve_time_ms, hints_used, attempts |
| `undo_pressed` | action_undone |
| `session_end` | total_puzzles_attempted, total_puzzles_solved, total_hints_used |

### 12.4 Data Export
- 12.4.1 One JSON file per participant per session. Naming convention: `gearlab_P042_20260517_143200.json`.
- 12.4.2 Auto-saved to a configurable local directory at session end.
- 12.4.3 Human-readable pretty-printed JSON (not minified). Schema version field present in every file.
- 12.4.4 Export is also available on demand via a button in the Research settings panel.
- 12.4.5 Replay mode: a researcher can load a session log file and GearLab will animate the participant's action sequence step-by-step.

### 12.5 Privacy & Compliance
- 12.5.1 **Zero network calls** in any mode. No telemetry. All logs written only to local disk.
- 12.5.2 Participant IDs are researcher-assigned anonymous codes. No names, emails, or personal identifiers are stored.
- 12.5.3 Research mode is `OFF` by default. It must be explicitly enabled before a session.
- 12.5.4 The log file schema is published in the project documentation and is versioned. Schema-breaking changes increment the major version number.

---

## 13. Accessibility Requirements

### 13.1 Visual Accessibility
- 13.1.1 All color-coded states (rotation direction, error, belt tension) have a redundant non-color indicator: shape, label, or icon. No state is communicated by color alone.
- 13.1.2 All interactive elements have a minimum clickable target size of 44 × 44 px.
- 13.1.3 All gear outlines, labels, and status text pass WCAG AA contrast ratio (4.5:1 for normal text, 3:1 for large text).
- 13.1.4 A high-contrast mode is available in Settings.
- 13.1.5 Tooth count and gear ratio values are always displayed as text; they are never communicated by color or position alone.

### 13.2 Cognitive Accessibility
- 13.2.1 Error messages always contain two parts: (1) what happened, and (2) one concrete suggested action. Messages that only state a problem without a remedy are not acceptable.
- 13.2.2 A maximum of one animated element is used per contextual hint or tooltip at a time.
- 13.2.3 All animation can be paused or reduced to slow-motion globally without any loss of information.

### 13.3 Age-Range Considerations
- 13.3.1 Explorer mode minimum font size: 16pt. All labels use simple vocabulary (no jargon).
- 13.3.2 No timed pressure exists in any mode unless explicitly opted into (puzzle timer is opt-in only, never forced).

---

## 14. Performance & Reliability Requirements

### 14.1 Responsiveness
- 14.1.1 A single gear placed on the canvas begins animating within **1 second** of pressing Play with no prior setup.
- 14.1.2 A change to a gear's tooth count (via slider or input) must recalculate the entire gear train and update all visual elements in under **100 ms**.
- 14.1.3 A tooltip triggered by hovering over a gear must appear within **300 ms**.
- 14.1.4 Mode switching (e.g., Student → Explorer) must re-render the full UI in under **200 ms**.

### 14.2 Reliability
- 14.2.1 The application must not crash on any user-constructed gear configuration, valid or invalid.
- 14.2.2 Invalid configurations produce a visible, friendly error state — they never cause an exception or freeze.
- 14.2.3 Undo/redo must be available at all times during a free-build session. There is no maximum undo depth in normal operation.
- 14.2.4 Session state auto-save (see 3.7.5) must complete in the background without any perceptible UI stall.

### 14.3 Startup
- 14.3.1 Cold launch to interactive canvas in under **5 seconds** on a mid-range Windows PC.
- 14.3.2 The welcome screen animation must not block interaction; the user can dismiss it at any time.
