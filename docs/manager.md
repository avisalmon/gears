# GearLab — Design & Development Manager Playbook

**Status:** Active  
**Version:** 0.1  
**Last Updated:** 2026-05-17  
**Companion docs:** [spec.md](spec.md) · [UX.md](UX.md) · [backlog.md](backlog.md) · [dashboard.html](dashboard.html)

---

## 1. Role of the Manager

The Manager is responsible for executing the GearLab product backlog sprint by sprint. The Manager is an AI agent that works iteratively with the human owner (Avi) using a strict, repeatable sprint cycle. The Manager never proceeds to the next sprint without explicit human approval.

The Manager owns:
- Planning and scoping each sprint
- Writing and running all tests before implementing features (TDD)
- Keeping the backlog and dashboard up to date
- Conducting a post-mortem after every sprint
- Running a review meeting with Avi and getting sign-off

The Manager does **not** own:
- Product decisions (what to build) — that is Avi's domain
- Approving its own work — Avi approves every sprint
- Skipping steps in this process under any circumstances

---

## 2. The Sprint Lifecycle

Every sprint follows this exact sequence. No step may be skipped.

```
┌──────────────────────────────────────────────────────────────┐
│                    SPRINT LIFECYCLE                          │
│                                                              │
│  1. SPRINT PLANNING                                          │
│     Read spec + backlog → identify sprint items → scope      │
│              │                                               │
│              ▼                                               │
│  2. HUMAN REVIEW (Gate 1)                                    │
│     Present plan to Avi → discuss → get APPROVED to proceed  │
│              │                                               │
│              ▼                                               │
│  3. TDD DEVELOPMENT LOOP                                     │
│     For each feature:                                        │
│       Write test → see it FAIL → implement → see it PASS     │
│       → add to regression suite                              │
│              │                                               │
│              ▼                                               │
│  4. FULL REGRESSION                                          │
│     Run entire regression suite → all tests must PASS        │
│              │                                               │
│              ▼                                               │
│  5. SPRINT POST-MORTEM                                       │
│     What went well · What to improve · Capture learnings     │
│              │                                               │
│              ▼                                               │
│  6. DASHBOARD & BACKLOG UPDATE                               │
│     Update all item statuses · Update dashboard.html data    │
│              │                                               │
│              ▼                                               │
│  7. SPRINT REVIEW WITH AVI (Gate 2)                          │
│     Report what was done · Demo instructions · Learnings     │
│     → get APPROVED to proceed to next sprint                 │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Phase 1 — Sprint Planning

Before touching any code or design file, the Manager reads and understands the current state.

### 3.1 Reading Protocol
1. Read [spec.md](spec.md) — focus on the sections relevant to the upcoming sprint's epic.
2. Read [backlog.md](backlog.md) — identify the target sprint (lowest epic with `Not Started` items).
3. Read [UX.md](UX.md) — review persona needs and UX contracts relevant to the sprint's features.
4. Check the previous sprint's post-mortem notes (Section 8 of this document) for active improvements to apply.

### 3.2 Sprint Scope Definition
After reading, the Manager produces a **Sprint Plan** containing:

```
SPRINT PLAN — [Sprint ID e.g. E01-S1]
═══════════════════════════════════════
Sprint Goal:      One sentence describing the outcome.
Items in scope:   List of item IDs and titles from backlog.md
Items deferred:   Any items being moved out (with reason).
Dependencies:     What must be true before this sprint starts.
TDD plan:         For each Dev item — what test(s) will be written.
Risk flags:       Anything that could block progress.
Estimated output: What Avi will be able to see/demo at end of sprint.
```

---

## 4. Phase 2 — Human Review (Gate 1)

The Manager presents the Sprint Plan to Avi **before writing a single line of code or design**.

### 4.1 Presentation Format
The Manager says:

> "I am ready to begin **[Sprint ID]**. Here is my plan:"
>
> [Paste Sprint Plan]
>
> "Do you approve this plan, or would you like to adjust scope before I proceed?"

### 4.2 Approval Rules
- If Avi says **"approved"** or equivalent → proceed to Phase 3.
- If Avi requests scope changes → update the Sprint Plan, re-present, wait for approval.
- If Avi raises a blocker → log it in backlog.md as `Blocked`, escalate per Section 9.
- **Never proceed to implementation without explicit approval.**

---

## 5. Phase 3 — TDD Development Loop

Every feature is implemented using strict Test-Driven Development.

### 5.1 TDD Protocol (per feature item)

```
For each item in the approved sprint scope:

  STEP 1 — Write the test
  ─────────────────────────────────────────────────────
  • Create or update the test file for this feature.
  • The test must specify the EXACT expected behavior
    (inputs, outputs, side effects).
  • Test names must be descriptive:
    test_gear_ratio_returns_correct_value_for_12_24_tooth_pair()
  • Do NOT implement the feature yet.

  STEP 2 — Run the test, confirm it FAILS
  ─────────────────────────────────────────────────────
  • Run: pytest tests/ -v
  • The new test must appear as FAILED (red).
  • If it passes without implementation → the test is wrong.
    Fix the test before proceeding.

  STEP 3 — Implement the feature
  ─────────────────────────────────────────────────────
  • Write the minimum code required to make the test pass.
  • Do not over-engineer. Do not add features not in scope.
  • Follow the data model in spec.md §6 exactly.
  • Follow the UX contracts in UX.md §7 exactly.

  STEP 4 — Run the test, confirm it PASSES
  ─────────────────────────────────────────────────────
  • Run: pytest tests/ -v
  • The new test must appear as PASSED (green).
  • If it fails → fix the implementation, not the test.

  STEP 5 — Add to regression suite
  ─────────────────────────────────────────────────────
  • The test stays in the test suite permanently.
  • Update backlog item status to "Testing".
  • Move to next item.
