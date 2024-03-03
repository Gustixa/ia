from warnings import warn
import heapq

class Nodo:
    """
    Clase para nodos en A* Pathfinding
    """

    def __init__(self, padre=None, posicion=None):
        self.padre = padre
        self.posicion = posicion

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, otro):
        return self.posicion == otro.posicion
    
    def __repr__(self):
        return f"{self.posicion} - g: {self.g} h: {self.h} f: {self.f}"

    # Definiendo menor que para la cola de prioridad
    def __lt__(self, otro):
        return self.f < otro.f
    
    # Definiendo mayor que para la cola de prioridad
    def __gt__(self, otro):
        return self.f > otro.f

def devolver_camino(nodo_actual):
    camino = []
    actual = nodo_actual
    while actual is not None:
        camino.append(actual.posicion)
        actual = actual.padre
    return camino[::-1]  # Devolver el camino en orden inverso

def astar(maze, inicio, fin, permitir_movimiento_diagonal=False):
    """
    Retorna una lista de tuplas como camino desde el inicio dado hasta el fin en el laberinto dado
    :param maze: Laberinto representado como una matriz
    :param inicio: Coordenadas de inicio
    :param fin: Coordenadas de fin
    :return: Lista de tuplas representando el camino
    """

    # Crear nodos de inicio y fin
    nodo_inicio = Nodo(None, inicio)
    nodo_inicio.g = nodo_inicio.h = nodo_inicio.f = 0
    nodo_fin = Nodo(None, fin)
    nodo_fin.g = nodo_fin.h = nodo_fin.f = 0

    # Inicializar listas abierta y cerrada
    lista_abierta = []
    lista_cerrada = []

    # Convertir lista abierta en cola de prioridad y añadir el nodo de inicio
    heapq.heapify(lista_abierta)
    heapq.heappush(lista_abierta, nodo_inicio)

    # Añadir una condición de parada
    iteraciones_externas = 0
    max_iteraciones = (len(maze[0]) * len(maze) // 2)

    # Definir cuadrados adyacentes para el movimiento
    cuadrados_adyacentes = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if permitir_movimiento_diagonal:
        cuadrados_adyacentes = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Bucle hasta encontrar el final
    while len(lista_abierta) > 0:
        iteraciones_externas += 1

        if iteraciones_externas > max_iteraciones:
            # Si llegamos a este punto, se devuelve el camino tal como está,
            # no contendrá el destino
            warn("Se ha renunciado al pathfinding, demasiadas iteraciones")
            return devolver_camino(nodo_actual)

        # Obtener el nodo actual
        nodo_actual = heapq.heappop(lista_abierta)
        lista_cerrada.append(nodo_actual)

        # Encontrado el objetivo
        if nodo_actual == nodo_fin:
            return devolver_camino(nodo_actual)

        # Generar hijos
        hijos = []

        for nueva_posicion in cuadrados_adyacentes:  # Cuadrados adyacentes

            # Obtener la posición del nodo
            posicion_nodo = (nodo_actual.posicion[0] + nueva_posicion[0], nodo_actual.posicion[1] + nueva_posicion[1])

            # Asegurarse de que esté dentro del rango
            if posicion_nodo[0] > (len(maze) - 1) or posicion_nodo[0] < 0 or posicion_nodo[1] > (
                    len(maze[len(maze) - 1]) - 1) or posicion_nodo[1] < 0:
                continue

            # Asegurarse de que sea un terreno transitable
            if maze[posicion_nodo[0]][posicion_nodo[1]] == 0:
                continue

            # Crear nuevo nodo
            nuevo_nodo = Nodo(nodo_actual, posicion_nodo)

            # Añadir a la lista de hijos
            hijos.append(nuevo_nodo)

        # Bucle a través de los hijos
        for hijo in hijos:
            # El hijo está en la lista cerrada
            if len([hijo_cerrado for hijo_cerrado in lista_cerrada if hijo_cerrado == hijo]) > 0:
                continue

            # Crear los valores f, g y h
            hijo.g = nodo_actual.g + 1
            # Heuristica euclideana
            hijo.h = ((hijo.posicion[0] - nodo_fin.posicion[0]) ** 2) + ((hijo.posicion[1] - nodo_fin.posicion[1]) ** 2)
            # Heuristica manhattan
            #hijo.h = abs(hijo.posicion[0] - nodo_fin.posicion[0]) + abs(hijo.posicion[1] - nodo_fin.posicion[1])

            hijo.f = hijo.g + hijo.h

            # El hijo ya está en la lista abierta
            if len(
                    [nodo_abierto for nodo_abierto in lista_abierta if hijo.posicion == nodo_abierto.posicion and hijo.g > nodo_abierto.g]) > 0:
                continue

            # Añadir el hijo a la lista abierta
            heapq.heappush(lista_abierta, hijo)

    warn("No se pudo obtener un camino hacia el destino")
    return None