"""Cài đặt thuật toán Insertion Sort (Sắp xếp chèn)."""

from __future__ import annotations

from typing import List, Optional, Sequence

from core.base_sort import BaseSort, ProgressCallback, T


class InsertionSort(BaseSort[T]):
    """Thuật toán Insertion Sort kế thừa từ BaseSort."""

    def __init__(
        self,
        data: Sequence[T],
        progress_callback: Optional[ProgressCallback] = None,
        progress_interval: int = 50,
    ) -> None:
        super().__init__(data, progress_callback, progress_interval)

    def sort(self) -> List[T]:
        """Sắp xếp mảng nội bộ và trả về mảng đã sắp xếp."""
        n = len(self.array)
        if n <= 1:
            return self.array

        for i in range(1, n):
            j = i
            # Khi phần tử trước lớn hơn phần tử hiện tại, hoán đổi lùi dần về đầu mảng
            while j > 0 and self.compare(j - 1, j) > 0:
                self.swap(j - 1, j)
                j -= 1

        self.report_progress()  # Đảm bảo báo cáo tiến độ cuối cùng
        return self.array