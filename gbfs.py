import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Node:
    def __init__(self, row, col, is_wall=False):
        self.row = row
        self.col = col
        self.is_wall = is_wall
        self.is_visited = False
        self.distance = float('inf')
        self.total_distance = float('inf')
        self.previous_node = None

def read_maze_from_file(file_path):
    with open(file_path, 'r') as file:
        maze_lines = file.readlines()

    maze = [list(map(int, line.strip())) for line in maze_lines]
    return np.array(maze)

def greedy_bfs(grid, start_node, finish_node):
    if not start_node or not finish_node or start_node == finish_node:
        return False

    unvisited_nodes = [] 
    visited_nodes_in_order = []
    start_node.distance = 0
    unvisited_nodes.append(start_node)

    while unvisited_nodes:
        unvisited_nodes.sort(key=lambda node: node.total_distance)
        closest_node = unvisited_nodes.pop(0)

        if closest_node == finish_node:
            return visited_nodes_in_order

        closest_node.is_visited = True
        visited_nodes_in_order.append(closest_node)

        neighbours = get_neighbours(closest_node, grid)
        for neighbour in neighbours:
            distance = closest_node.distance + 1

            # f(n) = g(n) + h(n)
            if neighbour_not_in_unvisited_nodes(neighbour, unvisited_nodes):
                unvisited_nodes.insert(0, neighbour)
                neighbour.distance = distance
                neighbour.total_distance = distance + manhattan_distance(neighbour, finish_node)
                neighbour.previous_node = closest_node
            elif distance < neighbour.distance:
                neighbour.distance = distance
                neighbour.total_distance = distance + manhattan_distance(neighbour, finish_node)
                neighbour.previous_node = closest_node

    return visited_nodes_in_order

def get_neighbours(node, grid):
    neighbours = []
    row, col = node.row, node.col

    if row != 0:
        neighbours.append(grid[row - 1][col])
    if col != len(grid[0]) - 1:
        neighbours.append(grid[row][col + 1])
    if row != len(grid) - 1:
        neighbours.append(grid[row + 1][col])
    if col != 0:
        neighbours.append(grid[row][col - 1])

    return [neighbour for neighbour in neighbours if not neighbour.is_wall and not neighbour.is_visited]

def manhattan_distance(node, finish_node):
    x = abs(node.row - finish_node.row)
    y = abs(node.col - finish_node.col)
    return x + y

def neighbour_not_in_unvisited_nodes(neighbour, unvisited_nodes):
    return all(node.row != neighbour.row or node.col != neighbour.col for node in unvisited_nodes)

def draw_maze_with_path(maze, path):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Establecer el color del borde en blanco
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)

    # Invertir colores para que los 0's sean blancos y los 1's negros/grises
    inverted_maze = np.where(maze == 0, 1, 0)
    ax.imshow(inverted_maze, cmap=plt.cm.binary, interpolation='nearest', vmin=0, vmax=1)
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Dibujar flechas de entrada y salida si existen
    start_coords = np.argwhere(maze == 2)
    finish_coords = np.argwhere(maze == 3)

    if start_coords.size > 0:
        ax.arrow(*start_coords[0][::-1], .4, 0, fc='green', ec='green', head_width=0.3, head_length=0.3)

    if finish_coords.size > 0:
        ax.arrow(*finish_coords[0][::-1], 0.4, 0, fc='blue', ec='blue', head_width=0.3, head_length=0.3)
    
    # Preparar para la animación del camino
    line, = ax.plot([], [], color='green', linewidth=2)
    
    def init():
        line.set_data([], [])
        return line,

    # La función update es llamada para cada punto del camino en el laberinto
    def update(frame):
        x, y = path[frame].col, path[frame].row
        line.set_data(*zip(*[(p.col, p.row) for p in path[:frame+1]]))  # actualizar los datos
        return line,
    
    # Ajustar el intervalo para una animación más rápida
    interval = 1  # Intervalo en milisegundos
    ani = animation.FuncAnimation(fig, update, frames=range(len(path)), init_func=init, blit=True, repeat=False, interval=interval)

    plt.show()

def start(file_path):
    maze = read_maze_from_file(file_path)

    # Convertir el laberinto a objetos Node
    node_grid = [[Node(row, col, is_wall=(cell == 0)) for col, cell in enumerate(row_cells)] for row, row_cells in enumerate(maze)]
    
    # Encontrar las coordenadas de inicio y fin
    start_coords = [(i, j) for i, row in enumerate(maze) for j, cell in enumerate(row) if cell == 2]
    end_coords = [(i, j) for i, row in enumerate(maze) for j, cell in enumerate(row) if cell == 3]
    
    if not start_coords or not end_coords:
        print("Error: No se encontraron las coordenadas de inicio o fin en el laberinto.")
        return
    
    start_coord, end_coord = start_coords[0], end_coords[0]
    start_node = node_grid[start_coord[0]][start_coord[1]]
    end_node = node_grid[end_coord[0]][end_coord[1]]
    
    start_time = time.time()  # Iniciar el temporizador    
    
    # Obtener el camino mediante Greedy BFS
    path = greedy_bfs(node_grid, start_node, end_node)
    
    end_time = time.time()  # Detener el temporizador
    elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido

    print(f"Tiempo de resolución: {elapsed_time:.6f} segundos")
    print(f"Cantidad de pasos: {len(path)}")
    # Dibujar el laberinto y el camino
    draw_maze_with_path(np.array(maze), path)

