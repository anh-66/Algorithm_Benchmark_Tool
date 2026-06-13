import time
from PyQt6.QtCore import QThread, pyqtSignal


class SortWorker(QThread):
    """
    Worker thread chạy thuật toán sắp xếp trên luồng nền (non-blocking).
    Kế thừa từ QThread để tích hợp với vòng lặp sự kiện PyQt6.
    """
    
    # Định nghĩa các signal theo yêu cầu
    progress_updated = pyqtSignal(int, int, float)   # (comparisons, swaps, elapsed_time)
    result_ready = pyqtSignal(str, list, int, int, float) # (name, sorted_array, comparisons, swaps, elapsed_time)
    error_occurred = pyqtSignal(str, str)            # (name, error_message)
    cancelled = pyqtSignal(str)                   # (name)

    def __init__(self, sort_class, input_array, delay=0, progress_interval=1000):
        """
        Khởi tạo Worker.
        
        :param sort_class: Lớp thuật toán sắp xếp (ví dụ: BubbleSort, QuickSort).
        :param input_array: Danh sách cần sắp xếp.
        :param delay: Thời gian chờ giữa các bước cập nhật tiến độ (giây).
        :param progress_interval: Số bước/tác vụ tối thiểu giữa các lần emit signal tiến độ.
        """
        super().__init__()
        self.sort_class = sort_class
        self.input_array = input_array
        self.delay = delay
        self.progress_interval = progress_interval

    def run(self):
        """
        Phương thức chính được gọi khi thread khởi động (start).
        Chứa logic chạy thuật toán và xử lý signal.
        """
        # 1. Lấy thời gian bắt đầu
        start_time = time.perf_counter()
        algorithm_name = self.sort_class.__name__

        # 2. Emit trạng thái khởi tạo (0%)
        self.progress_updated.emit(0, 0, 0.0)

        # 3. Định nghĩa hàm callback để cập nhật tiến độ ra bên ngoài luồng
        def emit_progress(comparisons, swaps):
            # Tính thời gian trôi qua
            current_elapsed = time.perf_counter() - start_time
            
            # Emit signal tiến độ
            self.progress_updated.emit(comparisons, swaps, current_elapsed)

            # Xử lý delay (tạo hiệu ứng animation chậm nếu cần)
            if self.delay > 0:
                time.sleep(self.delay)

            # Kiểm tra yêu cầu hủy từ main thread
            if self.isInterruptionRequested():
                raise InterruptedError("Operation cancelled by user")

        # 4. Try-Except để bắt lỗi và phát signal tương ứng
        try:
            # Khởi tạo đối tượng sorter
            sorter = self.sort_class(
                self.input_array, 
                progress_callback=emit_progress, 
                progress_interval=self.progress_interval
            )
            
            # Chạy thuật toán
            sorted_array = sorter.sort()
            
            # Tính tổng thời gian hoàn thành
            elapsed_time = time.perf_counter() - start_time

            # Emit kết quả thành công
            self.result_ready.emit(
                algorithm_name, 
                sorted_array, 
                sorter.comparisons, 
                sorter.swaps, 
                elapsed_time
            )

        except InterruptedError:
            # Xử lý khi người dùng yêu cầu hủy (Cancel)
            self.cancelled.emit(algorithm_name)

        except Exception as e:
            # Xử lý các lỗi khác (Lỗi logic, thiếu bộ nhớ, v.v.)
            self.error_occurred.emit(algorithm_name, str(e))

    def cancel(self):
        """
        Phương thức để yêu cầu dừng worker một cách graceful.
        """
        self.requestInterruption()