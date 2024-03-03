class Node:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.is_visited = False
        self.distance = float('inf')
        self.total_distance = float('inf')
        self.previous_node = None

def greedy_bfs(grid, start, finish):
    rows, cols = len(grid), len(grid[0])
    start_node = Node(start[0], start[1])
    finish_node = Node(finish[0], finish[1])

    unvisited_nodes = [start_node]
    visited_nodes_in_order = []

    while unvisited_nodes:
        unvisited_nodes.sort(key=lambda node: node.total_distance)
        current_node = unvisited_nodes.pop(0)

        if current_node.row == finish_node.row and current_node.col == finish_node.col:
            return visited_nodes_in_order

        current_node.is_visited = True
        visited_nodes_in_order.append(current_node)

        neighbours = get_neighbours(current_node, grid)
        for neighbour in neighbours:
            distance = current_node.distance + 1

            if neighbour_not_in_unvisited_nodes(neighbour, unvisited_nodes):
                unvisited_nodes.insert(0, neighbour)
                neighbour.distance = distance
                neighbour.total_distance = manhattan_distance(neighbour, finish_node)
                neighbour.previous_node = current_node
            elif distance < neighbour.distance:
                neighbour.distance = distance
                neighbour.total_distance = manhattan_distance(neighbour, finish_node)
                neighbour.previous_node = current_node

    return visited_nodes_in_order

# ...

def get_neighbours(node, grid):
    neighbours = []
    row, col = node.row, node.col

    if row > 0 and not grid[row - 1][col].is_wall:
        neighbours.append(grid[row - 1][col])
    if col < len(grid[0]) - 1 and not grid[row][col + 1].is_wall:
        neighbours.append(grid[row][col + 1])
    if row < len(grid) - 1 and not grid[row + 1][col].is_wall:
        neighbours.append(grid[row + 1][col])
    if col > 0 and not grid[row][col - 1].is_wall:
        neighbours.append(grid[row][col - 1])

    return [neighbour for neighbour in neighbours if not neighbour.is_visited]


# ...

def manhattan_distance(node, finish_node):
    x = abs(node.row - finish_node.row)
    y = abs(node.col - finish_node.col)
    return x + y

def neighbour_not_in_unvisited_nodes(neighbour, unvisited_nodes):
    for node in unvisited_nodes:
        if node.row == neighbour.row and node.col == neighbour.col:
            return False
    return True

def start(maze, start,end):
    # Convert the grid to Node objects
    node_grid = [[Node(row, col, is_wall=(cell == 0)) for col, cell in enumerate(row_cells)] for row, row_cells in enumerate(maze)]

    return greedy_bfs(node_grid, start, end)


