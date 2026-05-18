# GearLab — Copilot Agent Instructions

## CRITICAL: Python Environment Rules

This project uses a **Python virtual environment**. The following rules are
**non-negotiable** and must be followed in every session.

---

### 1. Always Use the Virtualenv

The virtualenv lives at `env\` in the project root.  
**Never install packages globally. Never run `python` or `pip` outside the venv.**

```powershell
# Activate before EVERY Python or pip command
cd C:\Projects\0Mech
.\env\Scripts\Activate.ps1
# Prompt should show (env) prefix before continuing
```

---

### 2. Always Set Proxy Before pip Install

Direct internet access is blocked. All `pip install` commands **must** set the Intel proxy first:

```powershell
$env:HTTP_PROXY  = "http://proxy-mu.intel.com:912"
$env:HTTPS_PROXY = "http://proxy-mu.intel.com:912"
pip install <package>
```

Or inline:
```powershell
pip install <package> --proxy http://proxy-mu.intel.com:912
```

---

### 3. Full Setup Recipe (run once, or to recreate env)

```powershell
cd C:\Projects\0Mech
python -m venv env
.\env\Scripts\Activate.ps1
$env:HTTP_PROXY  = "http://proxy-mu.intel.com:912"
$env:HTTPS_PROXY = "http://proxy-mu.intel.com:912"
pip install -r requirements.txt
```

---

### 4. After Installing Any New Package

```powershell
pip freeze > requirements.txt
```

Always commit the updated `requirements.txt`. Never commit the `env\` folder.

---

### 5. Running the Application

```powershell
.\env\Scripts\Activate.ps1
python main.py
```

### 6. Running Tests

```powershell
.\env\Scripts\Activate.ps1
pytest tests\ -v
```

---

### 7. Python Interpreter

- **Path**: `C:\Users\asalmon\AppData\Local\Programs\Python\Python311\python.exe`
- **Version**: Python 3.11.9
- **VS Code interpreter**: `.\env\Scripts\python.exe` (set in `.vscode\settings.json`)

---

## Project Overview

GearLab is a PyQt6-based educational gear simulation tool.  
Key documents (read before starting any sprint):

- [`docs/spec.md`](docs/spec.md) — Full product specification
- [`docs/UX.md`](docs/UX.md) — UX design, personas, user stories
- [`docs/backlog.md`](docs/backlog.md) — Sprint backlog (13 epics, 205 items)
- [`docs/manager.md`](docs/manager.md) — Sprint lifecycle and TDD process

## Project Structure

```
C:\Projects\0Mech\
├── main.py                  # Application entry point
├── requirements.txt         # All dependencies (keep updated)
├── pytest.ini               # Test runner config
├── run.ps1                  # One-click launcher
├── env\                     # Virtualenv (NEVER commit)
├── src\
│   └── gearlab\             # Main package
│       ├── __init__.py
│       ├── app.py           # QMainWindow shell
│       ├── canvas\          # E03: rendering engine
│       ├── engine\          # E04: kinematics engine
│       ├── ui\              # E05: panels and mode system
│       ├── puzzle\          # E07: puzzle engine
│       └── research\        # E10: research/logging mode
├── tests\
│   ├── unit\
│   ├── integration\
│   └── performance\
├── assets\
│   ├── design\              # E02: design artifacts
│   └── icons\
├── puzzles\                 # Built-in puzzle library (.gearlab files)
└── docs\
    ├── spec.md
    ├── UX.md
    ├── backlog.md
    ├── manager.md
    └── dashboard.html
```

## Technology Stack

| Library     | Purpose                        | Version  |
|-------------|--------------------------------|----------|
| PyQt6       | GUI framework + canvas         | ≥6.7.0   |
| NumPy       | Gear geometry calculations     | ≥1.26.0  |
| Pillow      | PNG export                     | ≥10.3.0  |
| pytest      | Test runner                    | ≥8.2.0   |
| pytest-qt   | Qt widget testing support      | ≥4.4.0   |

## Manager Process Reminder

Follow the sprint lifecycle in `docs/manager.md` exactly:  
**Plan → Gate 1 (Avi approval) → TDD Dev → Regression → Post-mortem → Dashboard update → Gate 2 (Avi approval)**

TDD is mandatory. Write the test first, confirm it fails, implement, confirm it passes, add to regression.
