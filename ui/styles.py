#Hằng số giao diện toàn ứng dụng và stylesheet Qt.

from __future__ import annotations


ALGORITHM_COLORS = {
    "Sắp xếp nổi bọt": "#0f9f8f",
    "Sắp xếp chèn": "#d97706",
    "Sắp xếp trộn": "#2563eb",
    "Sắp xếp nhanh": "#dc2626",
}


APP_STYLESHEET = """
QMainWindow {
    background: #f6f7fb;
}

QWidget {
    color: #1f2937;
    font-family: "Segoe UI", "Inter", Arial, sans-serif;
    font-size: 13px;
}

QFrame#ControlPanel,
QFrame#AlgorithmPanel {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
}

QLabel#AlgorithmTitle {
    font-size: 16px;
    font-weight: 700;
}

QLabel#SectionLabel {
    color: #475569;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
}

QLabel#StatLabel {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    color: #334155;
    font-weight: 600;
    padding: 6px 10px;
}

QComboBox,
QSpinBox {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    min-height: 28px;
    padding: 4px 28px 4px 10px;
}

QComboBox:hover,
QComboBox:focus,
QSpinBox:hover,
QSpinBox:focus {
    border-color: #0f9f8f;
}

QComboBox::drop-down,
QSpinBox::up-button,
QSpinBox::down-button {
    border: 0;
    width: 24px;
}

QComboBox QAbstractItemView {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    selection-background-color: #dbeafe;
    selection-color: #1f2937;
}

QPushButton {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    color: #1f2937;
    font-weight: 600;
    min-height: 30px;
    padding: 6px 14px;
}

QPushButton:hover {
    border-color: #64748b;
    background: #f8fafc;
}

QPushButton:pressed {
    background: #e2e8f0;
}

QPushButton:disabled {
    background: #f1f5f9;
    border-color: #e2e8f0;
    color: #94a3b8;
}

QPushButton#PrimaryButton {
    background: #0f9f8f;
    border-color: #0f9f8f;
    color: #ffffff;
}

QPushButton#PrimaryButton:hover {
    background: #0d8f81;
    border-color: #0d8f81;
}

QPushButton[segmentButton="true"] {
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 0;
    color: #475569;
    min-width: 96px;
}

QPushButton#SegmentFirst {
    border-top-left-radius: 6px;
    border-bottom-left-radius: 6px;
}

QPushButton#SegmentLast {
    border-top-right-radius: 6px;
    border-bottom-right-radius: 6px;
}

QPushButton[segmentButton="true"]:checked {
    background: #dbeafe;
    border-color: #2563eb;
    color: #1e3a8a;
}

QStatusBar {
    background: #f6f7fb;
    color: #64748b;
}
"""
