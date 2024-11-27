class Node:
    def __init__(self, value):
        # Initialize a node with a value and set its next reference to None.
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        # Initialize an empty stack with a 'top' pointer and a 'size' counter.
        self.top = None
        self.size = 0

    def push(self, value):
        # Create a new node with the given value.
        new_node = Node(value)
        # If the stack is empty, set the new node as the top.
        if self.size == 0:
            self.top = new_node
        else:
            # Otherwise, link the new node to the current top and update the top.
            new_node.next = self.top
            self.top = new_node
        # Increment the size of the stack.
        self.size += 1
        return True

    def pop(self):
        # Remove and return the value of the top node.
        if self.size == 0:
            return None  # Return None if the stack is empty.
        # Store the current top node.
        temp = self.top
        # Move the top pointer to the next node.
        self.top = self.top.next
        # Disconnect the popped node from the stack.
        temp.next = None
        # Decrement the size of the stack.
        self.size -= 1
        return temp.value

    def peek(self):
        """Return the value of the top node without popping."""
        # If the stack is empty, return None.
        if self.size == 0:
            return None
        # Return the value of the top node.
        return self.top.value

    def is_empty(self):
        # Check if the stack is empty by comparing the size to 0.
        return self.size == 0

    def get_size(self):
        # Return the number of elements in the stack.
        return self.size

class SearchHistory:
    def __init__(self):
        # Initialize a search history using a stack to store search details.
        self.history_stack = Stack()

    def push_search(self, search_details):
        """Push a new search detail onto the history stack."""
        # Add a new search detail to the history stack.
        self.history_stack.push(search_details)

    def pop_search(self):
        """Pop the last search detail from the history stack."""
        # Remove and return the most recent search detail from the history stack.
        return self.history_stack.pop()

    def view_history(self):
        """View all past searches."""
        # Collect all search details from the stack into a list.
        history = []
        # Start from the top of the stack.
        current = self.history_stack.top
        # Traverse through the stack to collect each search detail.
        while current is not None:
            history.append(current.value)
            current = current.next
        # Return the list of all past search details.
        return history

    def get_last_search(self):
        """Get the last search (top of the stack)."""
        # Return the most recent search detail without removing it.
        return self.history_stack.peek()
