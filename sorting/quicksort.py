import numpy as np

class QuickSort:
    def __init__(self):
        self.inf = 0
        pass

    def partition(self, array, low, high):
        """A Function to find pivot of an array"""
        rand_ind = np.random.randint(low, high + 1)
        array[high], array[rand_ind] = array[rand_ind], array[high]
        
        pivot_index = high
        pivot = array[pivot_index]

        for i in range(low, high + 1):
            if (array[i] < pivot):
                array[i], array[low] = array[low], array[i]
                low += 1
        array[low], array[pivot_index] = array[pivot_index], array[low]
        return low
    def divide_and_conquer(self, array, low, high):
        if (low < high):
            pivot_index = self.partition(array, low, high)
            self.divide_and_conquer(array, low, pivot_index - 1)
            self.divide_and_conquer(array, pivot_index + 1, high)

    def sort(self, array):        
        if (len(array) == 1): return array
        self.divide_and_conquer(array, 0, len(array) - 1)
        return array