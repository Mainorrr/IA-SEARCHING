import copy
from collections import deque, defaultdict
import os

#Convierte la matriz en tupla para poder hacer uso del hash y asi guardar el estado en Estados Visitados
def estado_a_tupla(estado):
    return tuple(tuple(col) for col in estado)

#Funcion para confirmar cantidad de fichas (16 en total, 4 por color), y que en cada columna este solo un color
def es_estado_objetivo(estado):
    color_conteo = defaultdict(int)
    colores_encontrados = set()
    total_fichas = 0
    columnas_usadas = set()

    for idx, columna in enumerate(estado):
        if not columna:
            continue

        #Si alguna ficha de la columna es diferente a la ficha base, hay mezcla; o esta en varias columnas
        color = columna[0]
        if any(ficha != color for ficha in columna):
            return False  # columna con colores mezclados
        if color in colores_encontrados:
            return False  # el color ya apareció en otra columna
        
        colores_encontrados.add(color)
        color_conteo[color] = len(columna)
        total_fichas += len(columna)
        columnas_usadas.add(idx)

    #Confirmar que no se perdieron o generaron mas fichas
    if total_fichas != 16:
        return False
    
    #Confirmar que no se generaron mas colores
    if len(color_conteo) != 4:
        return False
    
    #Confirmar que cada color tiene 4 fichas
    if any(cant != 4 for cant in color_conteo.values()):
        return False
    
    #Si no falla antes, es una solucion.
    return True

#Funciona para generar una lista de posibles movimientos
def generar_movimientos(estado):
    movimientos = []

    #Recorrer cada columna como fuente de movimiento, si es vacia se ignora
    for i, origen in enumerate(estado):
        if not origen:
            continue

        #Toma el valor de la ficha que se puede mover
        ficha = origen[-1]

        #Se revisan las demas columas como destinos (se ignora la columna fuente)
        for j, destino in enumerate(estado):
            if i == j:
                continue

            #Si el dentino tiene menos de 4 dichas, y, destino esta vacio o la ultima ficha es del mismo tipo
            #Se realiza el movieminto
            if len(destino) < 4 and (not destino or destino[-1] == ficha):
                nuevo_estado = copy.deepcopy(estado)
                nuevo_estado[i].pop()
                nuevo_estado[j].append(ficha)
                movimientos.append((nuevo_estado, (i, j)))
    return movimientos

#Funcion para camiar de matriz para manejar los movimientos, a matriz para mostrar en consola
def estado_a_matriz(estado):
    """Convierte el estado (columnas) a una matriz de 6x6 para impresión."""
    filas = []
    for nivel in reversed(range(6)):  # de la fila superior (5) a la inferior (0)
        fila = []
        for col in estado:
            if len(col) > nivel:
                fila.append(col[nivel])
            else:
                fila.append('_')
        filas.append(fila)
    return filas

#Funcion para guardar la solucion en archivo.txt
def guardar_solucion(nombre_archivo, solucion):
    """Guarda la solución en un archivo de salida."""
    ruta_output = os.path.join("Output", f"LAC_output_{nombre_archivo}")
    os.makedirs("Output", exist_ok=True)
    with open(ruta_output, "w") as f:
        for paso, estado in enumerate(solucion):
            f.write(f"Paso {paso}:\n")
            matriz = estado_a_matriz(estado)
            for fila in matriz:
                f.write(" ".join(fila) + "\n")
            f.write("\n")

#Funcion solucion
def solucionarLAC(matriz, nombre_archivo):
    print("Solucionando con Lista Abierta y Cerrada...")

    # Convertimos la matriz de entrada en columnas (pilas)
    columnas = [[] for _ in range(6)]
    for fila in reversed(matriz):  # empezamos desde abajo
        for i, ficha in enumerate(fila):
            if ficha != '_':
                columnas[i].append(ficha)

    estado_inicial = columnas
    abiertos = deque()
    cerrados = set()

    abiertos.append((estado_inicial, []))
    cerrados.add(estado_a_tupla(estado_inicial))

    mejor_camino = None
    mejor_estado = None

    while abiertos:
        estado_actual, camino = abiertos.popleft()

        # Guardamos el último estado y camino como respaldo
        mejor_estado = estado_actual
        mejor_camino = camino

        if es_estado_objetivo(estado_actual):
            print("\n¡Solución encontrada!")
            print("Número de movimientos:", len(camino))
            solucion_completa = [estado_inicial]
            actual = estado_inicial
            for mov in camino:
                nuevo_estado = copy.deepcopy(actual)
                ficha = nuevo_estado[mov[0]].pop()
                nuevo_estado[mov[1]].append(ficha)
                solucion_completa.append(copy.deepcopy(nuevo_estado))
                actual = nuevo_estado
            guardar_solucion(nombre_archivo, solucion_completa)
            return

        for nuevo_estado, movimiento in generar_movimientos(estado_actual):
            estado_hash = estado_a_tupla(nuevo_estado)
            if estado_hash not in cerrados:
                cerrados.add(estado_hash)
                abiertos.append((nuevo_estado, camino + [movimiento]))

    print("No se encontró solución.")

