"""Cài đặt thuật toán Bubble Sort (Sắp xếp nổi bọt)."""

from __future__ import annotations

from typing import List, Optional, Sequence

from core.base_sort import BaseSort, ProgressCallback, T


class BubbleSort(BaseSort[T]):
    """Thuật toán Bubble Sort kế thừa từ BaseSort."""

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

        for i in range(n - 1):
            swapped = False
            for j in range(0, n - 1 - i):
                # So sánh hai phần tử liên tiếp và hoán đổi nếu phần tử trước lớn hơn phần tử sau
                if self.compare(j, j + 1) > 0:
                    self.swap(j, j + 1)
                    swapped = True
            if not swapped:
                break

        self.report_progress()  # Đảm bảo báo cáo tiến độ cuối cùng
        return self.array