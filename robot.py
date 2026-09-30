"""Simple depth-first path learner using a linked list as its route memory."""

from linked_list import PathLinkedList


class Robot:
    def __init__(self, environment):
        self.environment = environment
        self.path = PathLinkedList()
        self.position = environment.start
        self.visited = set()
        self.status = "Ready"
        self.steps = 0
        self.session_reward = 0
        self.learning = False

    def reset(self):
        self.path.clear()
        self.position = self.environment.start
        self.visited.clear()
        self.status = "Ready"
        self.steps = 0
        self.session_reward = 0
        self.learning = False

    def start_learning(self):
        self.reset()
        self.path.add(*self.position, "Start", 0)
        self.visited.add(self.position)
        self.status = "Learning"
        self.learning = True

    def learning_step(self):
        """Do one visible DFS decision; the GUI schedules later steps."""
        if not self.learning:
            return self.status

        for x, y, action in self.environment.neighbors(self.position):
            next_cell = (x, y)
            if next_cell not in self.visited:
                reward = 10 if next_cell == self.environment.goal else 1
                self.path.add(x, y, action, reward)
                self.position = next_cell
                self.visited.add(next_cell)
                self.steps += 1
                self.session_reward += reward
                if next_cell == self.environment.goal:
                    self.status = "Goal Reached"
                    self.learning = False
                return self.status

        # No unvisited neighbor: erase this unsuccessful part of the route.
        if self.position == self.environment.start:
            self.status = "Dead End"
            self.learning = False
            self.session_reward -= 10
            return self.status

        self.path.remove_last()
        parent = self.path.last()
        self.position = (parent.x, parent.y)
        self.steps += 1
        self.session_reward -= 10
        return "Backtracking"

    def stop(self):
        if self.learning:
            self.learning = False
            self.status = "Stopped"
