"""Lớp cơ sở chung cho tất cả cài đặt thuật toán sắp xếp thủ công."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Generic, List, Optional, Sequence, TypeVar


T = TypeVar("T")
ProgressCallback = Callable[[int, int], None]


class BaseSort(ABC, Generic[T]):
   
    def __init__(
        self,
        data: Sequence[T],
        progress_callback: Optional[ProgressCallback] = None,
        progress_interval: int = 50,
    ) -> None:
        
        self.array: List[T] = list(data)
        self.comparisons: int = 0
        self.swaps: int = 0

        self._progress_callback = progress_callback
        self._progress_interval = max(1, progress_interval)
        self._operations_since_report = 0

    @abstractmethod
    def sort(self) -> List[T]:
        """Sắp xếp mảng nội bộ và trả về nó."""

    def compare(self, i: int, j: int) -> int:
        """So sánh hai vị trí trong mảng và đếm một phép so sánh.

        Returns:
            -1 nếu ``array[i] < array[j]``, 0 nếu bằng, và 1 nếu lớn hơn.
        """

        self.comparisons += 1
        self._record_operation()
        return self._compare_raw(self.array[i], self.array[j])

    def compare_values(self, left: T, right: T) -> int:
        """So sánh hai giá trị và đếm một phép so sánh.

        Hàm trợ giúp này hữu ích cho các thuật toán như merge sort và quick sort
        khi các giá trị so sánh nằm trong danh sách tạm hoặc biến pivot.
        """

        self.comparisons += 1
        self._record_operation()
        return self._compare_raw(left, right)

    def swap(self, i: int, j: int) -> None:
        """Hoán đổi hai vị trí trong mảng và đếm một phép hoán đổi."""

        self.array[i], self.array[j] = self.array[j], self.array[i]
        self.swaps += 1
        self._record_operation()

    def report_progress(self) -> None:
        """Ép gọi lại tiến độ với các bộ đếm hiện tại."""

        if self._progress_callback is not None:
            self._progress_callback(self.comparisons, self.swaps)
        self._operations_since_report = 0

    def _record_operation(self) -> None:
        """Kích hoạt cập nhật tiến độ sau khi đạt đủ số phép đo."""

        self._operations_since_report += 1
        if self._operations_since_report >= self._progress_interval:
            self.report_progress()

    @staticmethod
    def _compare_raw(left: T, right: T) -> int:
        """Trả về quan hệ thứ tự giữa hai giá trị có thể so sánh."""

        if left < right:
            return -1
        if left > right:
            return 1
        return 0