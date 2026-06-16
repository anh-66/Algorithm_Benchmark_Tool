"""Cài đặt thuật toán Quick Sort (Sắp xếp nhanh) với pivot ngẫu nhiên."""

from __future__ import annotations

import random
from typing import List, Optional, Sequence

from core.base_sort import BaseSort, ProgressCallback, T


class QuickSort(BaseSort[T]):
    """Thuật toán Quick Sort kế thừa từ BaseSort."""

    def __init__(
        self,
        data: Sequence[T],
        progress_callback: Optional[ProgressCallback] = None,
        progress_interval: int = 50,
    ) -> None:
        super().__init__(data, progress_callback, progress_interval)

    def sort(self) -> List[T]:
        """Sắp xếp mảng nội bộ và trả về mảng đã sắp xếp."""
        if not self.array:
            return self.array
        self._quick_sort(0, len(self.array) - 1)
        self.report_progress()  # Đảm bảo báo cáo tiến độ cuối cùng
        return self.array

    def _quick_sort(self, low: int, high: int) -> None:
        """Đệ quy sắp xếp nhanh trên các phân đoạn mảng."""
        if low < high:
            pivot_index = self._partition(low, high)
            self._quick_sort(low, pivot_index - 1)
            self._quick_sort(pivot_index + 1, high)

    def _partition(self, low: int, high: int) -> int:
        """Phân hoạch mảng sử dụng pivot ngẫu nhiên.
        
        Sử dụng hai con trỏ: smaller_index và current_index.
        """
        # Chọn pivot ngẫu nhiên giữa low và high
        pivot_idx = random.randint(low, high)
        # Hoán đổi pivot về cuối phân đoạn (vị trí high) để chuẩn bị phân hoạch
        self.swap(pivot_idx, high)
        
        pivot_val = self.array[high]
        smaller_index = low - 1  # Con trỏ cho các phần tử nhỏ hơn hoặc bằng pivot

        # Duyệt từ low đến high - 1 để phân loại các phần tử
        for current_index in range(low, high):
            # So sánh phần tử hiện tại với pivot
            if self.compare_values(self.array[current_index], pivot_val) <= 0:
                smaller_index += 1
                self.swap(smaller_index, current_index)

        # Đưa pivot về đúng vị trí của nó
        self.swap(smaller_index + 1, high)
        return smaller_index + 1
