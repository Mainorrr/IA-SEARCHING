#Para un mejor manejo de las fichas, se acomoda la matriz
#Se hace transpose y se limpia lo vacio para un mejor movimiento
def acomodarMatriz(matriz):
    # Transponer la matriz
    matrizTranspuesta = list(zip(*matriz))

    # Invertir y limpiar columnas usando for tradicional
    matrizNueva = []
    for col in matrizTranspuesta:
        nueva_columna = []
        for elem in reversed(col):
            if elem != '_':
                nueva_columna.append(elem)
        matrizNueva.append(nueva_columna)
    
    return matrizNueva




#Soluciona la matriz para el input correspondiente con LAC
def  solucionarLAC(matriz,nombre_archivo):
    print("Solucionando")
    return
