#Bảng biểu đồ tái sử dụng cho một thuật toán sắp xếp đơn lẻ.

from __future__ import annotations

from typing import List

import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


pg.setConfigOptions(antialias=True)


class AlgorithmPanel(QFrame):
    # Hiển thị tiến độ thời gian thực cho một thuật toán sắp xếp.

    COMPARISON_COLOR = QColor("#06b6d4")
    SWAP_COLOR = QColor("#f97316")

    def __init__(
        self,
        algorithm_name: str,
        color: str,
        max_points: int = 2500,
        parent: QFrame | None = None,
    ) -> None:
        # Tạo một bảng gồm tiêu đề, biểu đồ hai đường và bộ đếm trực tiếp.

        super().__init__(parent)
        self.algorithm_name = algorithm_name
        self.color = QColor(color)
        self.max_points = max(50, max_points)

        self._time_values: List[float] = []
        self._comparison_values: List[int] = []
        self._swap_values: List[int] = []

        self.setObjectName("AlgorithmPanel")
        self._build_ui()

    def update_progress(
        self,
        comparisons: int,
        swaps: int,
        elapsed_time: float,
    ) -> None:
        # Cập nhật bộ đếm và thêm điểm mới theo thời gian thực.

        total_operations = comparisons + swaps
        self._time_values.append(elapsed_time)
        self._comparison_values.append(comparisons)
        self._swap_values.append(swaps)

        if len(self._time_values) > self.max_points:
            self._time_values = self._time_values[-self.max_points :]
            self._comparison_values = self._comparison_values[-self.max_points :]
            self._swap_values = self._swap_values[-self.max_points :]

        self.comparisons_label.setText(f"So sánh: {comparisons:,}")
        self.swaps_label.setText(f"Hoán đổi: {swaps:,}")
        self.total_label.setText(f"Tổng: {total_operations:,}")
        self.elapsed_label.setText(f"Thời gian: {elapsed_time:.3f}s")

        self.comparisons_curve.setData(self._time_values, self._comparison_values)
        self.swaps_curve.setData(self._time_values, self._swap_values)

    def reset(self) -> None:
        #Xóa dữ liệu biểu đồ và đặt lại toàn bộ chỉ số hiển thị.

        self._time_values.clear()
        self._comparison_values.clear()
        self._swap_values.clear()

        self.comparisons_label.setText("So sánh: 0")
        self.swaps_label.setText("Hoán đổi: 0")
        self.total_label.setText("Tổng: 0")
        self.elapsed_label.setText("Thời gian: 0.000s")
        self.comparisons_curve.setData([], [])
        self.swaps_curve.setData([], [])

    def _build_ui(self) -> None:
        # Tạo các widget bảng và biểu đồ pyqtgraph.

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(14, 12, 14, 14)
        root_layout.setSpacing(10)

        self.title_label = QLabel(self.algorithm_name)
        self.title_label.setObjectName("AlgorithmTitle")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setStyleSheet(f"color: {self.color.name()};")
        root_layout.addWidget(self.title_label)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setMinimumHeight(220)
        self.plot_widget.setBackground("#ffffff")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.18)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.hideButtons()
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.setLabel("bottom", "Thời gian (s)")
        self.plot_widget.setLabel("left", "Số thao tác")
        self.plot_widget.getAxis("bottom").setPen(pg.mkPen("#94a3b8"))
        self.plot_widget.getAxis("left").setPen(pg.mkPen("#94a3b8"))
        self.plot_widget.getAxis("bottom").setTextPen(pg.mkPen("#64748b"))
        self.plot_widget.getAxis("left").setTextPen(pg.mkPen("#64748b"))

        self.legend = self.plot_widget.addLegend(offset=(12, 12))
        self.legend.setBrush(pg.mkBrush(255, 255, 255, 220))
        self.legend.setPen(pg.mkPen("#cbd5e1"))

        self.comparisons_curve = self.plot_widget.plot(
            [],
            [],
            pen=pg.mkPen(self.COMPARISON_COLOR, width=2.6),
            name="Số lần so sánh",
        )
        self.swaps_curve = self.plot_widget.plot(
            [],
            [],
            pen=pg.mkPen(self.SWAP_COLOR, width=2.6),
            name="Số lần hoán đổi",
        )
        root_layout.addWidget(self.plot_widget, stretch=1)

        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(8)

        self.comparisons_label = self._create_stat_label("So sánh: 0")
        self.swaps_label = self._create_stat_label("Hoán đổi: 0")
        self.total_label = self._create_stat_label("Tổng: 0")
        self.elapsed_label = self._create_stat_label("Thời gian: 0.000s")

        stats_layout.addWidget(self.comparisons_label)
        stats_layout.addWidget(self.swaps_label)
        stats_layout.addWidget(self.total_label)
        stats_layout.addWidget(self.elapsed_label)
        root_layout.addLayout(stats_layout)

    def _create_stat_label(self, text: str) -> QLabel:
        # Tạo một nhãn chỉ số nhỏ gọn.

        label = QLabel(text)
        label.setObjectName("StatLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMinimumWidth(110)
        return label
