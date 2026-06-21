"""Cửa sổ ứng dụng chính cho Algorithm Benchmark Tool."""

from __future__ import annotations

from functools import partial
from typing import Dict, List, Optional, Type

from PyQt6.QtWidgets import (
    QGridLayout,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.base_sort import BaseSort
from core.bubble_sort import BubbleSort
from core.insertion_sort import InsertionSort
from core.merge_sort import MergeSort
from core.quick_sort import QuickSort
from ui.algorithm_panel import AlgorithmPanel
from ui.control_panel import ControlPanel
from ui.styles import ALGORITHM_COLORS
from utils.data_generator import generate_array
from workers.sort_worker import SortWorker
from ui.result_dialog import ResultsDialog


class MainWindow(QMainWindow):
    #Điều phối giao diện, tạo dữ liệu và các worker benchmark.

    MICRO_DELAY_SECONDS = 0.0005

    ALGORITHMS: tuple[tuple[str, Type[BaseSort[int]]], ...] = (
        ("Sắp xếp nổi bọt", BubbleSort),
        ("Sắp xếp chèn", InsertionSort),
        ("Sắp xếp trộn", MergeSort),
        ("Sắp xếp nhanh", QuickSort),
    )

    DISTRIBUTION_LABELS = {
        "Random": "Ngẫu nhiên",
        "Nearly Sorted": "Gần sắp xếp",
        "Reversed": "Đảo ngược",
    }

    def __init__(self) -> None:
        # Tạo cửa sổ benchmark đầy đủ.

        super().__init__()
        self.setWindowTitle("Công cụ so sánh thuật toán sắp xếp")
        self.setMinimumSize(1180, 760)

        self.current_data: List[int] = []
        self.current_size: Optional[int] = None
        self.current_distribution: Optional[str] = None
        self.panels: Dict[str, AlgorithmPanel] = {}
        self.workers: Dict[str, SortWorker] = {}
        self.completed_count = 0
        self.benchmark_results: Dict[str, dict] = {}

        self._build_ui()

        initial_size = self.control_panel.selected_size()
        initial_distribution = self.control_panel.selected_distribution()
        self._generate_data(initial_size, initial_distribution, show_message=False)

    def start_benchmark(self, size: int, distribution: str) -> None:
        # Tạo dữ liệu mới và khởi động cả bốn worker sắp xếp.

        if self.workers:
            return

        self._generate_data(size, distribution, show_message=False)

        self.completed_count = 0
        self.benchmark_results.clear()  #xóa kết quả cũ
        self.control_panel.set_running(True)
        distribution_label = self._distribution_label(distribution)
        self.statusBar().showMessage(
            f"Đã tạo {size:,} phần tử kiểu {distribution_label}. Đang chạy so sánh..."
        )

        progress_interval = self._progress_interval_for_size(size)

        for algorithm_name, sort_class in self.ALGORITHMS:
            panel = self.panels[algorithm_name]
            panel.reset()

            worker = SortWorker(
                algorithm_name=algorithm_name,
                sort_class=sort_class,
                input_array=self.current_data,
                progress_interval=progress_interval,
                delay=self.MICRO_DELAY_SECONDS,
                parent=self,
            )
            worker.progress_updated.connect(panel.update_progress)
            worker.result_ready.connect(self._handle_result_ready)
            worker.error_occurred.connect(self._handle_worker_error)
            worker.cancelled.connect(self._handle_worker_cancelled)
            worker.finished.connect(partial(self._cleanup_worker, algorithm_name))
            self.workers[algorithm_name] = worker

        for worker in self.workers.values():
            worker.start()

    def closeEvent(self, event) -> None:  # type: ignore[override]
        # Yêu cầu các worker đang chạy dừng trước khi cửa sổ đóng.

        for worker in list(self.workers.values()):
            worker.cancel()
            worker.wait(1500)
        super().closeEvent(event)

    def _build_ui(self) -> None:
        # Tạo bố cục cửa sổ chính.

        central_widget = QWidget()
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(14, 14, 14, 10)
        root_layout.setSpacing(14)

        self.control_panel = ControlPanel()
        self.control_panel.benchmark_requested.connect(self.start_benchmark)
        root_layout.addWidget(self.control_panel)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setHorizontalSpacing(14)
        grid_layout.setVerticalSpacing(14)

        for index, (algorithm_name, _) in enumerate(self.ALGORITHMS):
            row = index // 2
            column = index % 2
            panel = AlgorithmPanel(
                algorithm_name,
                ALGORITHM_COLORS[algorithm_name],
            )
            self.panels[algorithm_name] = panel
            grid_layout.addWidget(panel, row, column)
            grid_layout.setRowStretch(row, 1)
            grid_layout.setColumnStretch(column, 1)

        root_layout.addLayout(grid_layout, stretch=1)
        self.setCentralWidget(central_widget)
        self.statusBar().showMessage("Sẵn sàng")

    def _generate_data(
        self,
        size: int,
        distribution: str,
        show_message: bool,
    ) -> None:
        # Tạo và lưu dữ liệu benchmark cho kịch bản đã chọn.

        self.current_data = generate_array(size, distribution)
        self.current_size = size
        self.current_distribution = distribution

        for panel in self.panels.values():
            panel.reset()

        if show_message:
            distribution_label = self._distribution_label(distribution)
            self.statusBar().showMessage(
                f"Đã tạo {size:,} phần tử với kiểu dữ liệu {distribution_label}.",
                4000,
            )

    def _handle_result_ready(
        self,
        algorithm_name: str,
        sorted_array: list,
        comparisons: int,
        swaps: int,
        elapsed_time: float,
    ) -> None:
        # LƯu số liệu cuối cùng từ worker hoàn thành thành công.

        del sorted_array
        #lưu lại thay vì del hết
        self.benchmark_results[algorithm_name] = {
            "comparisons": comparisons,
            "swaps": swaps,
            "elapsed_time": elapsed_time,
        }
        self._mark_worker_completed()

    def _handle_worker_error(self, algorithm_name: str, message: str) -> None:
        # Ghi nhận lỗi worker và tiếp tục tăng bộ đếm hoàn thành.

        QMessageBox.critical(
            self,
            "Lỗi khi chạy so sánh",
            f"{algorithm_name} gặp lỗi:\n{message}",
        )
        self._mark_worker_completed()

    def _handle_worker_cancelled(self, algorithm_name: str) -> None:
        # Xử lý hủy nhẹ nhàng từ một worker.

        self.statusBar().showMessage(f"{algorithm_name} đã bị hủy.", 4000)
        self._mark_worker_completed()

    def _mark_worker_completed(self) -> None:
        # Tiến trạng thái hoàn thành khi tất cả worker đã chạy xong.

        self.completed_count += 1
        if self.completed_count < len(self.ALGORITHMS):
            return

        self.control_panel.set_running(False)
        self.statusBar().showMessage("Đã hoàn tất so sánh.", 4000)

        # hiển thị bảng kết quả nếu có đủ dữ liệu 
        if self.benchmark_results:
            dialog = ResultsDialog(
                results=self.benchmark_results,
                size=self.current_size or 0,
                distribution_label=self._distribution_label(self.current_distribution),
                parent=self,
            )
            dialog.exec()

    def _cleanup_worker(self, algorithm_name: str) -> None:
        # Ngắt kết nối tín hiệu và xóa worker sau khi luồng hoàn tất.

        worker = self.workers.pop(algorithm_name, None)
        if worker is None:
            return

        for signal in (
            worker.progress_updated,
            worker.result_ready,
            worker.error_occurred,
            worker.cancelled,
            worker.finished,
        ):
            try:
                signal.disconnect()
            except TypeError:
                pass

        worker.deleteLater()

    def _distribution_label(self, distribution: Optional[str]) -> str:
        # Trả về tên tiếng Việt của kiểu dữ liệu.

        if distribution is None:
            return "Chưa chọn"
        return self.DISTRIBUTION_LABELS.get(distribution, distribution)

    @staticmethod
    def _progress_interval_for_size(size: int) -> int:
        # Chọn khoảng tiến độ phù hợp để vẫn mượt cho dữ liệu lớn.

        if size <= 100:
            return 5
        if size <= 500:
            return 25
        if size <= 1000:
            return 100
        return 1000
