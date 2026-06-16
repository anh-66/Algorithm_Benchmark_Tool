"""Cài đặt thuật toán Merge Sort (Sắp xếp trộn)."""

from __future__ import annotations

from typing import List, Optional, Sequence

from core.base_sort import BaseSort, ProgressCallback, T


class MergeSort(BaseSort[T]):
    """Thuật toán Merge Sort kế thừa từ BaseSort."""

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
        self._merge_sort(0, len(self.array) - 1)
        self.report_progress()  # Đảm bảo báo cáo tiến độ cuối cùng
        return self.array

    def _merge_sort(self, left: int, right: int) -> None:
        """Đệ quy phân chia mảng để sắp xếp trộn."""
        if left < right:
            middle = (left + right) // 2
            self._merge_sort(left, middle)
            self._merge_sort(middle + 1, right)
            self._merge(left, middle, right)

    def _merge(self, left: int, middle: int, right: int) -> None:
        """Trộn hai phần đã sắp xếp của mảng sử dụng compare_values()."""
        # Tạo danh sách tạm cho phần bên trái và bên phải
        left_part = self.array[left : middle + 1]
        right_part = self.array[middle + 1 : right + 1]

        i = 0  # Chỉ mục danh sách bên trái
        j = 0  # Chỉ mục danh sách bên phải
        k = left  # Chỉ mục ghi nhận lại vào self.array

        # Trộn các phần tử cho đến khi một trong hai danh sách tạm hết phần tử
        while i < len(left_part) and j < len(right_part):
            # So sánh hai giá trị tạm bằng compare_values
            if self.compare_values(left_part[i], right_part[j]) <= 0:
                self.array[k] = left_part[i]
                i += 1
            else:
                self.array[k] = right_part[j]
                j += 1
            k += 1

        # Sao chép các phần tử còn lại của left_part (nếu có)
        while i < len(left_part):
            self.array[k] = left_part[i]
            i += 1
            k += 1

        # Sao chép các phần tử còn lại của right_part (nếu có)
        while j < len(right_part):
            self.array[k] = right_part[j]
            j += 1
            k += 1
