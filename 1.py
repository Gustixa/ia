import graphviz

# Definición de las regiones de Australia y sus vecinos
australia = {
    'Western Australia': ['Northern Territory', 'South Australia'],
    'Northern Territory': ['Western Australia', 'South Australia', 'Queensland'],
    'South Australia': ['Western Australia', 'Northern Territory', 'Queensland', 'New South Wales', 'Victoria'],
    'Queensland': ['Northern Territory', 'South Australia', 'New South Wales'],
    'New South Wales': ['Queensland', 'South Australia', 'Victoria'],
    'Victoria': ['South Australia', 'New South Wales']
}

# Colores disponibles
colors = ['rojo', 'azul', 'verde']

# Función para verificar si un color es válido para un vértice dado
def es_color_valido(grafo, vertice, color, coloracion):
    for vecino in grafo[vertice]:
        if vecino in coloracion and coloracion[vecino] == color:
            return False
    return True

# Función para colorear el grafo
def colorear_grafo(grafo, colores):
    coloracion = {}
    for vertice in grafo:
        for color in colores:
            if es_color_valido(grafo, vertice, color, coloracion):
                coloracion[vertice] = color
                break
    return coloracion

# Función para crear el grafo visualmente con Graphviz
def crear_grafo_visual(grafo, coloracion):
    dot = graphviz.Graph(graph_attr={'rankdir': 'LR'})
    aristas_agregadas = set()  # Conjunto para almacenar las aristas agregadas
    for vertice in grafo:
        dot.node(vertice, style='filled', fillcolor=asignar_color_rgb(coloracion[vertice]), shape='ellipse', fontcolor='white')
        for vecino in grafo[vertice]:
            # Verificar si la arista ya ha sido agregada (en cualquier dirección)
            if (vertice, vecino) not in aristas_agregadas and (vecino, vertice) not in aristas_agregadas:
                dot.edge(vertice, vecino, dir='none')  # Agregar la arista sin dirección
                aristas_agregadas.add((vertice, vecino))  # Agregar la arista al conjunto
    return dot


# Función para asignar un código RGB a cada color
def asignar_color_rgb(color):
    if color == 'rojo':
        return '#b03a2e'
    elif color == 'azul':
        return '#1b4f72'
    elif color == 'verde':
        return '#186a3b'
    else:
        return '#FFFFFF'  # Color blanco para cualquier otro caso


# Colorear el mapa de Australia
coloracion_australia = colorear_grafo(australia, colors)

# Crear el grafo visual
grafo_visual = crear_grafo_visual(australia, coloracion_australia)

# Guardar y mostrar el grafo visual
grafo_visual.render('mapa_australia_coloreado', format='png', cleanup=True)
grafo_visual.view()

# Mostrar el resultado
for region, color in coloracion_australia.items():
    print(f"La región {region} está coloreada de {color}.")



# Función para verificar si un color es válido para una región
def es_color_valido(region, color, coloracion):
    for vecino in australia[region]:
        if vecino in coloracion and coloracion[vecino] == color:
            return False
    return True

# Función de backtracking para encontrar todas las soluciones
def encontrar_soluciones(regiones, colores, coloracion_actual={}):
    if len(coloracion_actual) == len(regiones):
        yield coloracion_actual
        return

    region = regiones[len(coloracion_actual)]
    for color in colores:
        if es_color_valido(region, color, coloracion_actual):
            coloracion_actual[region] = color
            yield from encontrar_soluciones(regiones, colores, coloracion_actual.copy())
            del coloracion_actual[region]


# Encontrar todas las soluciones posibles
soluciones = list(encontrar_soluciones(list(australia.keys()), colors))

# Imprimir las soluciones
print("Número de soluciones:", len(soluciones))
for i, solucion in enumerate(soluciones, start=1):
    print(f"Solución {i}: {solucion}")
