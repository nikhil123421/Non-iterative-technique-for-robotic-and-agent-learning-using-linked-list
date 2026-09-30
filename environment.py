"""Grid creation and movement checks for the simulation."""

import random


class GridEnvironment:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.start = (0, 0)
        self.goal = (rows - 1, cols - 1)
        self.obstacles = set()

    def generate(self, obstacle_rate=0.23):
        self.obstacles.clear()
        for x in range(self.rows):
            for y in range(self.cols):
                cell = (x, y)
                if cell not in (self.start, self.goal) and random.random() < obstacle_rate:
                    self.obstacles.add(cell)

    def is_valid(self, cell):
        x, y = cell
        return (0 <= x < self.rows and 0 <= y < self.cols
                and cell not in self.obstacles)

    def neighbors(self, cell):
        """Fixed order makes the agent's decisions repeatable for one grid."""
        x, y = cell
        choices = ((x, y + 1, "Right"), (x + 1, y, "Down"),
                   (x, y - 1, "Left"), (x - 1, y, "Up"))
        return [(nx, ny, action) for nx, ny, action in choices
                if self.is_valid((nx, ny))]