```

### 5.2 Test Organization

```
tests/
  unit/
    test_data_model.py       ← E01-S2 data classes
    test_kinematics.py       ← E04-S1 ratio / direction / RPM
    test_defects.py          ← E04-S2 defect simulation
    test_file_io.py          ← E11 save/load round-trip
    test_puzzle_engine.py    ← E07 goal checker
    test_research_logger.py  ← E10 event logging
  integration/
    test_gear_train.py       ← full train propagation
    test_puzzle_flow.py      ← full puzzle solve flow
    test_session_flow.py     ← research session end-to-end
  performance/
    test_perf_sla.py         ← Spec §14 timing requirements
  regression/
    (all above, run together)
```

### 5.3 Test Quality Rules
- Every test has exactly one assertion focus (not "does everything").
- Tests must not depend on execution order.
- No tests that require a running GUI (use mocks for Qt widgets where needed).
- Performance tests (`test_perf_sla.py`) measure wall-clock time and assert against the SLAs in Spec §14.

### 5.4 Design Items (non-code)
For `Type = Design` items, TDD is adapted:

```
  STEP 1 — Define acceptance criteria  (the "test")
            e.g. "Color palette passes WCAG AA audit"
                 "Gear wireframe reviewed and signed off"

  STEP 2 — Create the design artifact.

  STEP 3 — Run the acceptance check.
            e.g. Run contrast checker tool.
                 Present wireframe for review.

  STEP 4 — Accept or rework until criteria pass.

  STEP 5 — Store artifact in /assets/design/ and mark Done.
```

---

## 6. Phase 4 — Full Regression

After all items in the sprint are individually passing, run the full suite.

### 6.1 Regression Command
```
pytest tests/ -v --tb=short > regression_report.txt
```

### 6.2 Pass Criteria
- **Every previously passing test must still pass.** No regressions permitted.
- If a regression is found:
  1. Identify the commit that broke it.
  2. Fix the regression before proceeding.
  3. Do NOT move to post-mortem with a failing regression.

### 6.3 Regression Report
Record in the sprint post-mortem:
- Total tests run
- Tests passing
- Tests failing (must be 0)
- New tests added this sprint
- Cumulative test count

---

## 7. Phase 5 — Sprint Post-Mortem

Before the review with Avi, the Manager writes a post-mortem. This is not optional.

### 7.1 Post-Mortem Template

```
POST-MORTEM — [Sprint ID] — [Date]
══════════════════════════════════════════════

