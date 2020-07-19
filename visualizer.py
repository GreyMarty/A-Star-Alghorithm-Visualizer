from tkinter import Canvas
from time import time, sleep

from grid import Grid


class Visualizer(Canvas):
    def __init__(self, width, height, cell_size, pathfinder, **kwargs):
        super(Visualizer, self).__init__(width=cell_size * width, height=cell_size * height, **kwargs)
        kwargs["master"].config(bg="#cccccc")

        self.grid = Grid(width, height)
        self.cell_size = cell_size

        self.rendered_points = {}
        self.edited = []

        self.pathfinder = pathfinder(self.grid)
        self.start = None
        self.goal = None

    def pack(self, **kwargs):
        super(Visualizer, self).pack(fill="none", expand=1)

        self.bind("<Button-1>", self.add_wall)
        self.bind("<B1-Motion>", self.add_wall)
        self.bind("<Button-3>", self.remove_wall)
        self.bind("<B3-Motion>", self.remove_wall)

        self.draw_grid()

    def draw_grid(self):
        for x in range(0, self.grid.width * self.cell_size, self.cell_size):
            self.create_line([x, 0, x, self.grid.height * self.cell_size], fill="grey", width=1)

        for y in range(0, self.grid.height * self.cell_size, self.cell_size):
            self.create_line([0, y, self.grid.width * self.cell_size, y], fill="grey", width=1)

    def add_wall(self, mouse):
        grid_pos = int(mouse.x / self.cell_size), int(mouse.y / self.cell_size)

        if grid_pos in (self.start, self.goal):
            return

        if not self.start:
            self.start = grid_pos
            self.fill_cell(grid_pos, "red")
            return

        if not self.goal:
            self.goal = grid_pos
            self.fill_cell(grid_pos, "green")
            return

        if self.rendered_points.get(grid_pos):
            return

        if self.grid[grid_pos]:
            self.grid[grid_pos].is_wall = True
            self.edited.append(self.grid[grid_pos])

            self.fill_cell(grid_pos, "black")

    def remove_wall(self, mouse):
        grid_pos = int(mouse.x / self.cell_size), int(mouse.y / self.cell_size)

        if grid_pos == self.start:
            self.start = None
            self.clear_cell(grid_pos)
            return

        if grid_pos == self.goal:
            self.goal = None
            self.clear_cell(grid_pos)
            return

        if self.rendered_points.get(grid_pos):
            self.clear_cell(grid_pos)
            self.rendered_points.pop(grid_pos)

            if self.grid[grid_pos]:
                self.grid[grid_pos].is_wall = False
                self.edited.remove(self.grid[grid_pos])
    
    def fill_cell(self, grid_pos, color):
        rect = [
            (grid_pos[0]) * self.cell_size, (grid_pos[1]) * self.cell_size,
            (grid_pos[0] + 1) * self.cell_size, (grid_pos[1] + 1) * self.cell_size
        ]
        self.rendered_points[grid_pos] = self.create_rectangle(rect, fill=color)

    def clear_cell(self, grid_pos):
        self.delete(self.rendered_points[grid_pos])

    def clear(self):
        self.start = None
        self.goal = None
        for node in self.edited:
            node.is_wall = False
        self.rendered_points.clear()
        self.edited.clear()
        self.delete("all")
        self.draw_grid()

    def build_path(self):
        if not self.start or not self.goal:
            return

        passed = self.pathfinder.build_path(self.start, self.goal)

        for point in passed:
            start_time = time()
            if point in (self.start, self.goal):
                continue

            self.fill_cell(point, "blue")
            end_time = time()
            self.update()
            render_time = end_time - start_time
            sleep(max(0, 0.001 - render_time))

        for point in self.pathfinder.last_path:
            if abs(point[0] - self.goal[0]) + abs(point[1] - self.goal[1]) == 1:
                self.fill_cell(point, "purple")
                break
            self.fill_cell(point, "purple")
