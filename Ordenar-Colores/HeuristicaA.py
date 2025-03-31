import heapq
import os

def heuristica(matriz):
    """Calcula la heurística como la cantidad de letras fuera de su columna objetivo."""
    columnas = {c: [] for c in range(len(matriz[0]))}
    for fila in matriz:
        for col, valor in enumerate(fila):
            if valor != "_":
                columnas[col].append(valor)
    
    mal_colocadas = 0
    for col, valores in columnas.items():
        if valores and len(set(valores)) > 1:  # Si hay más de un tipo de letra
            mal_colocadas += len(valores)
    
    return mal_colocadas

def es_estado_final(matriz):
    """Verifica si la matriz es un estado final válido, donde cada letra solo aparece en una única columna."""
    letra_columnas = {}
    for col in range(len(matriz[0])):
        letras = [fila[col] for fila in matriz if fila[col] != "_"]
        if not letras:
            continue
        tipo_letra = letras[0]
        if any(letra != tipo_letra for letra in letras):
            return False
        if tipo_letra in letra_columnas:
            return False  # Una letra ya apareció en otra columna
        letra_columnas[tipo_letra] = col
    return True

def aplicar_gravedad(matriz):
    """Hace que las letras caigan al espacio disponible más abajo en cada columna."""
    nueva_matriz = [["_" for _ in range(len(matriz[0]))] for _ in range(len(matriz))]
    for col in range(len(matriz[0])):
        letras = [fila[col] for fila in matriz if fila[col] != "_"]
        for i, letra in enumerate(reversed(letras)):
            nueva_matriz[len(matriz) - 1 - i][col] = letra
    return nueva_matriz

def generar_movimientos(matriz):
    """Genera todos los movimientos posibles desde un estado dado con física de caída."""
    movimientos = []
    columnas = len(matriz[0])
    
    for col_origen in range(columnas):
        # Seleccionar solo la ficha más alta de la columna origen
        fila_origen = next((fila for fila in range(len(matriz)) if matriz[fila][col_origen] != "_"), None)
        if fila_origen is None:
            continue
        
        letra = matriz[fila_origen][col_origen]
        for col_destino in range(columnas):
            if col_origen == col_destino:
                continue
            
            pila_destino = [fila[col_destino] for fila in matriz if fila[col_destino] != "_"]
            
            if not pila_destino or pila_destino[-1] == letra:
                nueva_matriz = [fila[:] for fila in matriz]
                nueva_matriz[fila_origen][col_origen] = "_"  # Eliminar ficha de la posición original
                
                for fila in range(len(matriz)):
                    if nueva_matriz[fila][col_destino] == "_":
                        nueva_matriz[fila][col_destino] = letra
                        break
                
                nueva_matriz = aplicar_gravedad(nueva_matriz)
                movimientos.append(nueva_matriz)
    
    return movimientos

def resolver_a_estrella(matriz):
    """Resuelve el problema usando A* y devuelve los pasos."""
    prioridad = [(heuristica(matriz), 0, matriz, [])]  # (h, g, estado, camino)
    visitados = set()
    
    while prioridad:
        _, costo, estado_actual, camino = heapq.heappop(prioridad)
        clave_estado = str(estado_actual)
        
        if clave_estado in visitados:
            continue
        visitados.add(clave_estado)
        
        if es_estado_final(estado_actual):
            return camino + [estado_actual]  # Solución encontrada
        
        for nuevo_estado in generar_movimientos(estado_actual):
            heapq.heappush(prioridad, (costo + 1 + heuristica(nuevo_estado), costo + 1, nuevo_estado, camino + [estado_actual]))
    
    return None  # No se encontró solución

def guardar_solucion(nombre_archivo, solucion):
    """Guarda la solución en un archivo de salida."""
    ruta_output = os.path.join("Output", f"HA_output_{nombre_archivo}")
    os.makedirs("Output", exist_ok=True)
    with open(ruta_output, "w") as f:
        for paso, matriz in enumerate(solucion):
            f.write(f"Paso {paso}:\n")
            for fila in matriz:
                f.write(" ".join(fila) + "\n")
            f.write("\n")

def solucionarHA(matriz, nombre_archivo):
    solucion = resolver_a_estrella(matriz)
    if solucion:
        guardar_solucion(nombre_archivo, solucion)
        print(f"Solución guardada en Output/HA_output_{nombre_archivo}")
    else:
        print("No se encontró solución")