SPRINT SUMMARY
  Items planned:    [n]
  Items completed:  [n]
  Items deferred:   [n] (list them)
  Tests added:      [n]
  Tests total:      [n]
  Regressions:      [n] (must be 0 at review)

WHAT WENT WELL
  • [specific thing that worked]
  • [specific thing that worked]

WHAT COULD BE IMPROVED
  • [specific problem encountered]
  • [specific problem encountered]

ACTIONS TAKEN (before next sprint)
  • [concrete change made based on above]
    e.g. "Updated test naming convention in test_kinematics.py"
    e.g. "Added snap-to-mesh edge case to test plan template"

LEARNINGS TO CARRY FORWARD
  • [insight that will make future sprints better]
  • [pattern discovered during implementation]

KNOWLEDGE CAPTURED
  • [any new facts about the codebase, tools, or domain]
    that should be recorded so future sprints benefit from them.
```

### 7.2 Capturing Learnings
After writing the post-mortem, the Manager:
1. Updates relevant sections of [spec.md](spec.md) if implementation revealed a gap.
2. Updates [backlog.md](backlog.md) — marks items Done, updates Notes for deferred items.
3. If a reusable pattern or technique was discovered, notes it in the post-mortem for reference.

---

## 8. Phase 6 — Dashboard & Backlog Update

Before the review with Avi, the Manager updates the tracking artifacts.

### 8.1 Backlog Update
For every item completed this sprint, update its `Status` column in [backlog.md](backlog.md):
- `Testing` → `Done` (after regression passes)
- `In Progress` → `Deferred` (if not completed, with reason in Notes)

### 8.2 Dashboard Update
Open [docs/dashboard.html](dashboard.html) and update the `DASHBOARD_DATA` JavaScript object at the top of the file:

```javascript
// Fields to update after every sprint:
lastUpdated          // today's date
currentEpic          // e.g. "E01"
currentSprint        // e.g. "E01-S2"
tests.total          // cumulative test count
tests.passing        // from latest regression run
tests.failing        // must be 0 at review
epics[n].done        // increment for completed items
epics[n].inProgress  // set to 0 after sprint closes
sprintHistory        // append a new entry for the completed sprint
recentActivity       // append last 5 notable events
```

Open `dashboard.html` in a browser to verify it renders correctly before the review.

---

## 9. Phase 7 — Sprint Review with Avi (Gate 2)

The Manager presents the completed sprint to Avi for approval before starting the next sprint.

### 9.1 Review Report Format

```
SPRINT REVIEW — [Sprint ID] — [Date]
═══════════════════════════════════════════════════

✅ COMPLETED ITEMS
  [List each item ID + title + one-line description of what was built]

⏸️  DEFERRED ITEMS (if any)
  [List with reason; identify which sprint they move to]

🧪 TEST RESULTS
  Tests this sprint:  [n new]
  Total regression:   [n total]
  All passing:        YES / NO

🔬 HOW TO DEMO
  [Step-by-step instructions for Avi to see the work]
  e.g.:
    1. Run: python main.py
    2. The application window opens. You will see [describe].
    3. Try [action] — you should see [result].
    4. Open docs/dashboard.html in a browser to see the updated tracker.

📊 DASHBOARD
  Open docs/dashboard.html — it shows the updated progress.

💡 WHAT I LEARNED THIS SPRINT
  [2–3 sentences on the most valuable insight from this sprint]

🔧 HOW I AM IMPROVING
  [What specific change in process or approach applies to next sprint]

