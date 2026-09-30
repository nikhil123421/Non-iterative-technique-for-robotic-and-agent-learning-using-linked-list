# 🤖 Autonomous Robot Path Learning using Linked Lists

> A software-only Python simulation in which an autonomous agent explores a grid and retains a successful route in a manually implemented linked list.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white) ![GUI](https://img.shields.io/badge/GUI-Tkinter-2C3E50) ![Dependencies](https://img.shields.io/badge/Dependencies-None-success) ![Project](https://img.shields.io/badge/Project-College%20DSA-orange)

## Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Linked List Path Memory](#linked-list-path-memory)
- [Algorithm](#algorithm)
- [Rewards](#rewards)
- [Non-Iterative Learning](#non-iterative-learning)
- [Complexity](#complexity)


---

## About

This project simulates an autonomous robot in a two-dimensional grid. Starting at **S**, the robot avoids obstacles **#** and tries to reach the destination **G**.

```text
S  .  .  #  .
.  #  .  #  .
.  #  .  .  .
.  .  #  .  G
```

The robot records its route using linked-list nodes. Every node stores a coordinate, the action that reached it, a reward, and a pointer to the next state. If a branch ends unsuccessfully, the robot removes that section and backtracks.

> This is an educational **linked-list-based agent learning/path-memory simulation**. It is not a physical robotics project, neural network, or full reinforcement-learning system.

## Features

- Tkinter grid visualization with animated movement
- Random environment generation and reset controls
- Deterministic, easy-to-explain decisions
- Manual singly linked-list path memory
- Dead-end detection and backtracking
- Saved-path replay without recalculating a route
- Simple reward feedback
- No hardware, database, cloud service, or external packages

## Project Structure

```text
robot_path_learning/
├── main.py             # Starts the application
├── gui.py              # Tkinter interface and animation
├── robot.py            # Agent decisions and learning process
├── environment.py      # Grid, obstacles, and valid movements
├── linked_list.py      # PathNode and PathLinkedList
├── README.md           # Project documentation
└── requirements.txt    # No third-party dependencies
```

## Quick Start

**Requirements:** Python 3.x with Tkinter (included with most Python installations).

```bash
git clone <your-repository-url>
cd robot_path_learning
python main.py
```

If you already have the project folder, run:

```bash
python main.py
```

No `pip install` command is required.

## How It Works

```text
Generate Grid → Start at S → Check valid neighbours
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
        Unvisited valid cell                    No valid cell
                 │                                 │
                 ▼                                 ▼
      Add node to linked list             Remove last node
                 │                                 │
                 ▼                                 ▼
         Goal reached?                       Backtrack
          │          │
         Yes         No ───────────────► Continue exploring
          │
          ▼
   Preserve path and replay it
```

The robot checks directions in a fixed order:

```text
Right → Down → Left → Up
```

It ignores cells outside the grid, obstacle cells, and states already visited in the current attempt. The fixed order ensures that a given grid produces the same behaviour each time.

## Linked List Path Memory

The route is not secretly stored as a Python list. `linked_list.py` provides a manual linked-list implementation:

```python
class PathNode:
    def __init__(self, x, y, action, reward):
        self.x = x
        self.y = y
        self.action = action
        self.reward = reward
        self.next = None
```

```text
Start       Right        Down           Goal
  │            │           │              │
  ▼            ▼           ▼              ▼
(0,0) ──► (0,1) ──► (1,1) ──► ... ──► (r,c)
```

| Operation | Purpose in this project |
| --- | --- |
| Add node | Save a valid state/action transition |
| Traverse | Draw the route and calculate path reward |
| Search | Check a state on the current path |
| Remove last node | Discard an unsuccessful branch |
| Clear | Start a fresh attempt |
| Follow `next` | Replay the saved route |

When the goal is reached, the linked list is kept as the learned path. Replay follows each node's `next` pointer directly; it does not search for a new route.

## Algorithm

1. Add the start coordinate to the linked list and mark it as visited.
2. Check neighbouring cells in fixed order.
3. Append the first valid unvisited cell as a node with its action and reward.
4. If that cell is the goal, retain the linked list.
5. If no valid unvisited neighbour exists, remove the tail node and return to the previous node.
6. If no move is possible at the start, report a dead end/unreachable goal.

## Rewards

| Event | Reward |
| --- | ---: |
| Normal valid move | `+1` |
| Reaching the goal | `+10` |
| Dead-end/backtracking event | `-10` |

Valid movement rewards are stored in their corresponding nodes. The GUI shows feedback accumulated during the learning attempt. Obstacles are rejected before entering them, so the robot does not intentionally collide with them.

## Non-Iterative Learning

**Non-iterative** does not mean the program contains no loops. Loops are needed to inspect neighbours, traverse linked-list nodes, and render the grid.

Here it means that learning is not repeated statistical training over epochs. There are no neural-network weights, batches, value tables, or model updates. The agent instead incrementally creates one concrete sequence of state/action transitions and retains it as a linked path memory.

> The project uses simple rewards as feedback, but it is **not reinforcement learning** because it does not learn a policy or value function from repeated episodes.

## Interface Controls

| Control | Purpose |
| --- | --- |
| **Generate Environment** | Create a random obstacle layout |
| **Reset** | Clear the current attempt and keep the grid |
| **Start Learning** | Begin animated exploration |
| **Stop** | Safely stop the animation |
| **Replay Learned Path** | Replay a successful saved route |
| **Clear Learned Path** | Remove saved nodes and reset the robot |

## Complexity

Let **V** be the number of reachable grid cells.

| Task | Complexity | Why |
| --- | ---: | --- |
| Checking neighbours | `O(1)` per state | Only four directions |
| Exploring cells | `O(V)` | A cell is visited once |
| Tail removal | `O(V)` worst case | Singly linked list locates previous tail |
| Overall worst case | `O(V²)` | Backtracking may repeatedly traverse the route |
| Space | `O(V)` | Visited set and path nodes |


