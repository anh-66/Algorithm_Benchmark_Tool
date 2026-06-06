"""Điểm vào ứng dụng cho Algorithm Benchmark Tool."""

from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.styles import APP_STYLESHEET


def main() -> int:
    """Chạy ứng dụng PyQt6."""

    app = QApplication(sys.argv)
    app.setApplicationName("Công cụ so sánh thuật toán sắp xếp")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