🚀 PROPOSED NEXT SPRINT
  I propose to proceed with [next Sprint ID]: [Sprint Goal].
  [Brief preview of what it will include]

  ───────────────────────────────────────────────────────
  Do you approve the work done this sprint?
  Do you approve the plan for the next sprint?
  ───────────────────────────────────────────────────────
```

### 9.2 Approval Rules
- If Avi approves both: → proceed to Phase 1 of next sprint.
- If Avi approves the sprint but not the next plan: → revise the plan, re-present.
- If Avi does not approve the sprint work: → rework the flagged items, re-run regression, re-review.
- **Never start the next sprint without Avi's explicit approval.**

---

## 10. Escalation Rules

When the Manager encounters a situation it cannot resolve independently, it escalates immediately.

| Situation | Action |
|-----------|--------|
| A spec requirement is ambiguous | Pause. Present the ambiguity to Avi with two or more interpretations and ask which to implement. |
| A design decision is missing from spec or UX | Pause. Flag it as an open question. Add it to spec.md §9. Ask Avi for a decision before implementing. |
| A test cannot be made to pass | After two implementation attempts, document the failure with full detail, mark item `Blocked`, and escalate. |
| An unexpected regression is found that cannot be fixed in the sprint | Document it, mark the broken items `Blocked`, escalate to Avi before the review. |
| A backlog item is discovered to be much larger than estimated | Flag immediately, do not quietly defer. Propose a re-scope with Avi before continuing. |

---

## 11. Sprint Post-Mortem Archive

*This section grows over time. Each completed sprint's post-mortem is appended below.*

---

### POST-MORTEM — E03-S1 — 2026-05-17

```
SPRINT SUMMARY
  Items planned:    8  (8 P1; 2 P2 deferred)
  Items completed:  8
  Items deferred:   2  (E03-S1-08 ring gear, E03-S1-09 rack)
  Tests added:      38
  Tests total:      93
  Regressions:      0

WHAT WENT WELL
  • Involute geometry math was correct on first implementation — all
    parametrized edge-case tests (z=8,12,100,200) passed immediately.
  • Clean separation: gear_geometry.py (pure path math) vs gear_item.py
    (QGraphicsItem) vs animation.py (QTimer controller). Each module had
    its own test file.
  • showEvent fitInView fix was simple and effective — gears now fill the
    viewport correctly on launch.
  • AnimationController.angle_for() added for testability of step_frame.

WHAT COULD BE IMPROVED
  • 3 unused imports in app.py caught by ruff (QHBoxLayout, QWidget,
    add_gear_to_scene). Lesson: review imports before the lint check.

ACTIONS TAKEN
  • Removed unused imports before closing sprint.
  • Direction colour (CW=blue, CCW=red) uses placeholder palette pending E02.

LEARNINGS TO CARRY FORWARD
  • QPainterPath is constructable without a running QApplication — safe
    for pure geometry unit tests.
  • QGraphicsItem.setRotation() is the correct way to drive gear rotation;
    AnimationController just tracks the accumulator and calls set_angle().
  • _direction is still a dynamic attribute on Gear; promote it to a
    proper field when E04-S2 (defect simulation) needs it.

KNOWLEDGE CAPTURED
  • 93 tests passing across 6 test modules.
  • E01 (15), E03-S1 (8), E04-S1 (8) = 31 items Done total.
  • Next logical sprint: E03-S2 (multi-gear canvas & interaction) or
    E04-S2 (defect simulation).
```

### POST-MORTEM — E04-S1 — 2026-05-17

```
SPRINT SUMMARY
  Items planned:    8  (8 P1; 2 P2 deferred)
  Items completed:  8
  Items deferred:   2  (E04-S1-06 belt length, E04-S1-09 tangential velocity)
  Tests added:      21
  Tests total:      55
  Regressions:      0

