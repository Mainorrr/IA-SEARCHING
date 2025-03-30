from HeuristicaA import solucionarHA
from HeuristicaIDA import solucionarHIDA
from ListaAbiertaCerrada import solucionarLAC
from time import sleep as timeout


def txt_a_matriz(nombre_archivo):
    ruta_modificada = "Input/" + nombre_archivo
    
    try:
        with open(ruta_modificada, "r") as file:
            matriz = [line.strip().split() for line in file.readlines()]
        
        # Reemplazar 'x' por '_'
        matriz = [[char if char != 'x' else '_' for char in fila] for fila in matriz]
        return matriz
    except FileNotFoundError:
        print("Error: No se encontró el archivo.")
        return None

def mostrar_menu():
    print("\nSeleccione la heurística a utilizar:")
    print("1. Lista Abierta y Cerrada")
    print("2. Heurística A*")
    print("3. Heurística IDA*")
    print("4. Salir")

def main():
    
    while True:
        nombre_archivo = input("Ingrese el nombre del archivo de la carpeta Input: ")
        matriz = txt_a_matriz(nombre_archivo)
        
        if matriz is None:
            return
        
        mostrar_menu()
        opcion = input("Opción: ")
        if opcion == "1":
            print("\nEjecutando Lista Abierta y Cerrada")
            solucionarLAC(matriz,nombre_archivo)
        elif opcion == "2":
            print("\nEjecutando Heurística A*")
            solucionarHA(matriz,nombre_archivo)
        elif opcion == "3":
            print("\nEjecutando Heurística IDA*")
            solucionarHIDA(matriz,nombre_archivo)
        elif opcion == "4":
            print("Cerrando el programa")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
        
        timeout(1)
        print("\nVolviendo al menú principal...")
        timeout(3)


if __name__ == "__main__":
    main()