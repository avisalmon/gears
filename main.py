"""
GearLab — Interactive Gear & Belt Simulator
Entry point. Run with: python main.py
"""
import sys
from PyQt6.QtWidgets import QApplication
from gearlab.app import GearLabApp
from gearlab.logger import install_exception_hook


def main() -> None:
    install_exception_hook()
    app = QApplication(sys.argv)
    app.setApplicationName("GearLab")
    app.setApplicationVersion("0.1.0")
    window = GearLabApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
