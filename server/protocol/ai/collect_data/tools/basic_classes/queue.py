class Queue:
    def __init__(self, max_items: int) -> None:
        """
        Initialize a queue with a maximum capacity of max_items.

        Args:
            max_items (int): Maximum number of items that can be in the queue (not included).
        """
        # Initialize the available list with integers from 0 to max_items-1.
        self.available = [i for i in range(max_items)]

    def get(self) -> int:
        """
        Get the next available ID in the queue.

        Returns:
            int: The next available ID in the queue, or -1 if the maximum capacity has been reached.
        """
        # If the available list is empty, return -1 to indicate that the maximum capacity has been reached.
        if len(self.available) == 0:
            return -1
        # Remove and return the first item in the available list, which represents the next available ID in the queue.
        return self.available.pop(0)

    def free(self, id: int) -> None:
        """
        Add an ID to the queue to mark it as available.

        Args:
            id (int): The ID to be marked as available.
        """
        # Add the ID to the end of the available list, indicating that it is now available in the queue.
        self.available.append(id)

    def is_available(self) -> bool:
        """
        Check whether there are any available IDs in the queue.

        Returns:
            bool: True if there are available IDs in the queue, False otherwise.
        """
        # Return True if the available list is not empty, indicating that there are available IDs in the queue.
        return len(self.available) != 0
