import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
from queue import Queue

def create_maze(dim):
    # Crear un laberinto con dimensiones dadas, lleno de paredes
    maze = np.ones((dim*2+1, dim*2+1))

    # Definir el punto de inicio
    x, y = (0, 0)
    maze[2*x+1, 2*y+1] = 0

    # Inicializar la pila con el punto de inicio
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Definir las direcciones posibles
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] == 1:
                maze[2*nx+1, 2*ny+1] = 0
                maze[2*x+1+dx, 2*y+1+dy] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()
            
    # Crear una entrada y una salida en el laberinto
    maze[1, 0] = 0
    maze[-2, -1] = 0

    return maze

def find_path(maze):
    # Algoritmo BFS para encontrar el camino más corto
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = (1, 1)
    end = (maze.shape[0]-2, maze.shape[1]-2)
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    queue = Queue()
    queue.put((start, []))
    while not queue.empty():
        (node, path) = queue.get()
        for dx, dy in directions:
            next_node = (node[0]+dx, node[1]+dy)
            if (next_node == end):
                return path + [next_node]
            if (next_node[0] >= 0 and next_node[1] >= 0 and 
                next_node[0] < maze.shape[0] and next_node[1] < maze.shape[1] and 
                maze[next_node] == 0 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))

def draw_maze(maze, path=None):
    fig, ax = plt.subplots(figsize=(10,10))
    
    # Establecer el color del borde en blanco
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)

    ax.imshow(maze, cmap=plt.cm.binary, interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Preparar para la animación del camino
    if path is not None:
        line, = ax.plot([], [], color='red', linewidth=2)
        
        def init():
            line.set_data([], [])
            return line,
        
        # La función update es llamada para cada punto del camino en el laberinto
        def update(frame):
            x, y = path[frame]
            line.set_data(*zip(*[(p[1], p[0]) for p in path[:frame+1]]))  # actualizar los datos
            return line,
        
        # Ajustar el intervalo para una animación más rápida
        interval = 1  # Intervalo en milisegundos
        ani = animation.FuncAnimation(fig, update, frames=range(len(path)), init_func=init, blit=True, repeat = False, interval=interval)
    
    # Dibujar flechas de entrada y salida
    ax.arrow(0, 1, .4, 0, fc='green', ec='green', head_width=0.3, head_length=0.3)
    ax.arrow(maze.shape[1] - 1, maze.shape[0]  - 2, 0.4, 0, fc='blue', ec='blue', head_width=0.3, head_length=0.3)
    
    plt.show()


if __name__ == "__main__":
    dim = int(input("Ingresa la dimensión del laberinto: "))
    maze = create_maze(dim)
    path = find_path(maze)
    draw_maze(maze, path)