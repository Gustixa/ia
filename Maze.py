import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from queue import Queue
import os

def create_maze_from_file(filename):
    # Leer el laberinto desde el archivo
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Crear el laberinto a partir de los datos del archivo
    maze = np.array([[int(char) for char in line.strip()] for line in lines])

    return maze

def find_path(maze):
    # Algoritmo BFS para encontrar el camino más corto
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = tuple(np.argwhere(maze == 2)[0])
    end = tuple(np.argwhere(maze == 3)[0])
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
                maze[next_node] == 1 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))

def draw_maze(maze, path=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Establecer el color del borde en blanco
    fig.patch.set_edgecolor('white')
    fig.patch.set_linewidth(0)

    # Invertir colores para que los 0's sean blancos y los 1's negros/grises
    inverted_maze = np.where(maze == 0, 1, 0)
    ax.imshow(inverted_maze, cmap=plt.cm.binary, interpolation='nearest', vmin=0, vmax=1)
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
        ani = animation.FuncAnimation(fig, update, frames=range(len(path)), init_func=init, blit=True, repeat=False, interval=interval)
    
    # Dibujar flechas de entrada y salida
    ax.arrow(*np.argwhere(maze == 2)[0][::-1], .4, 0, fc='green', ec='green', head_width=0.3, head_length=0.3)
    ax.arrow(*np.argwhere(maze == 3)[0][::-1], 0.4, 0, fc='blue', ec='blue', head_width=0.3, head_length=0.3)
    
    plt.show()


if __name__ == "__main__":
    filename = input("Ingresa el nombre del archivo .txt con el laberinto: ")
    filename = os.path.join(os.getcwd(), filename)  # Obtener la ruta completa al archivo
    maze = create_maze_from_file(filename)
    path = find_path(maze)
    draw_maze(maze, path)