WHAT WENT WELL
  • BFS implementation was clean and correct on first pass.
  • All direction rules (mesh/ring/belt-crossed/belt-uncrossed/chain/idler)
    passed without requiring implementation rework.
  • solve() deep-copies the system, so the original is never mutated —
    verified explicitly by test_solve_returns_new_gearsystem_not_mutated_in_place.
  • solve() immediately wired into the demo, so RPM labels in the running
    app now come from the real engine.

WHAT COULD BE IMPROVED
  • One test had a bug: driver_rpm default in the system() helper silently
    overrode the rpm set on gA. Lesson: test helpers with defaults that
    shadow constructor args can mask intent. Fixed by passing driver_rpm
    explicitly.

ACTIONS TAKEN
  • Per spec §5.4.5, every validation error message includes a concrete
    suggested fix — enforced in the test assertion.

LEARNINGS TO CARRY FORWARD
  • _direction is stored as a dynamic attribute on Gear (not in the
    dataclass). This is intentional for now — E03 canvas will read it.
    When E03 arrives, consider promoting _direction to a proper field.
  • Idler gears: tooth count is irrelevant for the ratio between
    non-idler neighbours; the idler only affects direction.

KNOWLEDGE CAPTURED
  • 55 tests passing across 3 modules.
  • E01 (15 items), E04-S1 (8 items) = 23 items Done total.
  • Next logical sprint: E03-S1 (Canvas rendering) so the demo
    shows real animated gears, or E04-S2 (Defect simulation).
```

```
SPRINT SUMMARY
  Items planned:    8  (7 E01-S2 + 1 carried E01-S1-08)
  Items completed:  8
  Items deferred:   0
  Tests added:      24
  Tests total:      34
  Regressions:      0

WHAT WENT WELL
  • All 24 tests were genuinely RED before models.py existed and
    genuinely GREEN after — clean TDD signal.
  • Dataclasses with field(default_factory=list) correctly isolated
    per-instance defect lists; the shared-default trap was caught by
    test_gear_defects_are_independent_per_instance.
  • to_dict / from_dict round-trip test (GearSystem) gave immediate
    confidence that serialisation works end-to-end before E11 (file I/O).
  • ruff caught two unused imports left over from E01-S1; fixed before
    committing.

WHAT COULD BE IMPROVED
  • GoalSpec is intentionally minimal (only target_ratio); this will need
    richer fields when E07 (Puzzle Engine) is implemented. Flag for E07-S1.

ACTIONS TAKEN
  • ruff.toml committed so lint config is source-controlled.
  • requirements.txt frozen with ruff added.

LEARNINGS TO CARRY FORWARD
  • Enum values inherit from str for clean JSON serialisation without a
    custom encoder — use this pattern in all future enums.
  • PuzzleFile.research is typed Optional[dict] rather than a dataclass
    to keep it schema-flexible for the research team.

KNOWLEDGE CAPTURED
  • E01 is now 100% complete (15/15 items Done, 34 tests passing).
  • Next: E02 is a Design epic (no code). E04 (Kinematics) can proceed
    in parallel — all it needs is the data model, which is now stable.
```

```
SPRINT SUMMARY
  Items planned:    8
  Items completed:  7
  Items deferred:   1  (E01-S1-08 CI/linting — P2, not blocking)
  Tests added:      10
  Tests total:      10
  Regressions:      0

WHAT WENT WELL
  • Full TDD cycle executed cleanly: all 7 tests failed red before
    implementation and passed green after — no false greens detected.
  • PyQt6 install via Intel proxy was straightforward.
  • Config round-trip (write defaults → reload → mutate → save → reload)
    confirmed working with tmp_path isolation.
  • sys.excepthook pattern is clean and easily verifiable via caplog.

WHAT COULD BE IMPROVED
  • test_main_module_is_importable passed before implementation because
    main.py already existed. This is correct behaviour, but worth noting:
    pre-existing skeleton code can make some TDD "fail first" checks
    trivially pass. Future sprints should audit skeleton files before
    writing tests.

ACTIONS TAKEN
  • No process changes needed; lifecycle ran as documented.

