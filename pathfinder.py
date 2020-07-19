from queue import PriorityQueue


def decode_path(bad_path):
    path = []

    path_point = tuple(bad_path.keys())[-1]

    while bad_path[path_point]:
        path.append(path_point)
        path_point = bad_path[path_point]

    return path


def heuristic(a, b):
    x1, y1 = a
    x2, y2 = b

    return abs(x1 - x2) + abs(y1 - y2)


class AStarSearch:
    def __init__(self, graph, eight_directions=False):
        self.graph = graph
        self.eight_directions = eight_directions

        self.last_path = []

    def build_path(self, start, goal):
        came_from = {
            start: None
        }
        frontier = PriorityQueue()
        frontier.put((0, start))

        while not frontier.empty():
            current = frontier.get()[1]

            if current == goal:
                came_from[goal] = current
                break

            for new_pos in self.graph.get_neighbors(current[0], current[1], eight_directions=self.eight_directions):
                new_pos = new_pos.x, new_pos.y
                if new_pos not in came_from and not self.graph[new_pos].is_wall:
                    yield new_pos

                    dist = heuristic(new_pos, goal)
                    came_from[new_pos] = current
                    frontier.put((dist, new_pos))

            self.last_path = decode_path(came_from)
            self.last_path.reverse()
