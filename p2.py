from p1 import *  # Import any necessary modules or classes from p1

class MaxHeap:
    def __init__(self):
        # Initialize an empty list to store hospitals in the heap
        self.heap = []

    def is_empty(self):
        # Check if the heap is empty
        return len(self.heap) == 0

    def insert(self, hospital):
        # Add a new hospital to the heap
        self.heap.append(hospital)
        # Restore the heap property by moving the new element up
        self.heapify_up(len(self.heap) - 1)

    def extract_max(self):
        # Extract the hospital with the highest rating (root of the heap)
        if self.is_empty():
            return None
        
        # The max element is at the root (index 0)
        max_hospital = self.heap[0]
        # Move the last element to the root and remove the last element
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        # Restore the heap property by moving the new root down
        self.heapify_down(0)
        return max_hospital

    def max_hospital(self):
        # Get the hospital with the highest rating without removing it
        if self.is_empty():
            return None
        return self.heap[0]

    def heapify_up(self, index):
        # Restore the heap property by moving the element at 'index' up
        parent_index = (index - 1) // 2
        # Continue swapping the current element with its parent if the heap property is violated
        if index > 0 and self.heap[index]['rating'] > self.heap[parent_index]['rating']:
            # Swap the current element with its parent
            self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
            # Recursively heapify up the parent index
            self.heapify_up(parent_index)

    def heapify_down(self, index):
        # Restore the heap property by moving the element at 'index' down
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        largest = index

        # Check if the left child exists and is greater than the current element
        if (left_child_index < len(self.heap) and
                self.heap[left_child_index]['rating'] > self.heap[largest]['rating']):
            largest = left_child_index

        # Check if the right child exists and is greater than the current largest element
        if (right_child_index < len(self.heap) and
                self.heap[right_child_index]['rating'] > self.heap[largest]['rating']):
            largest = right_child_index

        # If the largest element is not the current index, swap and continue heapifying down
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            # Recursively heapify down the affected child index
            self.heapify_down(largest)

    def display_hospitals(self):
        # Display all hospitals in the heap along with their ratings
        if self.is_empty():
            print("Max Heap is empty.")
            return
        print("Max Heap (from highest to lowest rating):")
        # Iterate through the heap and display each hospital's name and rating
        for hospital in self.heap:
            print(f"Hospital: {hospital['name']}, Rating: {hospital['rating']}")
        print("")  # Print a blank line for better readability
