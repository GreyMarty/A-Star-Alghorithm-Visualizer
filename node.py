class Node:
    def __init__(self, x, y, **kwargs):
        self.pos = (x, y)
        self.neighbors = list(kwargs["neighbors"]) if "neighbors" in kwargs.keys() else []

        self.is_wall = False

        self.x = self.pos[0]
        self.y = self.pos[1]

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors and neighbor.pos != self.pos:
            self.neighbors.append(neighbor)

    def add_neighbors(self, neighbors):
        for neighbor in neighbors:
            self.add_neighbor(neighbor)