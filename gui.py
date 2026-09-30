"""Tkinter user interface and animation."""

import tkinter as tk
from tkinter import messagebox

from environment import GridEnvironment
from robot import Robot


class RobotPathApp:
    CELL = 48

    def __init__(self, root):
        self.root = root
        self.root.title("Autonomous Robot Path Learning using Linked Lists")
        self.root.resizable(False, False)
        self.environment = GridEnvironment()
        self.environment.generate()
        self.robot = Robot(self.environment)
        self.animation_id = None
        self.replay_node = None

        outer = tk.Frame(root, padx=12, pady=12)
        outer.pack()
        self.canvas = tk.Canvas(outer, width=self.CELL * self.environment.cols,
                                height=self.CELL * self.environment.rows,
                                bg="white", highlightthickness=1)
        self.canvas.grid(row=0, column=0, sticky="n")
        controls = tk.Frame(outer, padx=16)
        controls.grid(row=0, column=1, sticky="n")

        for label, command in (
            ("Generate Environment", self.generate), ("Reset", self.reset),
            ("Start Learning", self.start), ("Stop", self.stop),
            ("Replay Learned Path", self.replay), ("Clear Learned Path", self.clear_path),
        ):
            tk.Button(controls, text=label, width=22, command=command).pack(pady=3)

        self.status_var = tk.StringVar()
        tk.Label(controls, textvariable=self.status_var, justify="left", anchor="w",
                 font=("Arial", 10), padx=4, pady=12).pack(fill="x", pady=(12, 0))
        tk.Label(controls, text="Blue: robot   Green: goal\nGray: obstacle   Yellow: linked path",
                 justify="left", fg="#444").pack(anchor="w")
        self.draw()

    def cancel_animation(self):
        if self.animation_id:
            self.root.after_cancel(self.animation_id)
            self.animation_id = None

    def generate(self):
        self.cancel_animation()
        self.environment.generate()
        self.robot = Robot(self.environment)
        self.draw()

    def reset(self):
        self.cancel_animation()
        self.robot.reset()
        self.draw()

    def clear_path(self):
        self.cancel_animation()
        self.robot.reset()
        self.draw()

    def start(self):
        if self.robot.learning:
            return
        self.cancel_animation()
        self.robot.start_learning()
        self.draw()
        self.animate_learning()

    def stop(self):
        self.cancel_animation()
        self.robot.stop()
        self.draw()

    def animate_learning(self):
        state = self.robot.learning_step()
        self.draw()
        if self.robot.learning:
            self.animation_id = self.root.after(170, self.animate_learning)
        elif state == "Dead End":
            messagebox.showinfo("Learning finished", "No route to the goal was found.")

    def replay(self):
        if self.robot.status != "Goal Reached" or self.robot.path.head is None:
            messagebox.showinfo("Replay", "Learn a successful path first.")
            return
        self.cancel_animation()
        self.replay_node = self.robot.path.head
        self.robot.position = (self.replay_node.x, self.replay_node.y)
        self.animate_replay()

    def animate_replay(self):
        if self.replay_node is None:
            return
        self.robot.position = (self.replay_node.x, self.replay_node.y)
        self.draw()
        self.replay_node = self.replay_node.next
        if self.replay_node:
            self.animation_id = self.root.after(240, self.animate_replay)

    def draw(self):
        self.canvas.delete("all")
        env = self.environment
        path_cells = {(node.x, node.y) for node in self.robot.path.nodes()}
        for x in range(env.rows):
            for y in range(env.cols):
                x1, y1 = y * self.CELL, x * self.CELL
                cell = (x, y)
                color = "#f7df70" if cell in path_cells else "#ffffff"
                if cell in env.obstacles:
                    color = "#667085"
                self.canvas.create_rectangle(x1, y1, x1 + self.CELL, y1 + self.CELL,
                                             fill=color, outline="#c9cdd3")
                if cell == env.start:
                    self.canvas.create_text(x1 + 10, y1 + 10, text="S", fill="#222", font=("Arial", 9, "bold"))
                if cell == env.goal:
                    self.canvas.create_oval(x1 + 12, y1 + 12, x1 + 36, y1 + 36, fill="#35a854", outline="")
        rx, ry = self.robot.position
        self.canvas.create_oval(ry * self.CELL + 10, rx * self.CELL + 10,
                                ry * self.CELL + 38, rx * self.CELL + 38,
                                fill="#2f80ed", outline="#174ea6", width=2)
        self.status_var.set(
            f"Robot Status: {self.robot.status}\n\n"
            f"Current Position: ({rx}, {ry})\n\n"
            f"Steps: {self.robot.steps}\n\n"
            f"Learned Path Length: {max(0, self.robot.path.length - 1)}\n\n"
            f"Reward: {self.robot.session_reward}"
        )