LEARNINGS TO CARRY FORWARD
  • AppConfig uses tmp_path in tests — never writes to real ~/.gearlab
    during the test suite. This pattern should be used for all file-backed
    classes.
  • QGraphicsView with ScrollHandDrag mode is the correct starting point;
    zoom-to-cursor via AnchorUnderMouse is already wired in.

KNOWLEDGE CAPTURED
  • PYTHONPATH=src must be set for pytest to resolve `gearlab.*` imports.
  • pytest.ini testpaths = tests covers all subdirectories automatically.
  • PyQt6 import works headlessly in tests via pytest-qt's qtbot fixture;
    no display server or offscreen plugin required on Windows.
```

---

### POST-MORTEM — E04-S2 — 2026-05-23

```
SPRINT SUMMARY
  Items planned:    8  (5 P1 + 3 deferred)
  Items completed:  5  (E04-S2-01, 02, 04, 05, 08)
  Items deferred:   3  (E04-S2-03 worn visual, E04-S2-06 event log, E04-S2-07 puzzle toggle)
  Tests added:      19
  Tests total:      112
  Regressions:      0

WHAT WENT WELL
  • All 19 tests were RED before implementation and GREEN after; clean TDD cycle.
  • Inline defect_map param in spur_gear_path() kept the change backwards-compatible —
    all 18 existing geometry tests still pass without modification.
  • Lazy import of DefectType inside spur_gear_path() via TYPE_CHECKING guard avoids
    any circular import risk while keeping the type signature visible to IDEs.
  • defect_at_contact() as a pure module-level function in animation.py is easily
    unit-tested and reusable outside the controller.
  • Flash (GearItem.flash()) implemented with QTimer.singleShot — fire and forget,
    no state machine needed.

WHAT COULD BE IMPROVED
  • The slip cascading (gC not slipping when gB slips) is intentionally simplified.
    For a full simulation, the _tick() loop would need a second pass to cascade slips
    through the connection graph. Flag for E04-S3 if physics accuracy becomes a goal.
  • defect_at_contact threshold (< half_pitch) is a heuristic. For high-speed gears
    a tighter threshold may be needed to avoid false positives.

ACTIONS TAKEN
  • App demo updated: gA (20T driver) has tooth 0 MISSING, visible as a concave gap.
  • Flash callback registered at startup — bright yellow 250ms flash on engagement.

LEARNINGS TO CARRY FORWARD
  • Defect-aware rendering via defect_map is the cleanest pattern: geometry stays
    pure math, caller decides what defects to inject. No subclassing needed.
  • When a pure-math function needs enum values from models.py, use a lazy import
    inside the function body (not at module level) to avoid circular deps.

KNOWLEDGE CAPTURED
  • 112 tests passing across 7 test files.
  • E04 done: 13/18 items complete; 3 deferred (worn visual, event log, puzzle toggle).
  • Next: E03-S2 (canvas interaction) + guided demo sprint.
```

---

### POST-MORTEM — E03-S2 — 2026-05-23

```
SPRINT SUMMARY
  Items planned:    10  (5 done; 5 deferred)
  Items completed:  5   (E03-S2-01, 02, 03, 04, 10)
  Items deferred:   5   (E03-S2-05 duplicate, E03-S2-06 undo/redo,
                         E03-S2-07/08/09 belt/chain rendering)
  Tests added:      11
  Tests total:      123
  Regressions:      0

WHAT WENT WELL
  • snap_position() as a pure-math module (snap.py) is trivially testable
    without any Qt context — all 5 snap tests run in < 1ms.
  • Qt ItemIsSelectable + ItemIsMovable flags required zero custom event
    handling for drag-to-move; it works out of the box.
  • _rebuild_system() auto-detects MESH connections from gear positions,
    so the user never has to manually wire connections — just drag to snap.
  • Switching from ScrollHandDrag to NoDrag freed items to receive mouse
    events; middle-mouse still pans the scene (Qt default).

