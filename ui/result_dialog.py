# Dialog hiển thị bảng so sánh kết quả sau khi chạy xong benchmark.
 
from __future__ import annotations
 
from typing import Dict
 
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)
 
 
class ResultsDialog(QDialog):
    #Bảng so sánh kết quả cuối cùng của tất cả giải thuật.
 
    COLUMNS = ["Thuật toán", "So sánh", "Hoán đổi", "Tổng thao tác", "Thời gian (s)"]
 
    def __init__(
        self,
        results: Dict[str, dict],
        size: int,
        distribution_label: str,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.results = results
        self.size = size
        self.distribution_label = distribution_label
 
        self.setWindowTitle("Kết quả so sánh")
        self.setMinimumWidth(620)
        self.setModal(True)
 
        # Ép nền trắng cho toàn bộ dialog
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#1f2937"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#1f2937"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
 
        self._build_ui()
 
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
 
        # Thông tin lần chạy
        info = QLabel(
            f"Kích thước: {self.size:,} phần tử  ·  Kiểu dữ liệu: {self.distribution_label}"
        )
        info.setStyleSheet("font-size: 13px; color: #475569; background: transparent;")
        layout.addWidget(info)
 
        # Bảng
        table = QTableWidget()
        table.setColumnCount(len(self.COLUMNS))
        table.setHorizontalHeaderLabels(self.COLUMNS)
        table.setRowCount(len(self.results))
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.verticalHeader().setVisible(False)
        table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                gridline-color: #e5e7eb;
                font-size: 13px;
                color: #1f2937;
            }
            QTableWidget::item {
                background: #ffffff;
                color: #1f2937;
                padding: 8px 12px;
                border: none;
            }
            QTableWidget::item:selected {
                background: #ffffff;
                color: #1f2937;
            }
            QHeaderView {
                background: #ffffff;
            }
            QHeaderView::section {
                background: #ffffff;
                color: #475569;
                border: none;
                border-bottom: 1px solid #d1d5db;
                border-right: 1px solid #e5e7eb;
                padding: 8px 12px;
                font-weight: 700;
                font-size: 12px;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)
 
        for row, (algo_name, data) in enumerate(self.results.items()):
            comparisons = data["comparisons"]
            swaps = data["swaps"]
            total = comparisons + swaps
            elapsed = data["elapsed_time"]
 
            values = [
                algo_name,
                f"{comparisons:,}",
                f"{swaps:,}",
                f"{total:,}",
                f"{elapsed:.3f}",
            ]
 
            for col, text in enumerate(values):
                item = QTableWidgetItem(text)
                item.setForeground(QColor("#1f2937"))
                item.setBackground(QColor("#ffffff"))
                if col > 0:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                table.setItem(row, col, item)
 
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in range(1, len(self.COLUMNS)):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
 
        table.setFixedHeight(
            table.horizontalHeader().height()
            + table.rowHeight(0) * len(self.results)
            + 4
        )
        layout.addWidget(table)
 
        # Nút đóng
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Đóng")
        close_btn.setObjectName("PrimaryButton")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)