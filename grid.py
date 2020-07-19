from node import Node


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.nodes = [[Node(x, y) for x in range(width)] for y in range(height)]

        for x in range(width):
            for y in range(height):
                self[x, y].add_neighbors(self.get_neighbors(x, y))

    def __getitem__(self, item):
        if self.in_bounds(item[0], item[1]):
            return self.nodes[item[1]][item[0]]

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_neighbors(self, x, y, eight_directions=False):
        shifts = [
            (-1, 0),
            (1, 0),
            (0, 1),
            (0, -1)
        ]
        diagonal_shifts = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1)
        ]

        for shift in shifts:
            point = x + shift[0], y + shift[1]
            if self.in_bounds(point[0], point[1]):
                yield self[point]

        if eight_directions:
            for shift in diagonal_shifts:
                point = x + shift[0], y + shift[1]
                if self.in_bounds(point[0], point[1]):
                    yield self[point]

