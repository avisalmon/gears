# GearLab — User Experience Design

**Status:** Draft  
**Version:** 0.1  
**Last Updated:** 2026-05-17  
**Companion to:** [spec.md](spec.md)

---

## Table of Contents

1. [UX Philosophy](#1-ux-philosophy)
2. [Personas](#2-personas)
   - 2.1 Maya — The Curious Student
   - 2.2 Daniel — The High School Physics Teacher
   - 2.3 Dr. Lena — The Cognitive Behavior Researcher
3. [User Stories](#3-user-stories)
4. [User Journey Maps](#4-user-journey-maps)
5. [Emotional Arc Design](#5-emotional-arc-design)
6. [Gamification Framework](#6-gamification-framework)
7. [Adaptive UI Contract](#7-adaptive-ui-contract)
8. [Accessibility Principles](#8-accessibility-principles)
9. [Research & Data Layer](#9-research--data-layer)
10. [Open UX Questions](#10-open-ux-questions)
11. [Change Log](#11-change-log)

---

## 1. UX Philosophy

GearLab is not a calculator dressed up with animations. It is an **experience machine** — a space where understanding is earned through doing, not reading.

### 1.1 Core Design Principles

| # | Principle | What It Means in Practice |
|---|-----------|--------------------------|
| P1 | **Feel before formula** | Every user — even an engineer — sees the gears spin before they see a number. Motion is the primary teacher. |
| P2 | **Earn the depth** | Complexity is revealed progressively. A 7-year-old and a PhD use the same canvas; only the information layer changes. |
| P3 | **Make mistakes cheap** | Undo is always available. Broken configurations don't crash — they show friendly, informative error states. Experimentation must feel safe. |
| P4 | **Celebrate discovery** | When a user figures something out — achieves a ratio, identifies a defect — the system responds with positive feedback, not just silent success. |
| P5 | **Invisible complexity** | The simulation engine is sophisticated; the user should never feel that. Physics happens behind the curtain. |
| P6 | **Every mode is complete** | A kid in Explorer mode gets a full, satisfying experience. An engineer in Expert mode gets a full, satisfying experience. Neither is a "demo" of the other. |
| P7 | **Data is a side effect** | The researcher's data collection must be invisible to all other users. It must never degrade the experience for Maya or Daniel. |

---

## 2. Personas

---

### 2.1 Persona: Maya — The Curious Student

```
┌──────────────────────────────────────────────────────────────────┐
│  NAME:    Maya                                                   │
│  AGE:     15                                                     │
│  ROLE:    High school student, 10th grade STEM track             │
│  LOCATION: Mid-size city, uses the tool in school lab and at home│
│  DEVICE:  School Windows PC, personal laptop                     │
└──────────────────────────────────────────────────────────────────┘
```

**Background**  
Maya is naturally curious about how things work — she's the one who takes apart pens to see the spring. She's good at math when she can *see* it, but formulas on a whiteboard lose her. Her teacher assigned GearLab as a homework companion to a unit on mechanical advantage.

**Goals**
- Understand why a bicycle has gears and how changing gear ratio affects pedaling effort.
- Complete the assigned puzzle challenges (Medium difficulty).
- Build something cool to show her friends.

**Frustrations**
- "When I get something wrong, tools usually just say ERROR and I don't know what to do."
- "I hate reading walls of text to figure out how to use something."
- "Math feels fake when it's just symbols."

**Motivations**
- Immediate visual feedback — she wants to *see* the gears turn right away.
- Earning stars and completion badges gives her a sense of progress.
- Sharing her gear machine (as an image or file) to show friends.

**Technical Comfort**
- Confident with drag-and-drop apps.
- Will not read a manual. Must learn entirely through exploration and in-context hints.

**Key Behaviors in GearLab**
- Starts in **Student mode** as assigned by teacher.
- Connects two gears and immediately hits Play to see them spin.
- Tries wrong combinations first; expects gentle correction.
- Uses the hint system when stuck on puzzles (aims to use as few hints as possible).
- Shares her best design using the PNG export.

---

### 2.2 Persona: Daniel — The High School Physics Teacher

```
┌──────────────────────────────────────────────────────────────────┐
│  NAME:    Daniel                                                 │
│  AGE:     41                                                     │
│  ROLE:    High school physics & technology teacher, 12 years exp │
│  LOCATION: Suburban school, classroom of 28 students            │
│  DEVICE:  School projector PC (Windows), sometimes personal Mac  │
└──────────────────────────────────────────────────────────────────┘
```

**Background**  
Daniel has been teaching mechanics for over a decade. He's used whiteboards, physical gear kits, and YouTube videos — all with partial success. He finds that students engage for about 5 minutes with physical kits before they get distracted or break something. He wants a tool he can project on screen for the class and also assign as independent work.

**Goals**
- Project a live gear animation during class lectures to make the formula `ratio = N2/N1` visually obvious.
- Create custom puzzles that align with his syllabus (e.g., a puzzle on the exact gear ratios in a bicycle drivetrain).
- Track which students are stuck on which concepts without asking them directly.
- Have a reliable, crash-free experience in front of 28 students.

**Frustrations**
- "If it crashes in the middle of a lesson, I lose the class for 10 minutes."
- "I don't want to learn a new complex tool. I should be up and running in 10 minutes."
- "I need control over what students see — I want to hide the answers when I project a puzzle."

**Motivations**
- A tool that makes *his* teaching better, not one that replaces him.
- Confidence: knowing the tool will behave predictably in a live classroom.
- The puzzle editor lets him author his own exam-style problems.

**Technical Comfort**
- Solid with standard desktop apps.
- Will spend 20–30 minutes learning a new tool if it clearly pays off.
- Intimidated by command-line or developer-facing features.

**Key Behaviors in GearLab**
- Spends a Sunday afternoon building 5–6 custom puzzles for his class unit.
- During class: runs in **Presentation mode** — full screen, no toolbox clutter, formula panel visible.
- Assigns puzzles to students via shared `.gearlab` files on the school's drive.
- Checks the session summary (if available) to see aggregated class performance on puzzles.

---

### 2.3 Persona: Dr. Lena — The Cognitive Behavior Researcher

```
┌──────────────────────────────────────────────────────────────────┐
│  NAME:    Dr. Lena                                               │
│  AGE:     38                                                     │
│  ROLE:    Cognitive psychology researcher, university lab        │
│  LOCATION: University, runs GearLab in controlled study sessions │
│  DEVICE:  Researcher-controlled lab PCs (Windows)               │
└──────────────────────────────────────────────────────────────────┘
```

**Background**  
Dr. Lena studies how people develop spatial reasoning and problem-solving strategies — particularly how gamified environments affect learning transfer compared to traditional instruction. She has heard about GearLab and wants to use it as a research instrument in a study involving 60 university students across two groups: one playing puzzle mode freely, one following guided instruction.

**Goals**
- Capture rich behavioral data: time-on-task per puzzle, hint usage, number of failed attempts, gear configurations tried, undo frequency, and final solution path.
- Compare problem-solving strategies between novices and students with prior mechanical knowledge.
- Do this without altering the experience for study participants — data collection must be silent and invisible.
- Export data in a clean, analyzable format (CSV or JSON) at the end of a session.

**Frustrations**
- "Most educational tools don't log anything useful for research."
- "I need raw behavioral data, not just a score. I want the *process*, not the *result*."
- "IRB compliance means I cannot use tools that send data to the cloud. Everything must stay local."

**Motivations**
- GearLab as a research instrument is exciting because the task is concrete, measurable, and engaging to participants.
- The puzzle mode creates a controlled, reproducible task environment.
- She can design custom puzzles of controlled difficulty to test specific cognitive loads.

**Technical Comfort**
- Comfortable with Python and data files (CSV, JSON, pandas).
- Can edit a config file; does not expect a full developer workflow.
- Needs clear documentation for enabling and disabling the data layer.

**Key Behaviors in GearLab**
- Enables **Research Mode** via a config file or settings menu before each study session.
- Assigns a specific set of puzzles in a fixed order to all participants.
- Exports a per-session behavioral log at the end — one JSON/CSV file per participant.
- Does NOT interact with the tool herself during sessions — it runs on its own.
- Post-session: loads the export files into her Python analysis pipeline.

---

## 3. User Stories

### 3.1 Maya — Student Stories

| ID | As Maya, I want to... | So that... | Acceptance Criteria |
|----|----------------------|------------|---------------------|
| US-M1 | Drop a gear onto the canvas and see it spin immediately when I press Play | I get instant feedback and feel engaged | Gear animates within 1 second of pressing Play with no prior setup |
| US-M2 | Connect two gears and see the second one start spinning in the opposite direction | I understand the basic meshing rule visually | Second gear animates in reverse; direction arrow badges appear on both |
| US-M3 | Hover over any gear and read a plain sentence explaining its speed relative to the driver | I understand ratios without needing a formula | Tooltip appears within 300ms; language is simple, no jargon |
| US-M4 | Change a gear's tooth count with a slider and see the animation update live | I explore the relationship between size and speed | Animation re-calculates and updates in under 100ms |
| US-M5 | Attempt a puzzle and get a helpful message when I'm wrong — not just a red X | I know what to try next without feeling dumb | Error state shows a friendly message with a directional hint |
| US-M6 | Earn stars for completing a puzzle with few hints | I feel rewarded for thinking hard | Star rating shown at completion; fewer hints = more stars |
| US-M7 | Export my gear machine as an image to share | I can show my friends what I made | PNG exported with one click; filename defaults to the design name |
| US-M8 | Switch between Student and Explorer mode | I can simplify the UI when it feels overwhelming | Mode switch is one click; UI re-renders immediately |

### 3.2 Daniel — Teacher Stories

| ID | As Daniel, I want to... | So that... | Acceptance Criteria |
|----|------------------------|------------|---------------------|
| US-D1 | Build a custom puzzle in under 10 minutes | I can create class assignments without investing hours | Puzzle editor is accessible from the main menu; a complete puzzle can be authored and saved in ≤10 min |
| US-D2 | Lock certain elements in a puzzle so students cannot move them | The puzzle has a clear starting structure | Elements can be marked "locked" in the puzzle editor; locked elements show a padlock icon |
| US-D3 | Run GearLab in full-screen Presentation mode with a clean UI | My class sees the simulation, not developer chrome | Presentation mode hides toolbox and properties panel; formula panel stays visible |
| US-D4 | Show the gear ratio formula updating live as I change tooth counts | Students see math and motion simultaneously | Formula panel is always visible in Presentation mode; updates in real time |
| US-D5 | Save a puzzle file and share it via a school drive | Students open my puzzle on their own machines | Puzzle saves as a single portable `.gearlab` file; opens correctly on any GearLab install |
| US-D6 | See a summary of class performance on a puzzle set | I know which concepts need re-teaching | Aggregated summary (average solve time, hint usage rate) generated from student-exported session files |
| US-D7 | Trust the tool will not crash during a live lesson | I maintain classroom credibility | Zero crashes on any valid gear configuration; all error states are graceful and non-blocking |
| US-D8 | Discover new features gradually without reading documentation | I get better at the tool over time | In-context tooltips introduce one new feature per session until all features have been surfaced |

### 3.3 Dr. Lena — Researcher Stories

| ID | As Dr. Lena, I want to... | So that... | Acceptance Criteria |
|----|--------------------------|------------|---------------------|
| US-L1 | Enable a silent data-logging mode with no visible UI changes | Participants behave naturally | Research mode toggled via settings; zero visual difference for the participant |
| US-L2 | Log every user action with a timestamp | I can reconstruct the full problem-solving process | Event log captures: gear placed, connection made, parameter changed, hint used, play pressed, undo, solve attempt, time elapsed |
| US-L3 | Assign a fixed sequence of puzzles to run automatically | All participants complete the same task set in the same order | Session config file specifies puzzle order; tool loads them sequentially without user navigation |
| US-L4 | Export a session log as a structured JSON or CSV file | I can load data directly into my analysis pipeline | Export button (or auto-save on session end) produces a clean, schema-consistent file per participant |
| US-L5 | Assign a participant ID at session start | My data files are linked to my study records | Tool prompts for participant ID when Research mode is active; ID is embedded in all log filenames |
| US-L6 | Ensure all data stays on the local machine — no cloud upload | IRB compliance is maintained | Tool has no network calls; zero telemetry; all logs written only to local disk in a configurable path |
| US-L7 | Replay a participant's solution path after the session | I can qualitatively analyze strategy differences | Replay mode loads a session log and animates the actions step-by-step |
| US-L8 | Annotate puzzles with cognitive load metadata | I can correlate difficulty with behavioral signals | Puzzle file format includes optional researcher fields: expected_difficulty, domain_prior_required, spatial_reasoning_type |

---

## 4. User Journey Maps

### 4.1 Maya's Journey — "First Puzzle Solved"

```
STAGE          │  AWARENESS     │  FIRST LAUNCH   │  EXPLORATION   │  FIRST PUZZLE   │  COMPLETION    │  RETURN
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
ACTIONS        │ Teacher assigns│ Sees welcome     │ Drops first    │ Opens puzzle    │ Solves puzzle  │ Opens next day
               │ GearLab as HW  │ screen; picks    │ gear, hits     │ from homework   │ on 3rd attempt │ to try harder
               │                │ "Student" mode   │ Play           │ list            │ (1 hint used)  │ puzzle
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
THINKING       │ "Another tool  │ "OK this looks   │ "Oh it spins!  │ "I need to make │ "Wait — if I   │ "I want to
               │ the teacher    │ pretty simple"   │ What if I add  │ it go 3x faster │ use fewer teeth│ beat my star
               │ is making me   │                  │ another?"      │ — how?"         │ it goes faster"│ rating"
               │ use..."        │                  │                │                 │                │
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
FEELING        │ 😐 Neutral     │ 🙂 Mildly        │ 😊 Interested  │ 😕 Confused     │ 🤩 Proud /     │ 😊 Motivated
               │                │ curious          │                │ → 😤 Stuck       │ "I got it!"    │ returning
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
TOUCHPOINTS    │ Teacher verbal │ Welcome screen   │ Canvas + Play  │ Puzzle modal    │ Star rating    │ Recent files
               │ instruction    │ + mode selector  │ button         │ + hint button   │ + share button │ on home screen
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
PAIN POINTS    │ —              │ Mode names must  │ No manual help │ Error messages  │ —              │ Must remember
               │                │ be immediately   │ needed — good  │ must guide, not │                │ where she left
               │                │ self-explanatory │                │ just reject     │                │ off
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
OPPORTUNITIES  │ —              │ Quick-start      │ Snap-to-mesh   │ Hint system     │ Celebration    │ Progress      
               │                │ animated demo    │ removes        │ + directional   │ animation +    │ dashboard on  
               │                │ on welcome screen│ friction       │ error messages  │ share button   │ home screen   
```

---

### 4.2 Daniel's Journey — "Preparing a Class Lesson"

```
STAGE          │  DISCOVERY     │  PREP (SUNDAY)  │  CLASSROOM     │  DURING LESSON │  POST-LESSON   │  NEXT UNIT
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
ACTIONS        │ Hears about    │ Builds 5 custom  │ Launches in    │ Projects live   │ Collects       │ Updates
               │ GearLab from a │ puzzles; tests   │ Presentation   │ animation;      │ student files; │ puzzles based
               │ colleague      │ them himself     │ mode           │ edits live      │ checks summary │ on results
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
THINKING       │ "Is this worth │ "This puzzle     │ "Please don't  │ "Students are   │ "Half the class│ "I need a
               │ my time to     │ editor is        │ crash on me    │ actually         │ used 2+ hints  │ harder version
               │ learn?"        │ actually nice"   │ now..."        │ watching"       │ on puzzle 3"   │ of puzzle 3"
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
FEELING        │ 🤨 Skeptical   │ 😌 Absorbed /   │ 😬 Anxious     │ 😄 Confident /  │ 🧐 Analytical  │ 💡 Energized
               │                │ pleasantly       │                │ delighted        │                │
               │                │ surprised        │                │                 │                │
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
TOUCHPOINTS    │ Colleague demo │ Puzzle editor    │ Presentation   │ Formula panel   │ Summary export │ Puzzle editor
               │ or short video │ + file save      │ mode toggle    │ + live canvas   │ + hint data    │ (edit existing)
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
PAIN POINTS    │ No time for    │ Learning curve   │ Fear of        │ Must not show   │ Data is locked │ Iterating on
               │ long onboarding│ on first puzzle  │ live failure   │ toolbox chrome  │ in individual  │ difficulty is
               │                │ must be < 5 min  │                │ to students     │ student files  │ tedious
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
OPPORTUNITIES  │ 60-second demo │ Guided "first    │ F11 / one-key  │ Annotation layer│ Batch-import   │ Duplicate &
               │ video on launch│ puzzle" template │ Presentation   │ teacher can     │ student files  │ modify existing
               │ screen         │ in puzzle editor │ mode shortcut  │ draw on canvas  │ for aggregate  │ puzzle in editor
```

---

### 4.3 Dr. Lena's Journey — "Running a Research Study Session"

```
STAGE          │  STUDY DESIGN  │  SETUP          │  SESSION RUN   │  DATA EXPORT   │  ANALYSIS      │  PUBLICATION
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
ACTIONS        │ Designs puzzle │ Configures      │ Participant    │ Exports log     │ Loads CSV/JSON │ Uses GearLab
               │ battery;       │ Research mode;  │ solves puzzles │ per participant;│ into pandas;   │ session data
               │ writes IRB     │ sets puzzle     │ (Lena observes │ verifies schema │ runs behavioral│ as study
               │ protocol       │ sequence config │ silently)      │ completeness    │ analysis       │ instrument
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
THINKING       │ "Can this tool │ "The config     │ "Is it logging │ "Is the schema  │ "Hint timing   │ "This is
               │ give me the    │ file is clean   │ everything I   │ consistent      │ predicts final │ publishable
               │ granularity    │ and well-        │ need without   │ across all      │ performance    │ data"
               │ I need?"       │ documented"     │ participant     │ participants?"  │ better than    │
               │                │                 │ noticing?"     │                 │ time-on-task"  │
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
FEELING        │ 🧐 Evaluating  │ 😌 Systematic / │ 🤫 Vigilant /  │ ✅ Satisfied /  │ 😄 Excited by  │ 🎓 Validated
               │                │ in control      │ hoping it works│ or 😟 if schema │ early findings │
               │                │                 │                │ is broken       │                │
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
TOUCHPOINTS    │ Spec/docs +    │ `research.json` │ Invisible data │ Export button   │ Output CSV/JSON│ Cited in paper
               │ research fields│ config file     │ layer (no UI)  │ or auto-save    │ files          │
               │ in puzzle format│                │                │ at session end  │                │
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
PAIN POINTS    │ Unknown log    │ No GUI for      │ Any visible    │ Schema changes  │ Missing events │ Cannot cite
               │ granularity    │ research config │ research UI =  │ between versions│ = broken       │ without stable
               │ until she tests│ is a barrier    │ study bias     │ break pipeline  │ analysis       │ data schema
───────────────┼────────────────┼─────────────────┼────────────────┼─────────────────┼────────────────┼──────────────
OPPORTUNITIES  │ Published log  │ GUI settings    │ Verified-silent│ Schema version  │ Bundled example│ DOI-ready
               │ schema in docs │ panel for       │ mode (toggle   │ field in every  │ analysis       │ dataset export
               │ before study   │ research config │ verified by    │ log file        │ notebook       │ format
               │                │                 │ a test run)    │                 │ (Jupyter)      │
```

---

## 5. Emotional Arc Design

The emotional arc describes the intended feeling progression for each persona throughout a typical session. Designing to this arc ensures the tool delivers a satisfying, complete emotional experience — not just functional correctness.

### 5.1 Maya's Emotional Arc (typical 30-min session)

```
Excitement ↑ |        ★ COMPLETION
             |       /
             |      / ← "I almost have it"
Interest  ───|─────/──────────────────────────
             |    / ← gears spinning, exploring
Neutral   ───|───/────────────────────────────
             |  / ← launch, mode select
Skepticism ──|─/──────────────────────────────
             |/
             └────────────────────────────────→ Time
              Open     Explore    Stuck   Solve
```

**Design imperative:** The "Stuck" dip must be short and must end in a hint that feels encouraging, not condescending. The completion moment must feel earned and celebrated.

### 5.2 Daniel's Emotional Arc (prep session)

```
Confidence ↑ |               ★ READY FOR CLASS
             |              /
Comfortable─|─────────────/─────────────────
             |            / ← puzzle authored, tested
Neutral   ───|───────────/──────────────────
             |          / ← learning puzzle editor
Skeptical ───|─────────/─────────────────────
             |        / ← first launch
Anxious   ───|───────/──────────────────────
             └───────────────────────────────→ Time
              Launch   Learn   Author   Test
```

**Design imperative:** The skepticism→neutral transition must happen within the first 5 minutes. If Daniel is still confused at minute 10, he will close the tool and never return.

### 5.3 Dr. Lena's Emotional Arc (study session day)

```
Confidence ↑ |         ★ DATA EXPORTED ★
             |         |
Trusting ────|─────────|────────────────────
             |         |
Watchful  ───|─────────|────────────────────
             |    ↑ session running silently
Uncertain ───|────────────────────────────
             |  ↑ "will it log correctly?"
Skeptical ───|──────────────────────────────
             └───────────────────────────────→ Time
              Setup    Run     Export   Analyze
```

**Design imperative:** Dr. Lena needs a "verification moment" before the real study — a test run that proves logging is working correctly. Without this, she will be anxious throughout. Provide a **"Research mode test run"** that generates a sample log file she can inspect.

---

## 6. Gamification Framework

### 6.1 Principles Applied

GearLab uses **Self-Determination Theory (SDT)** as its gamification backbone:
- **Autonomy**: Users choose their path — free build or puzzle. No forced progression.
- **Competence**: Graduated difficulty + hint system ensures users always feel capable.
- **Relatedness**: Sharing designs and puzzles creates social connection even in a desktop tool.

### 6.2 Reward Mechanics

| Mechanic | Trigger | Persona Target | Purpose |
|----------|---------|----------------|---------|
| ⭐ Star rating (1–3) | Puzzle solved | Maya | Mastery signal; replay motivation |
| 🔓 Unlock badge | First use of new element type | Maya, Daniel | Feature discovery nudge |
| 📊 Ratio badge on gear | Any gear connected | All | Immediate feedback |
| ✨ Celebration animation | Puzzle solved correctly | Maya | Emotional reward |
| 🧩 Puzzle authored | First custom puzzle saved | Daniel | Creator recognition |
| 📈 Session summary | End of puzzle set | Daniel, Lena | Reflection + progress |

### 6.3 Progression System (Maya / Student)

```
Level 0 — Explorer:     Freely spin gears, no puzzles required
Level 1 — Apprentice:   Complete 3 Easy puzzles  → unlocks Belt elements
Level 2 — Mechanic:     Complete 3 Medium puzzles → unlocks Defect tools
Level 3 — Engineer:     Complete 3 Hard puzzles   → unlocks Expert data table
Level 4 — Inventor:     Author 1 custom puzzle    → unlocks Puzzle sharing
```

### 6.4 Anti-Frustration Design

| Risk | Mitigation |
|------|------------|
| Maya is stuck for >3 minutes | Subtle pulsing hint button appears (not intrusive) |
| Wrong configuration placed | Gear glows orange; tooltip says what's wrong and one way to fix it |
| Puzzle seems impossible | After 5 failed attempts, a "nudge" animation shows one correct partial step |
| Student quits mid-puzzle | Progress is auto-saved; next launch offers "Continue where you left off" |

---

## 7. Adaptive UI Contract

The UI mode is not just a cosmetic change. Each mode has a binding contract on what is shown, hidden, and editable.

| Feature | Explorer (Kids) | Student | Engineer | Puzzle | Presentation |
|---------|----------------|---------|----------|--------|--------------|
| Tooth count control | Slider only, large | Slider + number | Full input + module | Hidden | Read-only |
| Module / pitch | Hidden | Hidden | Visible | Hidden | Read-only |
| Defect injection | Hidden | Hidden | Full | Hidden (may be pre-set) | Hidden |
| Formula panel | Hidden | Simplified | Full + derivation | Hidden | Visible |
| Ratio badge | Large emoji + ratio | Ratio number | Ratio + RPM + velocity | Goal delta shown | Ratio number |
| Direction arrows | Large, colorful | Standard | Standard | Standard | Large |
| Properties panel | Minimal | Moderate | Full | Goal only | Minimal |
| Expert data table | Hidden | Hidden | Full | Hidden | Configurable |
| Toolbox | Icons only, large | Icons + labels | Icons + labels + count | Hidden (locked set) | Hidden |
| Undo button | Prominent | Standard | Standard | Standard | Hidden |
| Research logging | Never visible | Never visible | Never visible | Active if enabled | Never visible |

---

## 8. Accessibility Principles

### 8.1 Visual Accessibility
- 8.1.1 All color-coded states (direction, error, tension) have a non-color redundant indicator (shape, label, icon).
- 8.1.2 Minimum touch target size: 44×44px for all interactive elements.
- 8.1.3 High-contrast mode: all gear outlines and text pass WCAG AA contrast ratio.
- 8.1.4 Tooth count and ratio values always shown as text — never color alone.

### 8.2 Cognitive Accessibility
- 8.2.1 Error messages always state what happened AND what to do next. Never only what went wrong.
- 8.2.2 Maximum one animated element per contextual hint at a time.
- 8.2.3 Animation can be paused or slowed globally without losing any information.

### 8.3 Age-Range Considerations
- 8.3.1 Explorer mode font size: minimum 16pt. Labels short, simple vocabulary.
- 8.3.2 No timed pressure in any non-competitive mode. Timers are opt-in in puzzle mode only.

---

## 9. Research & Data Layer

### 9.1 Logged Event Schema

All events share this envelope:

```json
{
  "schema_version": "1.0",
  "participant_id": "P042",
  "session_id": "uuid",
  "puzzle_id": "gear_ratio_medium_07",
  "timestamp_ms": 12345678,
  "event_type": "...",
  "payload": { }
}
```

### 9.2 Event Types

| Event Type | Payload Fields | Notes |
|------------|----------------|-------|
| `session_start` | participant_id, mode, puzzle_sequence | |
| `puzzle_opened` | puzzle_id, difficulty | |
| `gear_placed` | gear_id, type, tooth_count, position | |
| `gear_moved` | gear_id, from_position, to_position | |
| `gear_deleted` | gear_id | |
| `connection_made` | connection_type, element_a, element_b | |
| `parameter_changed` | gear_id, field, old_value, new_value | |
| `play_pressed` | current_system_state_snapshot | |
| `hint_requested` | puzzle_id, hint_level (1/2/3), time_since_puzzle_open_ms | |
| `solve_attempted` | current_system_state_snapshot, is_correct | |
| `puzzle_solved` | puzzle_id, solve_time_ms, hints_used, attempts | |
| `undo_pressed` | action_undone | |
| `session_end` | total_puzzles_attempted, total_puzzles_solved, total_hints_used | |

### 9.3 Data File Convention
- One file per participant per session: `gearlab_P042_20260517_143200.json`
- Auto-saved on session end to a configurable local directory.
- Human-readable JSON (pretty-printed, not minified).

### 9.4 Privacy & Compliance
- 9.4.1 No network calls under any circumstances. Zero telemetry in all modes.
- 9.4.2 Participant IDs are researcher-assigned codes — no names or personal data in log files.
- 9.4.3 Research mode must be explicitly enabled. It is OFF by default.
- 9.4.4 A prominent "Research Mode Active" indicator shown to the researcher only at session start (not visible on participant screen if dual-monitor setup is not used).

---

## 10. Open UX Questions

| ID | Question | Relevant Persona | Priority |
|----|----------|-----------------|----------|
| UQ1 | Should Maya's progression (Apprentice → Mechanic) be visible as a persistent badge/progress bar, or milestone-only? | Maya | High |
| UQ2 | Should Daniel be able to annotate a live canvas during Presentation mode (virtual "pointer" or draw tool)? | Daniel | Medium |
| UQ3 | How does Dr. Lena handle a participant who quits mid-puzzle? Partial session log must be recoverable. | Lena | High |
| UQ4 | Should puzzle star ratings be stored globally (so Maya sees her best score on re-attempts)? | Maya | Medium |
| UQ5 | Is a dual-screen setup supported for Dr. Lena (researcher monitor shows research overlay; participant monitor is clean)? | Lena | Medium |
| UQ6 | Should the tool support a "classroom network" mode where Daniel can push a puzzle to all connected students? | Daniel | Low (v2) |
| UQ7 | Should hint text be configurable by Daniel when authoring a puzzle? | Daniel | High |
| UQ8 | What language(s) should the UI support at launch? | All | Medium |

---

## 11. Change Log

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 0.1 | 2026-05-17 | — | Initial UX document — 3 personas, journey maps, gamification framework, research data schema |
