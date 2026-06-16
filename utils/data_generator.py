import random
from typing import List, Optional

def _validate_size(size: int) -> None:
    """Kiểm tra giá trị size hợp lệ."""
    if size < 0:
        raise ValueError("size must be non-negative.")

def generate_random(size: int, min_value: int = 1, max_value: Optional[int] = None) -> List[int]:
    """Tạo mảng số nguyên ngẫu nhiên."""
    _validate_size(size)
    
    if max_value is None:
        max_value = size * 10
        
    if max_value < min_value:
        raise ValueError("max_value must be greater than or equal to min_value.")
        
    return [random.randint(min_value, max_value) for _ in range(size)]

def generate_nearly_sorted(size: int, disorder_swaps: Optional[int] = None) -> List[int]:
    """Tạo mảng gần sắp xếp (tăng dần rồi hoán đổi ngẫu nhiên một số lần)."""
    _validate_size(size)
    
    if size == 0:
        return []
        
    # Tạo mảng sắp xếp: [1, 2, 3, ..., size]
    arr = list(range(1, size + 1))
    
    if disorder_swaps is None:
        disorder_swaps = max(1, size // 20)
        
    # Thực hiện hoán đổi
    for _ in range(disorder_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
        
    return arr

def generate_reversed(size: int) -> List[int]:
    """Tạo mảng đảo ngược (giảm dần)."""
    _validate_size(size)
    
    # Tạo mảng giảm dần: [size, size-1, ..., 2, 1]
    return list(range(size, 0, -1))

def generate_array(size: int, case_type: str, min_value: int = 1, max_value: Optional[int] = None) -> List[int]:
    """Wrapper chính để tạo dữ liệu, lựa chọn kiểu dữ liệu dựa trên case_type."""
    _validate_size(size)
    
    # Chuẩn hóa case_type
    normalized_type = case_type.strip().casefold().replace("_", " ")
    
    # Điều phối hàm dựa trên loại dữ liệu yêu cầu
    if normalized_type == "random":
        return generate_random(size, min_value, max_value)
    elif normalized_type == "nearly sorted":
        return generate_nearly_sorted(size)
    elif normalized_type == "reversed":
        return generate_reversed(size)
    else:
        valid_cases = ["Random", "Nearly Sorted", "Reversed"]
        raise ValueError(f"Invalid case_type: '{case_type}'. Expected one of: {', '.join(valid_cases)}")
