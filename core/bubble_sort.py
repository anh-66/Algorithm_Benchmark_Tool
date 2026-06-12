from typing import List, TypeVar
from .base_sort import BaseSort

T = TypeVar("T")


class BubbleSort(BaseSort[T]):
    def sort(self) -> List[T]:
        n = len(self.data)
        for i in range(n - 1):
            swapped = False
            for j in range(0, n - 1 - i):
                # Nếu data[j] > data[j+1] thì swap
                if self.compare(j, j + 1):
                    self.swap(j, j + 1)
                    swapped = True
            if not swapped:
                break
        return self.data