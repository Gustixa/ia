import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from queue import Queue
import os
import time
from a_star import astar
from gbfs import start


# Función para crear el laberinto a partir de un archivo
def create_maze_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    maze = np.array([[int(char) for char in line.strip()] for line in lines])
    return maze

# Algoritmo BFS para encontrar el camino más corto
def breadth_first_search(maze):
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
            next_node = (node[0] + dx, node[1] + dy)
            if next_node == end:
                return path + [next_node]
            if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                    maze[next_node] == 1 and not visited[next_node]):
                visited[next_node] = True
                queue.put((next_node, path + [next_node]))

# Algoritmo DFS para encontrar el camino más corto
def depth_first_search(maze):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = tuple(np.argwhere(maze == 2)[0])
    end = tuple(np.argwhere(maze == 3)[0])
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    stack = [(start, [])]
    while stack:
        (node, path) = stack.pop()
        for dx, dy in directions:
            next_node = (node[0] + dx, node[1] + dy)
            if next_node == end:
                return path + [next_node]
            if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                    maze[next_node] == 1 and not visited[next_node]):
                visited[next_node] = True
                stack.append((next_node, path + [next_node]))

# Algoritmo Depth-Limited Search para encontrar el camino más corto con profundidad limitada
def depth_limited_search(maze, depth_limit):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    start = tuple(np.argwhere(maze == 2)[0])
    end = tuple(np.argwhere(maze == 3)[0])
    visited = np.zeros_like(maze, dtype=bool)
    visited[start] = True
    stack = [(start, [])]
    while stack:
        (node, path) = stack.pop()
        if len(path) <= depth_limit:
            for dx, dy in directions:
                next_node = (node[0] + dx, node[1] + dy)
                if next_node == end:
                    return path + [next_node]
                if (0 <= next_node[0] < maze.shape[0] and 0 <= next_node[1] < maze.shape[1] and
                        maze[next_node] == 1 and not visited[next_node]):
                    visited[next_node] = True
                    stack.append((next_node, path + [next_node]))

# Función para dibujar el laberinto y el camino
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
        line, = ax.plot([], [], color='green', linewidth=2)
        
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

# Función principal
if __name__ == "__main__":
    filename = "test_maze.txt"
    filename = os.path.join(os.getcwd(), filename)  # Obtener la ruta completa al archivo
    maze = create_maze_from_file(filename)
    # Menú de opciones
    print("Selecciona un algoritmo:")
    print("1. Breadth-First Search")
    print("2. Depth-First Search")
    print("3. Depth-Limited Search")
    print("4. Greedy Best-First Search")
    print("5. A*")

    choice = int(input("Ingresa el número del algoritmo que deseas utilizar: "))

    start_time = time.time()  # Iniciar el temporizador

    if choice == 1:
        path = breadth_first_search(maze)
    elif choice == 2:
        path = depth_first_search(maze)
    elif choice == 3:
        depth_limit = int(input("Ingresa el límite de profundidad para Depth-Limited Search: "))
        path = depth_limited_search(maze, depth_limit)
    elif choice == 4:
        start(filename)
    elif choice == 5:
        start = tuple(np.argwhere(maze == 2)[0])
        end = tuple(np.argwhere(maze == 3)[0])
        path = astar(maze, start, end)
    else:
        print("Opción no válida. Por favor, selecciona un número del 1 al 5.")

    end_time = time.time()  # Detener el temporizador
    elapsed_time = end_time - start_time  # Calcular el tiempo transcurrido

    if path:
        print(f"Tiempo de resolución: {elapsed_time:.6f} segundos")
        print(f"Cantidad de pasos: {len(path)}")
        draw_maze(maze, path)
    else:   
        print("No se encontró un camino.")
