"""
Application configuration system (E01-S1-06).
Reads/writes config.json in the config directory.
"""
import json
from pathlib import Path
from typing import Optional

_DEFAULTS = {
    "mode": "student",
    "last_file": None,
    "research_mode": False,
}

_CONFIG_FILENAME = "config.json"


class AppConfig:
    """Persistent application configuration backed by a JSON file."""

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        if config_dir is None:
            config_dir = Path.home() / ".gearlab"
        self._path = Path(config_dir) / _CONFIG_FILENAME
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._data = dict(_DEFAULTS)
        self._load()

    # ------------------------------------------------------------------
    # Public properties
    # ------------------------------------------------------------------

    @property
    def mode(self) -> str:
        return self._data["mode"]

    @mode.setter
    def mode(self, value: str) -> None:
        self._data["mode"] = value

    @property
    def last_file(self) -> Optional[str]:
        return self._data["last_file"]

    @last_file.setter
    def last_file(self, value: Optional[str]) -> None:
        self._data["last_file"] = value

    @property
    def research_mode(self) -> bool:
        return self._data["research_mode"]

    @research_mode.setter
    def research_mode(self, value: bool) -> None:
        self._data["research_mode"] = value

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self) -> None:
        self._path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")

    def _load(self) -> None:
        if self._path.exists():
            try:
                stored = json.loads(self._path.read_text(encoding="utf-8"))
                self._data.update(stored)
            except (json.JSONDecodeError, OSError):
                pass  # fall back to defaults
        else:
            self.save()  # write defaults on first run
