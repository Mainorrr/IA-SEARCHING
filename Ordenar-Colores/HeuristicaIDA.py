import copy

META = 4  # Número de fichas por columna
COLORES = ['R', 'G', 'Y', 'B'] # Colores de las fichas

def solucionarHIDA(matriz, nombre_archivo):
    columnas = matriz_a_columnas(matriz)
    archivo_salida = f"Output/{nombre_archivo}_output.txt"

    # Limpiar archivo anterior
    open(archivo_salida, 'w').close()

    # Ejecutar algoritmo y obtener solución
    solucion = ida_star(columnas)

    # Guardar todos los pasos
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

def ida_star(estado):
    limite = heuristica(estado)
    while True:
        resultado = busqueda(estado, 0, limite, [], set())
        if resultado != "LIMITE":
            return resultado
        limite += 1

def heuristica(estado):
    # Cuenta fichas mal colocadas (no sobre ficha de su mismo color)
    mal_colocadas = 0
    for col in estado:
        if not col:
            continue
        color = col[-1]
        for ficha in col:
            if ficha != color:
                mal_colocadas += 1
    return mal_colocadas

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
            continue  # Evitar volver atrás
        resultado = busqueda(nuevo_estado, g + 1, limite, camino + [estado], visitados)
        if resultado != "LIMITE":
            return resultado
    return "LIMITE"

def es_objetivo(estado):
    for columna in estado:
        if len(columna) == 0:
            continue
        if len(columna) != META or len(set(columna)) != 1:
            return False
    return True

def estado_a_tupla(estado):
    # Convierte el estado a forma inmutable para hashing
    return tuple(tuple(col) for col in estado)

def posibles_movimientos(estado):
    movimientos = []
    for i, origen in enumerate(estado):
        if not origen:
            continue
        ficha = origen[-1]
        for j, destino in enumerate(estado):
            if i == j:
                continue
            if len(destino) < 6:  # Límite de altura
                if len(destino) == 0 or destino[-1] == ficha:
                    movimientos.append((i, j))
    return movimientos

def mover(estado, origen, destino):
    nuevo = copy.deepcopy(estado)
    ficha = nuevo[origen].pop()
    nuevo[destino].append(ficha)
    return nuevo

def guardar_paso_en_archivo(paso, columnas, archivo_salida):
    with open(archivo_salida, 'a') as f:
        f.write(f"Paso {paso}:\n")
        for fila in range(5, -1, -1):  # de arriba hacia abajo
            linea = []
            for col in columnas:
                if fila < len(col):
                    linea.append(col[fila])
                else:
                    linea.append('_')
            f.write(" ".join(linea) + '\n')
        f.write("\n")
