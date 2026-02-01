import numpy as np
import math
import time
import sys


class HeapSort:
    def __init__(self):
        self.inf = 0
        pass
    def heapify(self, array, i):
        if (i == 0): return
        node = i

        while(node > 0):
            parent = (node - 1) // 2
            if (array[parent] > array[node]):
                array[parent], array[node] = array[node], array[parent]
                node = parent
            else:
                break     

    def pop(self, array):
        if (len(array) == 0): return None
        popped_value = array[0]
        array[0] = self.inf

        node = 0
        while(True):
            left = 2 * node + 1
            right = 2 * node + 2

            if (left >= len(array) and right >= len(array)): break

            left_value, right_value = self.inf, self.inf + 1
            if (left < len(array)): left_value = array[left]
            if (right < len(array)): right_value = array[right]

            if (left_value < right_value):
                array[node], array[left] = array[left], array[node]
                node = left
            else:
                array[node], array[right] = array[right], array[node]
                node = right            

        return popped_value
            
    def sort(self, array):
        n = len(array)
        self.inf = np.max(array) + 1

        for i in range(0, n):
            self.heapify(array, i)
        sorted_array = np.empty(n)

        for i in range(n):
            sorted_array[i] = self.pop(array)
        return sorted_array

class GeminiHeapSort:
    def heapify(self, arr, n, i):
        """
        Hàm này duy trì tính chất Max-Heap (Sift-Down).
        n: kích thước của heap cần xét
        i: chỉ số node đang xét
        """
        largest = i  # Khởi tạo largest là root
        left = 2 * i + 1     # left = 2*i + 1
        right = 2 * i + 2    # right = 2*i + 2
  
        # Kiểm tra xem con trái có tồn tại và lớn hơn root không
        if left < n and arr[left] > arr[largest]:
            largest = left
  
        # Kiểm tra xem con phải có tồn tại và lớn hơn largest hiện tại không
        if right < n and arr[right] > arr[largest]:
            largest = right
  
        # Nếu largest không phải là root, đổi chỗ
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]  # Swap
  
            # Đệ quy heapify tiếp cây con vừa bị ảnh hưởng
            self.heapify(arr, n, largest)
  
    def sort(self, array):
        n = len(array)
  
        # 1. Xây dựng Max-Heap (Build Heap)
        # Bắt đầu từ node cha cuối cùng (n//2 - 1) lùi về 0
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(array, n, i)
  
        # 2. Trích xuất từng phần tử (Extract elements)
        for i in range(n - 1, 0, -1):
            # Di chuyển root (lớn nhất) về cuối mảng
            array[i], array[0] = array[0], array[i]
            
            # Gọi heapify trên mảng đã giảm kích thước (chỉ xét đến i)
            # để đưa phần tử lớn nhất còn lại lên đầu
            self.heapify(array, i, 0)
            
        return array
    
if (__name__ == "__main__"):
    sample = np.array([5, 3, 2, 4, 1], dtype = np.int64)
    sample = Heapsort().sort(sample)
    print(sample)

    sample = np.array([5, 3, 2, 4, 1], dtype = np.float32)
    sample = Heapsort().sort(sample)
    print(sample)

    sample = np.random.randint(0, 1000, 10)
    sample = Heapsort().sort(sample)
    print(sample)

    sample = np.random.randint(0, 1000, 100000)
    start = time.time()
    sample = Heapsort().sort(sample)
    ending = time.time()

    times = ending - start
    print(times)