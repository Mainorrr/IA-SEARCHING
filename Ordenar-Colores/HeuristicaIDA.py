import copy

META = 4 
COLORES = ['R', 'G', 'Y', 'B']

def solucionarHIDA(matriz, nombre_archivo):
    columnas = matriz_a_columnas(matriz)
    archivo_salida = f"Output/{nombre_archivo}_output.txt"
    open(archivo_salida, 'w').close()

    solucion = ida_star(columnas)

    for paso, estado in enumerate(solucion):
        guardar_paso_en_archivo(paso, estado, archivo_salida)
    print(f"Solución guardada en: {archivo_salida}")

# Convierte la matriz de entrada a una lista de columnas
# donde cada columna es una lista de fichas (de abajo hacia arriba)
def matriz_a_columnas(matriz):
    columnas = [[] for _ in range(6)]
    for fila in reversed(matriz):
        for col_index in range(6):
            valor = fila[col_index]
            if valor != '_':
                columnas[col_index].append(valor)
    return columnas

# Función principal para resolver el problema usando IDA*
# Se basa en la heurística de fichas mal colocadas
def ida_star(estado):
    limite = heuristica(estado)
    while True:
        resultado = busqueda(estado, 0, limite, [], set())
        if resultado != "LIMITE":
            return resultado
        limite += 1

# Función heurística que cuenta el número de fichas mal colocadas
# (fichas que no están en la columna correcta)
def heuristica(estado):
    mal_colocadas = 0
    for col in estado:
        if not col:
            continue
        color = col[-1]
        for ficha in col:
            if ficha != color:
                mal_colocadas += 1
    return mal_colocadas

# Función de búsqueda recursiva que implementa el algoritmo IDA*
# Limita la profundidad de búsqueda a un límite dado
def busqueda(estado, g, limite, camino, visitados):
    f = g + heuristica(estado)
    if f > limite:
        return "LIMITE"
    if es_objetivo(estado):
        return camino + [estado]

    estado_hash = estado_a_tupla(estado)
    if estado_hash in visitados:
        return "LIMITE"
    visitados.add(estado_hash)

    minimo = float('inf')
    for (i, j) in posibles_movimientos(estado):
        nuevo_estado = mover(estado, i, j)
        if camino and nuevo_estado == camino[-1]:
            continue
        resultado = busqueda(nuevo_estado, g + 1, limite, camino + [estado], visitados)
        if resultado != "LIMITE":
            return resultado
    return "LIMITE"

# Verifica si el estado actual es el objetivo
# (todas las columnas tienen el mismo color y están llenas)
def es_objetivo(estado):
    for columna in estado:
        if len(columna) == 0:
            continue
        if len(columna) != META or len(set(columna)) != 1:
            return False
    return True

# Convierte el estado a forma inmutable para hashing
def estado_a_tupla(estado):
    return tuple(tuple(col) for col in estado)

# Genera todos los movimientos posibles desde un estado dado
# (considerando la física de caída de las fichas)
def posibles_movimientos(estado):
    movimientos = []
    for i, origen in enumerate(estado):
        if not origen:
            continue
        ficha = origen[-1]
        for j, destino in enumerate(estado):
            if i == j:
                continue
            if len(destino) < 6:
                if len(destino) == 0 or destino[-1] == ficha:
                    movimientos.append((i, j))
    return movimientos

# Realiza un movimiento de una ficha de una columna a otra
# (sin modificar el estado original)
def mover(estado, origen, destino):
    nuevo = copy.deepcopy(estado)
    ficha = nuevo[origen].pop()
    nuevo[destino].append(ficha)
    return nuevo

# Guarda el estado actual en un archivo de salida
# en un formato legible (de arriba hacia abajo)
def guardar_paso_en_archivo(paso, columnas, archivo_salida):
    with open(archivo_salida, 'a') as f:
        f.write(f"Paso {paso}:\n")
        for fila in range(5, -1, -1):
            linea = []
            for col in columnas:
                if fila < len(col):
                    linea.append(col[fila])
                else:
                    linea.append('_')
            f.write(" ".join(linea) + '\n')
        f.write("\n")
