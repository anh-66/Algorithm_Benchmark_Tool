"""Thanh điều khiển phía trên để tạo dữ liệu và chạy benchmark."""

from __future__ import annotations

from typing import Dict

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QWidget,
)


class ControlPanel(QFrame):
    #Thu thập kích thước mảng và kiểu dữ liệu cho lần benchmark.

    benchmark_requested = pyqtSignal(int, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        # Tạo widget bảng điều khiển.

        super().__init__(parent)
        self.setObjectName("ControlPanel")
        self.distribution_buttons: Dict[str, QPushButton] = {}
        self._build_ui()

    def selected_size(self) -> int:
        # Trả về kích thước mảng hiện được nhập.

        return self.size_input.value()

    def selected_distribution(self) -> str:
        # Trả về khóa kiểu dữ liệu đang được chọn.

        for label, button in self.distribution_buttons.items():
            if button.isChecked():
                return label
        return "Random"

    def set_running(self, is_running: bool) -> None:
        # Bật hoặc tắt điều khiển khi các luồng worker đang chạy.

        self.size_input.setEnabled(not is_running)
        for button in self.distribution_buttons.values():
            button.setEnabled(not is_running)
        self.start_button.setEnabled(not is_running)

    def _build_ui(self) -> None:
        # Xây dựng bố cục điều khiển ngang gọn nhẹ.

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(12)

        size_label = QLabel("Kích thước")
        size_label.setObjectName("SectionLabel")
        layout.addWidget(size_label)

        self.size_input = QSpinBox()
        self.size_input.setObjectName("SizeInput")
        self.size_input.setRange(1, 5000)
        self.size_input.setSingleStep(100)
        self.size_input.setValue(500)
        self.size_input.setAccelerated(True)
        self.size_input.setKeyboardTracking(False)
        self.size_input.setFixedWidth(130)
        layout.addWidget(self.size_input)

        distribution_label = QLabel("Kiểu dữ liệu")
        distribution_label.setObjectName("SectionLabel")
        layout.addWidget(distribution_label)

        self.distribution_group = QButtonGroup(self)
        self.distribution_group.setExclusive(True)

        distributions = (
            ("Random", "Ngẫu nhiên"),
            ("Nearly Sorted", "Sắp xếp một phần"),
            ("Reversed", "Đảo ngược"),
        )

        for index, (value, label) in enumerate(distributions):
            button = QPushButton(label)
            if index == 0:
                button.setObjectName("SegmentFirst")
            elif index == 2:
                button.setObjectName("SegmentLast")
            else:
                button.setObjectName("SegmentMiddle")
            button.setProperty("segmentButton", True)
            button.setCheckable(True)
            button.setChecked(index == 0)
            self.distribution_group.addButton(button)
            self.distribution_buttons[value] = button
            layout.addWidget(button)

        layout.addStretch(1)

        self.start_button = QPushButton("Tạo dữ liệu và chạy so sánh")
        self.start_button.setObjectName("PrimaryButton")
        self.start_button.clicked.connect(self._emit_benchmark_requested)
        layout.addWidget(self.start_button)

    def _emit_benchmark_requested(self) -> None:
        # Phát yêu cầu tạo dữ liệu mới và chạy tất cả thuật toán.

        self.benchmark_requested.emit(
            self.selected_size(),
            self.selected_distribution(),
        )
