"""
Centralised logging and unhandled-exception handler (E01-S1-07).
No unhandled exception should reach the user as a raw traceback.
"""
import logging
import sys
import traceback
from typing import Type

_LOG_FORMAT = "%(asctime)s  %(levelname)-8s  %(name)s — %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(format=_LOG_FORMAT, datefmt=_DATE_FORMAT, level=logging.INFO)


def get_logger(name: str = "gearlab") -> logging.Logger:
    """Return the named GearLab logger (default: root 'gearlab' logger)."""
    return logging.getLogger(name)


def handle_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_tb,
) -> None:
    """
    Top-level exception hook.
    Logs the full traceback at ERROR level without re-raising.
    Install with: sys.excepthook = handle_exception
    """
    log = get_logger()
    tb_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    log.error("Unhandled exception: %s\n%s", exc_value, "".join(tb_lines))


def install_exception_hook() -> None:
    """Replace sys.excepthook so all unhandled exceptions are logged."""
    sys.excepthook = handle_exception
