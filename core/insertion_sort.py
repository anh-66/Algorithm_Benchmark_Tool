from typing import List, TypeVar
from .base_sort import BaseSort

T = TypeVar("T")


class InsertionSort(BaseSort[T]):
    def sort(self) -> List[T]:
        n = len(self.data)
        for i in range(1, n):
            j = i
            # Khi data[j-1] > data[j] thì swap lùi dần về đầu
            while j > 0 and self.compare(j - 1, j):
                self.swap(j - 1, j)
                j -= 1
        return self.data