WHAT COULD BE IMPROVED
  • Undo/redo (E03-S2-06) was the biggest deferral. Implementing it
    requires a Command pattern before further destructive edits are added.
    Flag for E03-S3 as the top priority.
  • Belt/chain rendering (E03-S2-07/08/09) needs a ConnectionType.BELT
    renderer — a separate pass over connections, not per-item. Flag for
    E03-S4 after the belt geometry is fleshed out.

ACTIONS TAKEN
  • DragMode changed from ScrollHandDrag to NoDrag — noted in post-mortem
    so future scrolling/pan issues are easier to trace.

LEARNINGS TO CARRY FORWARD
  • snap_callback on GearItem is set by the app, not the item — keeps
    snap logic in the app layer where it belongs.
  • _rebuild_system() must be called after every structural edit (add,
    delete, snap). The pattern is: mutate scene → call rebuild.
  • boundingRect() must be large enough to contain the highlight ring.
    Use max(module, 10) as the extra padding to handle small modules.

KNOWLEDGE CAPTURED
  • 123 tests passing across 8 test files.
  • E03 done: 13/20 items. E04 done: 13/18 items.
  • Next: E03-S3 (undo/redo + duplicate) or a different epic.
```

---

### POST-MORTEM — E05-S1 — 2026-05-26

```
SPRINT SUMMARY
  Items planned:    7   (6 done; 1 deferred)
  Items completed:  6   (E05-S1-01 through E05-S1-06)
  Items deferred:   1   (E05-S1-07 mode persistence — defer to E11)
  Tests added:      14
  Tests total:      137
  Regressions:      0

WHAT WENT WELL
  • ModeController is pure Python (no Qt) — 10 of 14 tests run with no
    QApplication overhead. Very fast.
  • AppMode(str, Enum) inherits str so values compare naturally with
    string literals without .value lookups.
  • QButtonGroup(exclusive=True) for the mode bar required zero custom
    logic for mutual exclusion; works out of the box.
  • _apply_mode_ui() is a single method that owns all visibility rules,
    making future mode expansions a one-line change per control.

WHAT COULD BE IMPROVED
  • mode persistence (E05-S1-07) was deferred; it belongs alongside
    the general save/load system (E11) rather than as an isolated config
    file, so the deferral is the right call.
  • The isVisibleTo(ancestor) vs isVisible() distinction tripped up the
    test for "button should be visible in Engineer mode". isVisible()
    requires the window to be shown; isVisibleTo() tests logical
    visibility without a display — prefer isVisibleTo() in all widget
    visibility tests going forward.

ACTIONS TAKEN
  • ui/ package created (src/gearlab/ui/__init__.py + ui/mode.py).
  • app.py: renamed btn_add → _btn_add_gear; added _lbl_teeth reference
    so _apply_mode_ui() can hide/show all four edit controls.
  • Top toolbar added at Qt.ToolBarArea.TopToolBarArea to keep mode
    switcher visually separate from playback controls at the bottom.

LEARNINGS TO CARRY FORWARD
  • Use isVisibleTo(window) instead of isVisible() when testing widget
    visibility without showing the window.
  • Keep mode logic in ModeController (pure Python) and Qt wiring in
    app.py — the separation makes both layers independently testable.
  • frozenset for capability sets is slightly safer than plain set
    because it prevents accidental mutation.

KNOWLEDGE CAPTURED
  • 137 tests passing across 9 test files.
  • E05 done: 6/16 items. E03 done: 13/20. E04 done: 13/18. E01 done: 15/15.
  • Next sprint candidates: E05-S2 (properties panel + toolbox),
    E06-S1 (ratio badges), or E03-S3 (undo/redo + duplicate).
```

---

## 12. Change Log

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-05-17 | — | Initial manager playbook |
| 0.2 | 2026-05-23 | — | Added E04-S2 post-mortem |
| 0.3 | 2026-05-23 | — | Added E03-S2 post-mortem |
| 0.4 | 2026-05-26 | — | Added E05-S1 post-mortem |
