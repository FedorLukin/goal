"""Точка входа для запуска плеера."""

import sys
from PyQt6.QtWidgets import QApplication

from player import PlayerWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PlayerWindow()
    window.show()

    sys.exit(app.exec())
