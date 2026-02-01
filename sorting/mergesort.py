import numpy as np
import pandas as pd
import copy
import random
import time

class MergeSort:
    def __init__(self):
        self.inf = 0
        pass

    def merge(self, left_array, right_array):
        """A Function to merge two sorted numpy arrays"""
        left_ptr, right_ptr, result_ptr = 0, 0, 0

        len_left, len_right = len(left_array), len(right_array)
        len_total = len_left + len_right
        
        merged_array = np.empty(len_total, dtype = left_array.dtype)

        while(left_ptr < len_left or right_ptr < len_right):
            left_value, right_value = self.inf, self.inf

            if (left_ptr < len_left): left_value = left_array[left_ptr]
            if (right_ptr < len_right): right_value = right_array[right_ptr]
            
            merged_array[result_ptr] = min(left_value, right_value)
            result_ptr += 1
            
            if (left_value < right_value):
                left_ptr += 1
            else:
                right_ptr += 1

        return merged_array
    
    def sort(self, array):
        n = len(array)
        self.inf = np.max(array) + 1

        if (n == 1): return array

        half_length = 1

        while(half_length < n):
            for i in range(0, n, 2 * half_length):

                array[i:i + 2 * half_length] = self.merge(array[i:i+half_length],
                                                           array[i+half_length:i + 2 * half_length])
            half_length *= 2
        return array

class GeminiMergeSort:
    def merge(self, left_array, right_array):
        """Hàm trộn hai mảng đã sắp xếp thành một mảng mới"""
        n_left = len(left_array)
        n_right = len(right_array)
        total_len = n_left + n_right
        
        # 1. Cấp phát trước bộ nhớ (Pre-allocation) - Quan trọng nhất!
        # Dùng dtype của mảng gốc để đảm bảo tính nhất quán (int/float)
        merged_array = np.empty(total_len, dtype=left_array.dtype)
        
        i = 0 # Con trỏ mảng trái
        j = 0 # Con trỏ mảng phải
        k = 0 # Con trỏ mảng kết quả

        # 2. So sánh và điền vào mảng kết quả
        while i < n_left and j < n_right:
            if left_array[i] <= right_array[j]:
                merged_array[k] = left_array[i]
                i += 1
            else:
                merged_array[k] = right_array[j]
                j += 1
            k += 1
            
        # 3. Xử lý phần dư (Thay thế cho logic self.inf)
        # Nếu mảng trái còn, điền nốt
        while i < n_left:
            merged_array[k] = left_array[i]
            i += 1
            k += 1
            
        # Nếu mảng phải còn, điền nốt
        while j < n_right:
            merged_array[k] = right_array[j]
            j += 1
            k += 1
            
        return merged_array

    def sort(self, array):
        # Chuyển đổi sang numpy array nếu đầu vào là list để tránh lỗi
        if not isinstance(array, np.ndarray):
            array = np.array(array)
            
        n = len(array)
        if n <= 1: return array

        # Thuật toán Bottom-up (Iterative)
        width = 1
        while width < n:
            # Duyệt qua từng cặp mảng con
            for i in range(0, n, 2 * width):
                # Xác định các điểm cắt
                left = i
                mid = min(i + width, n)
                right = min(i + 2 * width, n)
                
                # Trộn hai phần: [left:mid] và [mid:right]
                # Lưu ý: Slicing trong numpy tạo view, nhưng merge trả về mảng mới
                # nên ta gán lại vào mảng gốc.
                merged = self.merge(array[left:mid], array[mid:right])
                
                # Gán ngược lại vào mảng gốc
                array[left:right] = merged
                
            width *= 2
            
        return array


if (__name__ == "__main__"):
    sample = np.array([5, 3, 2, 4, 1], dtype = np.int64)
    sample = GeminiMergeSort().sort(sample)
    print(sample)

    sample = np.array([5, 3, 2, 4, 1], dtype = np.float32)
    sample = GeminiMergeSort().sort(sample)
    print(sample)

    array = [5, 3, 2, 4, 1]
    sample = GeminiMergeSort().sort(sample)
    print(sample)

    sample = np.random.randint(0, 1000, 10)
    sample = GeminiMergeSort().sort(sample)
    print(sample)

    original = np.random.randint(0, 1000, 100000)

    sample = copy.deepcopy(original)
    start = time.time()
    sample = GeminiMergeSort().sort(sample)
    ending = time.time()

    times = ending - start
    print(times)

    sample = copy.deepcopy(original)
    start = time.time()
    sample = MergeSort().sort(sample)
    ending = time.time()

    times2 = ending - start
    print(times2)

