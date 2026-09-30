"""A small linked list used as the robot's path memory."""


class PathNode:
    def __init__(self, x, y, action, reward):
        self.x = x
        self.y = y
        self.action = action
        self.reward = reward
        self.next = None


class PathLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def add(self, x, y, action, reward):
        node = PathNode(x, y, action, reward)
        if self.head is None:
            self.head = node
        else:
            self.tail.next = node
        self.tail = node
        self.length += 1
        return node

    def contains(self, x, y):
        current = self.head
        while current:
            if current.x == x and current.y == y:
                return True
            current = current.next
        return False

    def remove_last(self):
        """Remove the latest route state when DFS abandons a branch."""
        if self.head is None:
            return None
        if self.head is self.tail:
            removed = self.head
            self.head = self.tail = None
            self.length = 0
            return removed

        current = self.head
        while current.next is not self.tail:
            current = current.next
        removed = self.tail
        current.next = None
        self.tail = current
        self.length -= 1
        return removed

    def clear(self):
        self.head = None
        self.tail = None
        self.length = 0

    def last(self):
        return self.tail

    def nodes(self):
        """Return a normal list only for drawing/reporting, not as memory."""
        result = []
        current = self.head
        while current:
            result.append(current)
            current = current.next
        return result

    def total_reward(self):
        total = 0
        current = self.head
        while current:
            total += current.reward
            current = current.next
        return total
