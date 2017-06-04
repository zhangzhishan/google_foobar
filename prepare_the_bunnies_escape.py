from collections import deque


class Node:

    def __init__(self, x, y, remove_flag, maze):
        self.x = x
        self.y = y;
        self.remove_flag = remove_flag
        self.maze = maze

    def __hash__(self):
        return self.x ^ self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.remove_flag == other.remove_flag

    def get_neighbors(self):
        neighbors = []
        x = self.x
        y = self.y
        remove_flag = self.remove_flag
        maze = self.maze
        rows = len(maze)
        columns = len(maze[0])

        if x > 0:
            wall = maze[y][x - 1]
            if wall:
                if remove_flag > 0:
                    neighbors.append(Node(x - 1, y, remove_flag - 1, maze))
            else:
                neighbors.append(Node(x - 1, y, remove_flag, maze))

        if x < columns - 1:
            wall = maze[y][x + 1]
            if wall:
                if remove_flag > 0:
                    neighbors.append(Node(x + 1, y, remove_flag - 1, maze))
            else:
                neighbors.append(Node(x + 1, y, remove_flag, maze))

        if y > 0:
            wall = maze[y - 1][x]
            if wall:
                if remove_flag > 0:
                    neighbors.append(Node(x, y - 1, remove_flag - 1, maze))
            else:
                neighbors.append(Node(x, y - 1, remove_flag, maze))

        if y < rows - 1:
            wall = maze[y + 1][x]
            if wall:
                if remove_flag > 0:
                    neighbors.append(Node(x, y + 1, remove_flag - 1, maze))
            else:
                neighbors.append(Node(x, y + 1, remove_flag, maze))

        return neighbors




def answer(maze):
    source = Node(0, 0, 1, maze)
    queue = deque([source])
    distance_map = {source: 1}
    columns = len(maze[0])
    rows = len(maze)

    while queue:
        current_node = queue.popleft()

        if current_node.x == columns - 1 and current_node.y == rows - 1:
            return distance_map[current_node]

        for child_node in current_node.get_neighbors():
            if child_node not in distance_map.keys():
                distance_map[child_node] = distance_map[current_node] + 1
                queue.append(child_node)

    return 1000 * 1000 * 1000 # Cannot escape

